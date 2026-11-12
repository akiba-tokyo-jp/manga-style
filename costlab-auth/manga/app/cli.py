"""Operator commands, run inside the container (the app listens on 127.0.0.1 there):

    docker exec manga-style python -m app.cli queue
    docker exec manga-style python -m app.cli prompt <node id> [--lang ja|en]
    docker exec -i manga-style python -m app.cli put <node id> - [--model-version V] < picture.png
    docker exec -i manga-style python -m app.cli import < samples.jsonl

`put` stores a new sample for the node (PNG/JPEG, converted to greyscale 768x1024), records the
generation prompt of the node, raises the node's API version and clears its regeneration request.
`import` reads JSON lines {"id", "image_b64", "prompt": {"ja", "en"}, "model_version", "created_at"} and
stores each picture with the prompt that really made it. A line whose picture and prompt are already
stored changes nothing, so the same file can be imported again.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8080"


def call(method: str, path: str, data: bytes | None = None, ctype: str = "application/octet-stream") -> dict | list:
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": ctype} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"error {exc.code}: {body}") from exc


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app.cli")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("queue", help="list regeneration requests")
    p = sub.add_parser("prompt", help="print the sample prompt of a node")
    p.add_argument("id")
    p.add_argument("--lang", choices=("ja", "en"), default="en")
    p = sub.add_parser("put", help="store a new sample image for a node")
    p.add_argument("id")
    p.add_argument("file", help="image path inside the container, or - for stdin")
    p.add_argument("--model-version", default="")
    sub.add_parser("import", help="store samples from JSON lines on stdin (with their recorded prompts)")
    sub.add_parser("import-pairs", help="代表と別場面の2枚を一組として取り込む（JSONL）")
    args = ap.parse_args(argv)
    if args.cmd == "queue":
        for item in call("GET", "/internal/queue"):
            print(f"{item['id']}\t{item['requested_at']}\t{item['note']}")
        return 0
    if args.cmd == "import-pairs":
        count = 0
        for line in sys.stdin.buffer:
            if not line.strip():
                continue
            data = json.loads(line)
            nid = data.pop('id')
            out = call('POST', f"/internal/sample-pairs/{urllib.parse.quote(nid, safe='')}",
                       json.dumps(data, ensure_ascii=False).encode(), 'application/json')
            print(f"{nid}\tversion {out['version']}\t{len(out['samples'])} samples")
            count += 1
        print(f"imported pairs {count}")
        return 0
    if args.cmd == "import":
        count = 0
        for line in sys.stdin.buffer:
            if not line.strip():
                continue
            nid = json.loads(line)["id"]
            out = call("POST", f"/internal/samples/{urllib.parse.quote(nid)}", line, "application/json")
            print(f"{nid}\tversion {out['version']}\t{out['sample']['file']}\t{out['sample']['sha256'][:12]}")
            count += 1
        print(f"imported {count}")
        return 0
    node = urllib.parse.quote(args.id)
    if args.cmd == "prompt":
        print(call("GET", f"/internal/prompt/{node}")["prompt"][args.lang])
        return 0
    raw = sys.stdin.buffer.read() if args.file == "-" else open(args.file, "rb").read()
    query = f"?model_version={urllib.parse.quote(args.model_version)}" if args.model_version else ""
    out = call("POST", f"/internal/samples/{node}{query}", raw)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
