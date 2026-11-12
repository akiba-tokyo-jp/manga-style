"""manga.akiba.tokyo.jp: manga style catalogue (public pages, read API for Genko Studio, admin).

Routing (outer Caddy): /__auth/* -> costlab-auth, /admin* -> forward_auth (costlab-auth) then here,
everything else -> here. The admin routes check the costlab-auth session again themselves
(fail closed), and every admin POST must come from this site's own origin.
"""
from __future__ import annotations

import base64
import http.client
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit, parse_qsl

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from starlette.exceptions import HTTPException as StarletteHTTPException

from .store import (DEFAULT_MODEL_VERSION, EDITABLE, MAX_UPLOAD_BYTES, MODEL_ID, SAMPLE_SIZE, InputError, Store)
from .api_doc import API_DOC, EXAMPLE_IDS, STYLE_FIELDS, TREE_FIELDS
from .ui import LICENSE_TERMS, UI
from .catalogue import (GPT, MODELS, MODEL_COOKIE, TEXT, FACETS,
                        select_model, model_url, catalogue_page)

APP_DIR = Path(__file__).resolve().parent
SITE_ORIGIN = os.environ.get("MANGA_SITE_ORIGIN", "https://manga.akiba.tokyo.jp").rstrip("/")
DATA_DIR = os.environ.get("MANGA_DATA_DIR", "/data")
# costlab-auth's forward_auth endpoint. Unset = admin is closed (fail closed).
ADMIN_VERIFY_URL = os.environ.get("MANGA_ADMIN_VERIFY_URL", "")

PUBLIC_CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
              "object-src 'none'; base-uri 'none'; form-action 'self'")
ADMIN_CSP = PUBLIC_CSP + "; frame-ancestors 'none'"

_store: Store | None = None


def store() -> Store:
    global _store
    if _store is None:
        _store = Store(DATA_DIR)
    return _store


@asynccontextmanager
async def lifespan(_app):
    store()  # load (and on first boot: create) the data before serving
    yield


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
env = Environment(loader=FileSystemLoader(APP_DIR / "templates"), autoescape=select_autoescape(("html",)),
                  undefined=StrictUndefined, trim_blocks=False, lstrip_blocks=False)

# --------------------------------------------------------------------------- helpers
def pick_lang(request: Request, name: str = "lang", default: str | None = None) -> str:
    value = request.query_params.get(name)
    if value in UI:
        return value
    if default:
        return default
    accept = (request.headers.get("accept-language") or "").strip().lower()
    return "en" if accept.startswith("en") else "ja"


def is_genko(request: Request) -> bool:
    return request.query_params.get("client") == "genko" or "GenkoStudio" in (request.headers.get("user-agent") or "")


def page_url(path: str, lang: str, genko: bool, **extra) -> str:
    params = {"lang": lang, **extra}
    if genko:
        params["client"] = "genko"
    return f"{path}?{urlencode(params)}"


def node_path(nid: str) -> str:
    return f"/n/{quote(nid)}"


def file_url(nid: str, name: str) -> str:
    return f"{SITE_ORIGIN}/files/{quote(nid)}/{quote(name)}"


def comparisons_api(s: Store, nid: str) -> list[dict]:
    """/v1/styles comparisons[]: the same sample prompt drawn by another model. Not part of the style:
    adding one does not change version / updated_at, and samples / reference / model are unchanged."""
    cmp = s.comparison(nid)
    if not cmp:
        return []
    return [{"model": {k: cmp["model"][k] for k in ("id", "version", "name")},
             "url": file_url(nid, cmp["file"]), "prompt_from": "samples[0].prompt.en",
             "settings": dict(cmp["settings"]), "created_at": cmp["created_at"]}]


def render(name: str, status: int = 200, csp: str = PUBLIC_CSP, **ctx) -> HTMLResponse:
    body = env.get_template(name).render(**ctx)
    return HTMLResponse(body, status_code=status, headers={"Content-Security-Policy": csp})


def base_ctx(lang: str, genko: bool, switch_url: str, page_title: str | None, breadcrumb: list) -> dict:
    other = "en" if lang == "ja" else "ja"
    return {"lang": lang, "genko": genko, "ui": UI[lang], "lang_switch_url": switch_url,
            "other_lang_label": UI[other]["lang_name"], "page_title": page_title, "breadcrumb": breadcrumb,
            "search_url": page_url("/search", lang, genko)}


def requested_model(request: Request, *, api: bool = False) -> str:
    try:
        return select_model(request.query_params.get('model'),
                            None if api else request.cookies.get(MODEL_COOKIE))
    except ValueError:
        raise HTTPException(400, 'unknown model')


def public_page(name: str, request: Request, ctx: dict, model: str, *, status: int = 200):
    lang, genko = ctx['lang'], ctx['genko']
    switch = urlsplit(ctx['lang_switch_url'])
    ctx['lang_switch_url'] = switch.path + '?' + urlencode({**dict(parse_qsl(switch.query)), 'model': model})
    ctx.update(newui=TEXT[lang], active_model=model, model_info=MODELS[model],
               home_url=model_url('/', lang, genko, model),
               search_url=model_url('/search', lang, genko, model),
               api_guide_url=model_url('/api', lang, genko, model))
    allowed = {'lang', 'plang', 'client', 'root', 'topic', 'q', 'line', 'proportion', 'finish', 'expression', 'view', 'page'}
    current = {k: v[:100] for k, v in request.query_params.items() if k in allowed}
    current['lang'] = lang
    if genko:
        current['client'] = 'genko'
    ctx['model_tabs'] = [{**m, 'active': m['id'] == model,
                          'url': request.url.path + '?' + urlencode({**current, 'model': m['id']})}
                         for m in MODELS.values()]
    body = render(name, status=status, **ctx)
    body.set_cookie(MODEL_COOKIE, model, max_age=31536000, httponly=True,
                    secure=urlsplit(SITE_ORIGIN).scheme == 'https', samesite='lax')
    body.headers['Vary'] = 'Accept-Language, User-Agent, Cookie'
    return body


def gallery(request: Request, root_id: str = ''):
    s = store()
    lang, genko, model = pick_lang(request), is_genko(request), requested_model(request)
    root_id = root_id or (request.query_params.get('root') or '')[:100]
    topic = (request.query_params.get('topic') or '')[:100]
    q = (request.query_params.get('q') or '').strip()[:100]
    facets = {k: (request.query_params.get(k) or '')[:30] for k in FACETS}
    try:
        page = int(request.query_params.get('page') or '1')
        result = catalogue_page(s, model=model, lang=lang, root=root_id, topic=topic,
                                q=q, page=page, facets=facets)
    except (ValueError, OverflowError):
        raise HTTPException(400, 'invalid gallery filter')
    other = 'en' if lang == 'ja' else 'ja'
    selected = {'root': root_id, 'topic': topic, 'q': q, **facets}
    title = s.title(root_id, lang) if root_id else TEXT[lang]['heading']
    ctx = base_ctx(lang, genko, model_url('/search', other, genko, model, **selected), title, [])
    cards = []
    for nid in result['ids']:
        c = card(s, nid, lang, genko, model=model)
        if s.base[nid]['level'] == 1:
            c['url'] = model_url('/styles/' + quote(nid), lang, genko, model)
            c['summary'] = TEXT[lang]['basic']
        cards.append(c)
    ctx.update(cards=cards, gallery_title=title, q=q, selected=selected,
               roots=[{'id': n, 'title': s.title(n, lang), 'url': model_url(node_path(n), lang, genko, model)}
                      for n in result['roots']],
               topics=[{'id': n, 'title': path_text(s, n, lang)} for n in result['topics']],
               facet_options={k: [{'value': value, 'label': ja if lang == 'ja' else en}
                                 for value, ja, en in values] for k, values in FACETS.items()},
               total=result['total'], page=result['page'], pages=result['pages'],
               previous_url=model_url('/search', lang, genko, model, **selected, page=result['page'] - 1)
                            if result['page'] > 1 else None,
               next_url=model_url('/search', lang, genko, model, **selected, page=result['page'] + 1)
                        if result['page'] < result['pages'] else None,
               clear_url=model_url('/search', lang, genko, model, root=root_id),
               topic_basic_url=model_url(node_path(topic), lang, genko, model) if topic else None,
               category_basic_genko='genko://use-style?id=' + root_id if root_id and model == GPT else None,
               registered_count=sum(1 for nid in s.order if s.visible(nid)) if model == GPT else 0)
    return public_page('gallery.html', request, ctx, model)


def path_text(s: Store, nid: str, lang: str, include_self: bool = True) -> str:
    """The category path as one line, e.g. "ギャグ漫画 › シュール › ゆるい手描きの落書き風"."""
    titles = s.path_titles(nid, lang)
    return UI[lang]["path_sep"].join(titles if include_self else titles[:-1])


def card(s: Store, nid: str, lang: str, genko: bool, model: str = GPT) -> dict:
    n = s.effective(nid)
    kids = len(s.children(nid))
    rep = s.representative(nid)
    label = None
    if kids:
        label = UI[lang]["count_genres" if n["level"] == 1 else "count_styles"].format(n=kids)
    # 題名だけでは絵柄が決まらない（同じ題名が別の分類にある）ので、一覧のカードにも上の段の分類を添える。
    return {"id": nid, "title": n["title"][lang], "summary": n["summary"][lang],
            "path": path_text(s, nid, lang, include_self=False),
            "url": model_url(node_path(nid), lang, genko, model), "level": n["level"], "model_name": MODELS[model]["name"],
            "thumb_url": f"/files/{quote(rep[0])}/{quote(rep[1])}" if rep else None, "count_label": label}


def not_found_page(request: Request) -> HTMLResponse:
    lang, genko = pick_lang(request), is_genko(request)
    ctx = base_ctx(lang, genko, page_url("/", "en" if lang == "ja" else "ja", genko),
                   UI[lang]["not_found_title"], [])
    return public_page("error.html", request, ctx, requested_model(request), status=404)


@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    path = request.url.path
    if exc.status_code == 404 and not path.startswith(("/v1/", "/files/", "/static/", "/internal/", "/admin")):
        return not_found_page(request)
    if exc.status_code == 403 and (path == "/admin" or path.startswith("/admin/")):
        return render("admin_denied.html", status=403, csp=ADMIN_CSP, reason=exc.detail, msg=None, err=None)
    headers = dict(exc.headers or {})
    if path.startswith("/v1/"):
        headers.update(cors_headers())
    return JSONResponse({"error": exc.detail if isinstance(exc.detail, str) else "error"},
                        status_code=exc.status_code, headers=headers)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    path = request.url.path
    if path.startswith(("/admin", "/internal/")):
        response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive"
        response.headers["Cache-Control"] = "private, no-store"
    elif path.startswith("/v1/"):
        response.headers.setdefault("Cache-Control", "no-cache")
        response.headers["Vary"] = "Origin, Authorization"
    elif path.startswith("/static/"):
        response.headers.setdefault("Cache-Control", "public, max-age=300")
    elif not path.startswith("/files/"):
        response.headers.setdefault("Cache-Control", "no-cache")
        response.headers["Vary"] = "Accept-Language, User-Agent"
    return response


# --------------------------------------------------------------------------- public pages
@app.get("/healthz")
def healthz():
    s = store()
    return {"ok": True, "nodes": len(s.order), "comparisons": len(s.compare)}


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return "User-agent: *\nDisallow: /admin\nDisallow: /internal/\n"


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return gallery(request)


@app.get('/styles/{nid}', response_class=HTMLResponse)
def direct_style(request: Request, nid: str):
    return node_page(request, nid, direct=True)


@app.get("/n/{nid}", response_class=HTMLResponse)
def node_page(request: Request, nid: str, direct: bool = False):
    s = store()
    if not s.visible(nid):
        return not_found_page(request)
    model = requested_model(request)
    if s.base[nid]['level'] == 1 and not direct:
        return gallery(request, nid)
    lang, genko = pick_lang(request), is_genko(request)
    plang = pick_lang(request, "plang", default=lang)
    n = s.effective(nid)
    other = "en" if lang == "ja" else "ja"
    extra = {"model": model, **({"plang": plang} if plang != lang else {})}
    detail_path = '/styles/' + quote(nid) if direct else node_path(nid)
    switch = model_url(detail_path, other, genko, model, **({"plang": plang} if plang != other else {}))
    crumbs = [{"title": s.effective(c)["title"][lang], "url": page_url(node_path(c), lang, genko, **extra)}
              for c in s.chain(nid)]
    upper = path_text(s, nid, lang, include_self=False)
    # ページの題名（タブ・共有したときの見出し）にも分類を添える。
    shown_title = f"{n['title'][lang]}（{upper}）" if upper and lang == "ja" else (
        f"{n['title'][lang]} ({upper})" if upper else n["title"][lang])
    ctx = base_ctx(lang, genko, switch, shown_title, crumbs)
    # 分類の道筋は題名のすぐ上に出す（node.html）。ページ上端のパンくずは重なるので出さない。
    ctx["path_crumbs"], ctx["breadcrumb"] = crumbs, []
    if model != GPT:
        ctx.update(empty_title=n['title'][lang], empty_path=path_text(s, nid, lang),
                   empty_compare=request.query_params.get('view') == 'compare')
        return public_page('model_empty.html', request, ctx, model)
    prompt = s.style_prompt(nid)
    sample = n["sample"]
    # 同じ題名の絵柄（本人の依頼 2026-09-28: 名前だけで伝わり、別の分類の絵柄が選ばれて制作をやり直した）。
    same = [{"id": k, "path": path_text(s, k, lang), "url": page_url(node_path(k), lang, genko, **extra)}
            for k in s.same_title(nid, lang)]
    cmp = s.comparison(nid) if sample else None
    ui = UI[lang]
    ctx.update(
        node={"id": nid, "level": n["level"], "title": n["title"][lang], "summary": n["summary"][lang],
              "level_label": UI[lang]["level_label"].format(n=n["level"]),
              "path_upper": s.path_titles(nid, lang)[:-1],
              "api_url": f"{SITE_ORIGIN}/v1/styles/{nid}?model={model}", "genko_url": f"genko://use-style?id={nid}"},
        # コピーする文の先頭に付ける 1 行（プロンプトはプロンプトの言語、URL は画面の言語）。
        copy_head={"prompt": TEXT[plang]['model_prefix'].format(name=MODELS[model]['name']) + '\n' + UI[plang]["copy_head"].format(path=path_text(s, nid, plang), id=nid),
                   "url": TEXT[lang]['model_prefix'].format(name=MODELS[model]['name']) + '\n' + UI[lang]["copy_head"].format(path=path_text(s, nid, lang), id=nid)},
        same_title=same,
        sample_pair=[{"url": f"/files/{quote(nid)}/{quote(item['file'])}",
                      "width": item.get("width", SAMPLE_SIZE[0]), "height": item.get("height", SAMPLE_SIZE[1]),
                      "alt": ui["sample_alt"].format(title=n["title"][lang]),
                      "label": ui["sample_representative" if i == 0 else "sample_application"],
                      "prompt": item["prompt"][plang]}
                     for i, item in enumerate(s.samples(nid))] if len(s.samples(nid)) > 1 else [],
        sample=({"url": f"/files/{quote(nid)}/{quote(sample['file'])}",
                 "thumb_url": f"/files/{quote(nid)}/{quote(sample['thumb'])}",
                 "width": SAMPLE_SIZE[0], "height": SAMPLE_SIZE[1],
                 "alt": UI[lang]["sample_alt"].format(title=n["title"][lang])} if sample else None),
        prompt={"text": prompt[plang], "tags": prompt["tags"], "lang": plang},
        prompt_langs=[{"code": code, "label": UI[code]["lang_name"], "current": code == plang,
                       "url": model_url(detail_path, lang, genko, model, **({"plang": code} if code != lang else {}))
                       + "#prompt-heading"} for code in ("ja", "en")],
        sample_prompt=(sample["prompt"][plang] if sample else None),
        children=[card(s, k, lang, genko, model=model) for k in s.children(nid)],
        requested_versions=list(dict.fromkeys(item['model']['version'] for item in s.samples(nid))),
        compare_models=request.query_params.get('view') == 'compare',
        compare_url=model_url(detail_path, lang, genko, model, plang=plang, view='compare'),
        back_to_gallery=model_url(node_path(s.chain(nid)[0]), lang, genko, model),
        # 同じプロンプトで別のモデルが描いた絵（2026-10-18 本人「今の画像サンプルを GPT Image として残し、
        # WAI-Illustrious-SDXL でのサンプルも載せよう」「同じプロンプトでどう変わるのかの対比」）。
        compare=({"base_label": ui["compare_base"].format(version=sample["model"]["version"]),
                  "url": f"/files/{quote(nid)}/{quote(cmp['file'])}",
                  "label": ui["compare_other"].format(name=cmp["model"]["name"], version=cmp["model"]["version"]),
                  "how": ui["compare_how"].format(**cmp["settings"],
                                                  negative=ui["compare_no_negative"] if not cmp["settings"]["negative_prompt"] else cmp["settings"]["negative_prompt"]),
                  "note": ui["compare_note"] + (ui["compare_two_steps"] if n["level"] > 1 else ""),
                  "width": SAMPLE_SIZE[0], "height": SAMPLE_SIZE[1],
                  "alt": ui["compare_alt"].format(title=n["title"][lang], name=cmp["model"]["name"])} if cmp else None),
    )
    return public_page("node.html", request, ctx, model)


@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request):
    return gallery(request)


@app.get("/api", response_class=HTMLResponse)
def api_guide(request: Request):
    """How to use the read API (linked from the footer of every page)."""
    lang, genko = pick_lang(request), is_genko(request)
    other = "en" if lang == "ja" else "ja"
    doc = API_DOC[lang]
    ctx = base_ctx(lang, genko, page_url("/api", other, genko), doc["title"], [{"title": doc["title"], "url": ""}])
    ctx.update(doc=doc, origin=SITE_ORIGIN, tree_fields=TREE_FIELDS[lang], style_fields=STYLE_FIELDS[lang],
               examples=[f"{SITE_ORIGIN}/v1/tree"] + [f"{SITE_ORIGIN}/v1/styles/{i}" for i in EXAMPLE_IDS])
    model = requested_model(request)
    if model != GPT:
        ctx.update(empty_title=TEXT[lang]['empty_heading'], empty_path='')
        return public_page('model_empty.html', request, ctx, model)
    return public_page("api.html", request, ctx, model)


@app.get("/files/{nid}/{name}")
def files(request: Request, nid: str, name: str):
    if requested_model(request, api=True) != GPT:
        raise HTTPException(404, 'not found')
    s = store()
    path = s.sample_path(nid, name) if s.visible(nid) else None
    if path is None:
        raise HTTPException(404, "not found")
    return FileResponse(path, media_type="image/jpeg",
                        headers={"Cache-Control": "public, max-age=31536000, immutable"})


# --------------------------------------------------------------------------- read API (Genko)
def cors_headers() -> dict:
    return {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Authorization", "Access-Control-Max-Age": "600"}


def api_guard(request: Request) -> None:
    s = store()
    if s.api_mode() != "token":
        return
    auth = request.headers.get("authorization") or ""
    scheme, _, token = auth.partition(" ")
    if scheme.lower() != "bearer" or not s.check_token(token.strip()):
        raise HTTPException(401, "unauthorized", headers={"WWW-Authenticate": 'Bearer realm="manga-style"'})


def api_json(request: Request, body: dict) -> JSONResponse:
    headers = cors_headers()
    if store().api_mode() == "token":
        headers["Cache-Control"] = "private, no-store"
    return JSONResponse(body, headers=headers)


def api_lang(request: Request) -> str:
    value = request.query_params.get("lang") or "ja"
    return value if value in UI else "ja"


@app.options("/v1/{rest:path}")
def api_preflight(rest: str):
    return Response(status_code=204, headers=cors_headers())


@app.get('/v1/models')
def api_models(request: Request):
    api_guard(request)
    s = store()
    return api_json(request, {'models': [{**m, 'style_count': sum(s.visible(n) for n in s.order)
                                         if m['id'] == GPT else 0} for m in MODELS.values()]})


@app.get("/v1/tree")
def api_tree(request: Request):
    api_guard(request)
    model = requested_model(request, api=True)
    if model != GPT:
        return api_json(request, {'version': 1, 'nodes': [], 'model': MODELS[model]})
    s = store()
    lang = api_lang(request)
    nodes = []
    for nid in s.order:
        if not s.visible(nid):
            continue
        n = s.effective(nid)
        rep = s.representative(nid)
        nodes.append({"id": nid, "parent": n["parent"], "level": n["level"], "title": n["title"][lang],
                      "summary": n["summary"][lang], "thumbnail_url": file_url(*rep) if rep else None,
                      # 追加の欄（2026-09-28、Genko 側の依頼）: 1段目からこの枝までの表示名（最後がこの枝）。
                      "path": s.path_titles(nid, lang)})
    return api_json(request, {"version": 1, "nodes": nodes})


@app.get("/v1/styles/{nid}")
def api_style(request: Request, nid: str):
    api_guard(request)
    if requested_model(request, api=True) != GPT:
        raise HTTPException(404, 'not found')
    s = store()
    if not s.visible(nid):
        raise HTTPException(404, "not found")
    lang = api_lang(request)
    n = s.effective(nid)
    sample = n["sample"]
    samples = [{"subject": item["subject"], "url": file_url(nid, item["file"]),
                "prompt": {"ja": item["prompt"]["ja"], "en": item["prompt"]["en"]}}
               for item in s.samples(nid)]
    children = []
    for k in s.children(nid):
        kn = s.effective(k)
        rep = s.representative(k)
        children.append({"id": k, "title": kn["title"][lang], "summary": kn["summary"][lang],
                         "thumbnail_url": file_url(*rep) if rep else None})
    body = {
        "id": nid,
        # 上の段（1段目から親まで）の id と表示名。1段目は空の配列（2026-09-28、Genko 側の依頼）。
        "path": [{"id": c, "title": s.title(c, lang)} for c in s.chain(nid)[:-1]],
        "level": n["level"],
        "title": n["title"][lang],
        "summary": n["summary"][lang],
        "expression": s.expression(nid),
        "model": {"id": MODEL_ID, "version": sample["model"]["version"] if sample else None},
        "prompt": s.style_prompt(nid),
        "avoid": s.avoid_for(nid),
        "samples": samples,
        "reference": 0 if samples else None,
        "license": {"generated": True, "artist_names": False, "terms": LICENSE_TERMS},
        "version": n["version"],
        "updated_at": n["updated_at"],
        # 追加の欄（2026-09-27、Genko 側の依頼）: 公開中の 1 つ下の段。3段目は空。
        "children": children,
        # 追加の欄（2026-10-18）: 同じ見本のプロンプトを別の画像生成モデルで描いた比較の絵。絵柄の一部ではない。
        "comparisons": comparisons_api(s, nid),
    }
    return api_json(request, body)


# --------------------------------------------------------------------------- admin
def admin_allowed(request: Request) -> bool:
    """Ask costlab-auth whether this request carries a valid session (never follow its redirect)."""
    if not ADMIN_VERIFY_URL:
        return False
    target = urlsplit(ADMIN_VERIFY_URL)
    conn_cls = http.client.HTTPSConnection if target.scheme == "https" else http.client.HTTPConnection
    conn = conn_cls(target.hostname or "", target.port, timeout=3)
    try:
        conn.request("GET", target.path or "/", headers={
            "Cookie": request.headers.get("cookie", ""),
            "X-Forwarded-Uri": request.url.path,
            "X-Forwarded-Host": urlsplit(SITE_ORIGIN).hostname or "",
            "X-Forwarded-Proto": "https",
        })
        status = conn.getresponse().status
    except OSError:
        return False
    finally:
        conn.close()
    return 200 <= status < 300


def require_admin(request: Request, post: bool = False) -> None:
    if post:
        origin = request.headers.get("origin")
        fetch_site = request.headers.get("sec-fetch-site")
        if origin != SITE_ORIGIN or (fetch_site and fetch_site != "same-origin"):
            raise HTTPException(403, "origin")
    if not admin_allowed(request):
        raise HTTPException(403, "session")


def admin_node_url(nid: str | None, msg: str | None = None, err: str | None = None) -> str:
    base = "/admin" if nid is None else f"/admin/n/{quote(nid)}"
    params = {k: v for k, v in (("msg", msg), ("err", err)) if v}
    return base + (f"?{urlencode(params)}" if params else "")


def admin_row(s: Store, nid: str) -> dict:
    n = s.effective(nid)
    return {"id": nid, "title": n["title"]["ja"], "title_en": n["title"]["en"], "published": n["published"],
            "path": " › ".join(s.path_titles(nid, "ja")[:-1]),
            "visible": s.visible(nid), "has_sample": bool(n["sample"]), "regen": bool(n["regen"]),
            "edited": n["edited"], "version": n["version"], "kids": len(s.kids.get(nid, [])),
            "url": admin_node_url(nid)}


def admin_render(name: str, request: Request, **ctx) -> HTMLResponse:
    ctx.setdefault("msg", request.query_params.get("msg"))
    ctx.setdefault("err", request.query_params.get("err"))
    return render(name, csp=ADMIN_CSP, **ctx)


@app.get("/admin", response_class=HTMLResponse)
def admin_home(request: Request):
    require_admin(request)
    s = store()
    return admin_render("admin_index.html", request, stats=s.stats(), api_mode=s.api_mode(), tokens=s.tokens(),
                        rows=[admin_row(s, k) for k in s.kids.get(None, [])], new_token=None)


@app.get("/admin/n/{nid}", response_class=HTMLResponse)
def admin_node(request: Request, nid: str):
    require_admin(request)
    s = store()
    if not s.exists(nid):
        raise HTTPException(404, "not found")
    n = s.effective(nid)
    gen = s.generation_prompt(nid)
    fields = {key: n[field][lang] for key, (field, lang, _) in EDITABLE.items()}
    pending = s.state['nodes'][nid].get('pending_style')
    if pending:
        fields.update({f'words_{lang}':text for lang,text in pending.items()})
    sample = n["sample"]
    return admin_render(
        "admin_node.html", request, node=n, row=admin_row(s, nid), fields=fields,
        limits={key: limit for key, (_, _, limit) in EDITABLE.items()},
        crumbs=[{"title": s.effective(c)["title"]["ja"], "url": admin_node_url(c)} for c in s.chain(nid)],
        hidden_by=[s.effective(c)["title"]["ja"] for c in s.chain(nid)[:-1] if not s.effective(c)["published"]],
        sample=({**sample, "url": f"/admin/files/{quote(nid)}/{quote(sample['file'])}"} if sample else None),
        gen_prompt=gen, style_prompt=s.style_prompt(nid), public_url=node_path(nid) + "?lang=ja",
        rows=[admin_row(s, k) for k in s.kids.get(nid, [])], default_model=DEFAULT_MODEL_VERSION,
    )


@app.get("/admin/files/{nid}/{name}")
def admin_files(request: Request, nid: str, name: str):
    require_admin(request)
    path = store().sample_path(nid, name)
    if path is None:
        raise HTTPException(404, "not found")
    return FileResponse(path, media_type="image/jpeg")


@app.get("/admin/queue", response_class=HTMLResponse)
def admin_queue(request: Request):
    require_admin(request)
    return admin_render("admin_queue.html", request, items=store().queue())


def _node_action(request: Request, nid: str, action, ok: str, redirect_to: str | None = None):
    require_admin(request, post=True)
    s = store()
    if not s.exists(nid):
        raise HTTPException(404, "not found")
    try:
        action(s)
    except InputError as exc:
        return RedirectResponse(admin_node_url(nid, err=str(exc)), status_code=303)
    return RedirectResponse(redirect_to or admin_node_url(nid, msg=ok), status_code=303)


def _back_url(back: str, msg: str) -> str | None:
    """Where a publish/hide button in a list returns to: "top" = admin top, a node id = that node, else the node."""
    if back == "top":
        return admin_node_url(None, msg=msg)
    if back and store().exists(back):
        return admin_node_url(back, msg=msg)
    return None


@app.post("/admin/n/{nid}/publish")
def admin_publish(request: Request, nid: str, back: str = Form("")):
    return _node_action(request, nid, lambda s: s.set_published(nid, True), "公開しました。",
                        _back_url(back, "公開しました。"))


@app.post("/admin/n/{nid}/hide")
def admin_hide(request: Request, nid: str, back: str = Form("")):
    return _node_action(request, nid, lambda s: s.set_published(nid, False), "隠しました。",
                        _back_url(back, "隠しました。"))


@app.post("/admin/n/{nid}/edit")
def admin_edit(request: Request, nid: str, title_ja: str = Form(...), title_en: str = Form(...),
               summary_ja: str = Form(...), summary_en: str = Form(...), words_ja: str = Form(...),
               words_en: str = Form(...), words_tags: str = Form(...)):
    values = {"title_ja": title_ja, "title_en": title_en, "summary_ja": summary_ja, "summary_en": summary_en,
              "words_ja": words_ja, "words_en": words_en, "words_tags": words_tags}
    return _node_action(request, nid, lambda s: s.edit(nid, values), "保存しました。")


@app.post("/admin/n/{nid}/reset")
def admin_reset(request: Request, nid: str):
    return _node_action(request, nid, lambda s: s.reset(nid), "元の内容に戻しました。")


@app.post("/admin/n/{nid}/regen")
def admin_regen(request: Request, nid: str, note: str = Form("")):
    return _node_action(request, nid, lambda s: s.request_regen(nid, note), "作り直しを頼みました。")


@app.post("/admin/n/{nid}/regen-cancel")
def admin_regen_cancel(request: Request, nid: str):
    return _node_action(request, nid, lambda s: s.cancel_regen(nid), "作り直しの依頼を取り消しました。")


async def _read_upload(upload: UploadFile) -> bytes:
    data = await upload.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise InputError("画像が 20MB を超えています。")
    return data


@app.post("/admin/n/{nid}/sample")
async def admin_sample(request: Request, nid: str, image: UploadFile = File(...),
                       model_version: str = Form(""), prompt_ja: str = Form(""), prompt_en: str = Form("")):
    require_admin(request, post=True)
    s = store()
    if not s.exists(nid):
        raise HTTPException(404, "not found")
    try:
        raw = await _read_upload(image)
        s.put_sample(nid, raw, prompt={"ja": prompt_ja, "en": prompt_en}, model_version=model_version,
                     origin="admin")
    except InputError as exc:
        return RedirectResponse(admin_node_url(nid, err=str(exc)), status_code=303)
    return RedirectResponse(admin_node_url(nid, msg="見本の絵を差し替えました。"), status_code=303)


@app.post("/admin/api-mode")
def admin_api_mode(request: Request, mode: str = Form(...)):
    require_admin(request, post=True)
    try:
        store().set_api_mode(mode)
    except InputError as exc:
        return RedirectResponse(admin_node_url(None, err=str(exc)), status_code=303)
    return RedirectResponse(admin_node_url(None, msg="API の公開の方法を変えました。"), status_code=303)


@app.post("/admin/tokens")
def admin_token_create(request: Request, label: str = Form("")):
    require_admin(request, post=True)
    s = store()
    plain = s.create_token(label)
    return admin_render("admin_index.html", request, stats=s.stats(), api_mode=s.api_mode(), tokens=s.tokens(),
                        rows=[admin_row(s, k) for k in s.kids.get(None, [])], new_token=plain,
                        msg="トークンを作りました。この画面を閉じると二度と表示されません。")


@app.post("/admin/tokens/{tid}/revoke")
def admin_token_revoke(request: Request, tid: str):
    require_admin(request, post=True)
    try:
        store().revoke_token(tid)
    except InputError as exc:
        return RedirectResponse(admin_node_url(None, err=str(exc)), status_code=303)
    return RedirectResponse(admin_node_url(None, msg="トークンを消しました。"), status_code=303)


# --------------------------------------------------------------------------- internal (docker exec only)
def require_loopback(request: Request) -> None:
    """Only a process inside this container (docker exec ... python -m app.cli) reaches 127.0.0.1."""
    host = request.client.host if request.client else ""
    if host not in ("127.0.0.1", "::1"):
        raise HTTPException(404, "not found")


@app.get("/internal/queue")
def internal_queue(request: Request):
    require_loopback(request)
    return store().queue()


@app.get("/internal/prompt/{nid}")
def internal_prompt(request: Request, nid: str):
    require_loopback(request)
    s = store()
    if not s.exists(nid):
        raise HTTPException(404, "not found")
    return {"id": nid, "prompt": s.generation_prompt(nid)}


@app.post("/internal/sample-pairs/{nid}")
async def internal_sample_pair(request: Request, nid: str):
    """Loopback operator import: bounded JSON, both images and their exact prompts together."""
    require_loopback(request)
    s = store()
    if not s.exists(nid):
        raise HTTPException(404, 'not found')
    raw = bytearray()
    async for chunk in request.stream():
        if len(raw) + len(chunk) > MAX_UPLOAD_BYTES * 3 + 64000:
            raise HTTPException(413, '画像2枚の上限を超えています。')
        raw.extend(chunk)
    try:
        data = json.loads(raw)
        if not isinstance(data, dict) or set(data) - {'samples','style_prompt_sha256','complete_style'}:
            raise InputError('2枚組の入力形式が違います。')
        items = data.get('samples')
        if not isinstance(items, list) or len(items) != 2:
            raise InputError('見本は2枚必要です。')
        clean = []
        for item in items:
            if not isinstance(item, dict) or set(item) != {'subject','image_b64','prompt','model_version','created_at'}:
                raise InputError('画像の記録の形式が違います。')
            encoded = item['image_b64']
            if not isinstance(encoded, str) or len(encoded) > (MAX_UPLOAD_BYTES+2)//3*4:
                raise InputError('画像が上限を超えています。')
            clean.append({**{k:v for k,v in item.items() if k != 'image_b64'},
                          'raw':base64.b64decode(encoded,validate=True)})
        records = s.put_sample_pair(nid, clean, data.get('style_prompt_sha256'),
                                    complete_style=data.get('complete_style'))
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(400, str(exc) if isinstance(exc, InputError) else '2枚組の入力を読み取れません。') from exc
    return {'id':nid,'version':s.effective(nid)['version'],'samples':records}


@app.post("/internal/samples/{nid}")
async def internal_sample(request: Request, nid: str, model_version: str = ""):
    """The body is the image, or JSON {image_b64, prompt {ja, en}, model_version, created_at} to keep the
    prompt that really made the picture (python -m app.cli import)."""
    require_loopback(request)
    s = store()
    if not s.exists(nid):
        raise HTTPException(404, "not found")
    raw = await request.body()
    prompt, created_at = None, None
    try:
        if (request.headers.get("content-type") or "").startswith("application/json"):
            try:
                doc = json.loads(raw)
                raw = base64.b64decode(doc["image_b64"], validate=True)
                prompt = {lang: str(doc["prompt"][lang]) for lang in ("ja", "en")}
            except (ValueError, KeyError, TypeError) as exc:
                raise InputError("JSON の形が違います（image_b64, prompt.ja, prompt.en が要ります）。") from exc
            model_version = str(doc.get("model_version") or model_version)
            created_at = doc.get("created_at")
        sample = s.put_sample(nid, raw, prompt=prompt, model_version=model_version or None, origin="cli",
                              created_at=created_at)
    except InputError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    n = s.effective(nid)
    return {"id": nid, "version": n["version"], "updated_at": n["updated_at"], "sample": sample}


