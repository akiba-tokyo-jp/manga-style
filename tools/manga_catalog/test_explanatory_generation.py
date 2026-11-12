"""独立生成の入力、再開、履歴混入防止（外部生成は呼ばない）。"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_explanatory as gen

class GenerationTests(unittest.TestCase):
    def job(self, nid='shonen-battle-chibi-comic', role='representative'):
        return {'id': nid, 'subject': role, 'prompt': {'ja': '白黒の絵。男性が立つ。', 'en': 'Black ink. A man standing.'},
                'aspect_ratio': 'portrait', 'style_prompt_sha256': 'a'*64, 'expression': 'mono'}

    def test_manifest_rejects_duplicate_unsafe_and_history_fields(self):
        a = self.job()
        self.assertEqual(gen.validate_jobs([a]), [a])
        for jobs in [[a,a], [dict(a,id='../escape')], [dict(a,messages=[])], [dict(a,image_url='old.png')],
                     [dict(a,previous_response_id='previous')], [dict(a,aspect_ratio='1:1')]]:
            with self.subTest(jobs=jobs), self.assertRaises(ValueError):
                gen.validate_jobs(jobs)

    def test_request_is_one_prompt_no_prior_conversation_and_exact_model(self):
        body = {'prompt': self.job()['prompt']['en'], 'model': gen.MODEL, 'n': 1,
                'quality': 'high', 'size': '1024x1536', 'background': 'opaque'}
        gen.validate_request(self.job(), 'images/generations', body)
        for extra in [{'messages': []}, {'conversation_id':'old'}, {'images':[]}, {'model':'gpt-image-2.5-sunburst'}]:
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                gen.validate_request(self.job(), 'images/generations', dict(body, **extra))

    def test_local_validation_driver_propagates_failed_child(self):
        import contextlib
        import io
        from unittest.mock import patch
        import validate_explanatory as validation
        with tempfile.TemporaryDirectory() as d:
            with patch.object(validation,'COMMANDS',[['-c','raise SystemExit(7)']]), \
                 patch.object(sys,'argv',['validate_explanatory','--output',d]), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(validation.main(),1)
            receipt=json.loads((Path(d)/'result.json').read_text())
            self.assertIs(receipt['passed'],False)
            self.assertEqual(receipt['commands'][0]['exit_code'],7)

    def test_completion_requires_final_matching_request_and_actual_image(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            img = p/'original.png'
            img.write_bytes(b'explicit synthetic fixture, not a generated image')
            rec = {'job_sha256':gen.digest(self.job()), 'image':'original.png', 'image_sha256':gen.file_sha(img),
                   'success':True}
            (p/'complete.json').write_text(json.dumps(rec))
            self.assertTrue(gen.completed(self.job(),p))
            img.write_bytes(b'changed')
            with self.assertRaises(ValueError):
                gen.completed(self.job(),p)
            with self.assertRaises(ValueError):
                gen.completed(dict(self.job(),aspect_ratio='square'),p)

if __name__ == '__main__':
    unittest.main()
