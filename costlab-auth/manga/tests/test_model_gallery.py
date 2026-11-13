"""承認済みgallery導線・モデル選択・空モデルの分離。生成/ネットワーク無し。"""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit
from html.parser import HTMLParser

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from fastapi.testclient import TestClient
from app import main
from app.store import Store


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'a':
            self.links.append(values)


class ModelGalleryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='manga-model-gallery-')
        self.data = Path(self.tmp.name)
        seed = self.data/'seed'
        seed.mkdir()
        for p in (HERE.parent/'app/seed').iterdir():
            if p.is_file():
                shutil.copy2(p, seed/p.name)
        main._store = Store(self.data, seed_dir=seed, compare_dir=self.data/'no-compare')
        self.client = TestClient(main.app, base_url='https://manga.akiba.tokyo.jp')
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        main._store = None
        self.tmp.cleanup()

    def test_category_opens_flat_gallery_not_second_level_gate(self):
        r = self.client.get('/n/shonen?lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertIn('id="gallery-results"', r.text)
        cards = [a for a in Links(r.text).links if 'gallery-card' in a.get('class', '')]
        self.assertTrue(any(a.get('data-level') == '3' for a in cards))
        self.assertTrue(all(parse_qs(urlsplit(a['href']).query)['model'] == ['gpt-image'] for a in cards))
        self.assertNotIn('次の段を選ぶ', r.text)

    def test_topic_is_optional_filter_not_an_extra_page(self):
        r = self.client.get('/search?root=shonen&topic=shonen-school&lang=ja')
        self.assertEqual(r.status_code, 200)
        cards = [a for a in Links(r.text).links if 'gallery-card' in a.get('class', '')]
        self.assertTrue(cards)
        self.assertTrue(all(a['data-style-id'].startswith('shonen-school') for a in cards))

    def test_look_based_second_level_stays_a_selectable_style(self):
        r = self.client.get('/search?root=gag&q=gag-hetauma&lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertIn('data-style-id="gag-hetauma"', r.text)

    def test_model_choice_survives_navigation_language_search_and_revisit(self):
        r = self.client.get('/?model=anima-turbo&lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.client.cookies.get('manga_model'), 'anima-turbo')
        self.assertIn('Anima Turbo', r.text)
        self.assertIn('準備中', r.text)
        self.assertNotIn('/files/', r.text)
        for path in ['/n/shonen?lang=ja', '/search?q=線&lang=en', '/n/gag-hetauma?lang=ja', '/api?lang=ja', '/']:
            result = self.client.get(path)
            self.assertEqual(result.status_code, 200, path)
            self.assertIn('data-active-model="anima-turbo"', result.text)
            self.assertNotIn('/files/', result.text)
        for a in Links(r.text).links:
            path = urlsplit(a.get('href', '')).path
            if path.startswith(('/n/', '/search')):
                self.assertEqual(parse_qs(urlsplit(a['href']).query).get('model'), ['anima-turbo'])

    def test_explicit_URL_model_wins_over_saved_preference(self):
        self.client.get('/?model=anima-turbo')
        r = self.client.get('/n/shonen-battle-bold-black?model=gpt-image&lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertIn('data-active-model="gpt-image"', r.text)
        self.assertIn('/files/shonen-battle-bold-black/', r.text)
        self.assertEqual(self.client.cookies.get('manga_model'), 'gpt-image')

    def test_anima_detail_never_reuses_GPT_prompt_image_copy_or_Genko(self):
        before = main.store().style_prompt('shonen-battle-bold-black')['en']
        r = self.client.get('/n/shonen-battle-bold-black?model=anima-turbo&lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertIn('準備中', r.text)
        self.assertNotIn(before, r.text)
        self.assertNotIn('/files/', r.text)
        self.assertNotIn('data-copy-target=', r.text)
        self.assertNotIn('genko://', r.text)

    def test_API_legacy_default_is_GPT_and_ignores_UI_cookie(self):
        original = self.client.get('/v1/styles/shonen-battle-bold-black').json()
        self.client.get('/?model=anima-turbo')
        explicit = self.client.get('/v1/styles/shonen-battle-bold-black?model=gpt-image').json()
        self.assertEqual(self.client.get('/v1/styles/shonen-battle-bold-black').json(), original)
        self.assertEqual(explicit, original)
        self.assertEqual(self.client.get('/v1/tree?model=gpt-image').json(), self.client.get('/v1/tree').json())

    def test_anima_API_is_empty_instead_of_GPT_fallback(self):
        r = self.client.get('/v1/tree?model=anima-turbo')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['nodes'], [])
        self.assertEqual(r.json()['model']['id'], 'anima-turbo')
        self.assertEqual(self.client.get('/v1/styles/shonen-battle-bold-black?model=anima-turbo').status_code, 404)

    def test_anima_explicit_file_request_does_not_return_GPT_image(self):
        s = main.store().samples('shonen-battle-bold-black')[0]
        self.assertEqual(self.client.get('/files/shonen-battle-bold-black/'+s['file']+'?model=anima-turbo').status_code, 404)
        self.assertEqual(self.client.get('/files/shonen-battle-bold-black/'+s['file']).status_code, 200)

    def test_unknown_model_is_rejected_without_fallback(self):
        for path in ['/?model=unknown', '/search?model=unknown', '/n/gag?model=unknown', '/v1/tree?model=unknown']:
            self.assertEqual(self.client.get(path).status_code, 400, path)

    def test_clear_filters_label_is_localized_text_not_dict_method(self):
        for lang, label in (('ja', '条件をクリア'), ('en', 'Clear filters')):
            with self.subTest(lang=lang):
                # The dynamic Anima fixture is intentionally empty; populated
                # static galleries share this template with the GPT gallery.
                response = self.client.get(f'/search?model=gpt-image&lang={lang}')
                self.assertEqual(response.status_code, 200)
                self.assertRegex(response.text, r'class="filter-clear"[^>]*>' + label + r'</a>')
                self.assertNotIn('built-in method', response.text)

    def test_gallery_pagination_retains_filters_and_model(self):
        r = self.client.get('/search?root=shonen&model=gpt-image&lang=en&page=2')
        self.assertEqual(r.status_code, 200)
        pages = [a for a in Links(r.text).links if 'page-link' in a.get('class', '')]
        self.assertTrue(pages)
        for a in pages:
            q = parse_qs(urlsplit(a['href']).query)
            self.assertEqual(q['model'], ['gpt-image'])
            self.assertEqual(q['root'], ['shonen'])
            self.assertEqual(q['lang'], ['en'])

    def test_model_tabs_keep_search_filters_and_page_position(self):
        r = self.client.get('/search?root=shonen&q=line&page=2&lang=en&model=gpt-image')
        link = next(a for a in Links(r.text).links if a.get('class', '').startswith('model-tab')
                    and parse_qs(urlsplit(a['href']).query).get('model') == ['anima-turbo'])
        query = parse_qs(urlsplit(link['href']).query)
        self.assertEqual(query['page'], ['2'])
        self.assertEqual(query['q'], ['line'])
        self.assertEqual(query['root'], ['shonen'])

    def test_hidden_style_is_not_in_any_gallery_or_model(self):
        main.store().set_published('shonen-battle', False)
        r = self.client.get('/search?q=shonen-battle&model=gpt-image')
        self.assertNotIn('data-style-id="shonen-battle-bold-black"', r.text)
        self.assertEqual(self.client.get('/n/shonen-battle-bold-black?model=anima-turbo').status_code, 404)

    def test_pure_UI_requests_do_not_change_GPT_state_or_prompts(self):
        before = (self.data/'state.json').read_bytes()
        for p in ['/?model=gpt-image', '/n/shonen?model=gpt-image', '/search?root=shonen&line=thin', '/n/shonen-battle-bold-black?model=anima-turbo']:
            self.client.get(p)
        self.assertEqual((self.data/'state.json').read_bytes(), before)

    def test_detail_copy_identifies_model_and_keeps_actual_prompt(self):
        r = self.client.get('/n/shonen-battle-bold-black?model=gpt-image&lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertIn('モデル: GPT Image', r.text)
        self.assertIn('data-copy-target="sample-prompt-0"', r.text)
        self.assertIn('model=gpt-image', r.text)

    def test_no_mandatory_topic_for_search(self):
        r = self.client.get('/search?q=doodle&model=gpt-image&lang=ja')
        self.assertEqual(r.status_code, 200)
        self.assertIn('id="gallery-results"', r.text)
        self.assertIn('gallery-card', r.text)

    def test_not_found_keeps_selected_model_in_header(self):
        self.client.get('/?model=anima-turbo')
        r = self.client.get('/n/missing-style?lang=ja')
        self.assertEqual(r.status_code, 404)
        self.assertIn('data-active-model="anima-turbo"', r.text)

    def test_api_guide_language_link_explicitly_keeps_model(self):
        r = self.client.get('/api?model=anima-turbo&lang=ja')
        links = [a for a in Links(r.text).links if a.get('hreflang') == 'en']
        self.assertTrue(links)
        self.assertEqual(parse_qs(urlsplit(links[0]['href']).query)['model'], ['anima-turbo'])

    def test_negative_screentone_tag_is_not_positive_tone_filter(self):
        from app.catalogue import features_match
        self.assertFalse(features_match({'tags': 'pen-only, no screentone'}, {'finish': 'tone'}, 'mono'))

    def test_model_switch_overrides_the_spread_header_rule(self):
        css = (HERE.parent/'app/static/gallery.css').read_text()
        match = __import__('re').search(r'\.site-header \.model-switch\s*\{([^}]*)\}', css)
        self.assertIsNotNone(match, 'group selector must beat .site-header .wrap')
        declarations = match.group(1).replace(' ', '')
        self.assertIn('justify-content:flex-start', declarations)

    def test_search_action_does_not_shrink_or_wrap(self):
        css = (HERE.parent/'app/static/gallery.css').read_text()
        match = __import__('re').search(r'\.gallery-search \.button\s*\{([^}]*)\}', css)
        self.assertIsNotNone(match)
        declarations = match.group(1).replace(' ', '')
        self.assertIn('flex:00auto', declarations)
        self.assertIn('white-space:nowrap', declarations)
        self.assertRegex(css, r'\.gallery-search \.search-row\{[^}]*align-items:stretch')

    def test_model_registry_exposes_empty_anima_status(self):
        r = self.client.get('/v1/models')
        self.assertEqual(r.status_code, 200)
        models = {m['id']: m for m in r.json()['models']}
        self.assertEqual(models['anima-turbo']['name'], 'Anima Turbo')
        self.assertEqual(models['anima-turbo']['style_count'], 0)
        self.assertEqual(models['anima-turbo']['status'], 'preparing')


class RunnerInventoryTests(unittest.TestCase):
    def test_model_gallery_suite_is_registered_exactly_once(self):
        import ast
        source = HERE.parents[2]/'tools/manga_catalog/validate_explanatory.py'
        tree = ast.parse(source.read_text())
        commands = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == 'COMMANDS' for t in n.targets))
        self.assertEqual(sum('test_model_gallery.py' in c for c in commands), 1)


if __name__ == '__main__':
    unittest.main()
