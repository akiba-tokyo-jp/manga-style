#!/usr/bin/env python3
"""Real Caddy routing for manga.akiba.tokyo.jp: the production block of caddy/Caddyfile, run by a real
Caddy binary, in front of stub upstreams.

    CADDY_BIN=/path/to/caddy python costlab-auth/manga/tests/caddy_routing.py            # the tests
    CADDY_BIN=/path/to/caddy python costlab-auth/manga/tests/caddy_routing.py --power    # detection power

CI takes the binary from caddy:latest, the tag production runs (caddy/docker-compose.yml).
Without CADDY_BIN every test is SKIPPED, which means UNVERIFIED, never passed (--require turns that
into a failure).

Only the address, the tls line and the upstreams of the block are substituted:
  costlab-auth:8000 -> auth stub: 204 when the Cookie holds costlab_session=good, else 303 to login
  manga-style:8080  -> app stub: records every request (method, path, headers, cookies, body)

Why this exists: on 2026-09-26 the admin answered {"error":"forbidden"} right after a successful login.
Caddy 2.11's forward_auth `copy_headers Cookie` deletes the Cookie from the request it forwards
when the auth response has no Cookie header (a 204 has none), so the app's own session re-check
got no cookie. Unit tests with a fake auth server could not see it; only a real Caddy can.
"""
from __future__ import annotations

import http.client
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CADDYFILE = Path(os.environ.get("MANGA_CADDYFILE") or ROOT / "caddy" / "Caddyfile")
CADDY = os.environ.get("CADDY_BIN", "")
HOST = "manga.akiba.tokyo.jp"
GOOD = "costlab_session=good"
ORIGIN = "https://manga.akiba.tokyo.jp"


def site_block(text: str, address: str) -> str:
    """The exact text of one top-level site block (brace matched)."""
    m = re.search(r"^" + re.escape(address) + r" \{\r?$", text, re.M)
    if not m:
        raise AssertionError(f"site block {address!r} not found")
    depth = 0
    for j in range(m.end() - 1, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[m.start():j + 1]
    raise AssertionError("unbalanced site block")


def local_config(block: str, port: int, auth_port: int, app_port: int) -> str:
    assert block.count("manga-style:8080") == 1, "the block must proxy to manga-style exactly once"
    assert "costlab-auth:8000" in block, "the block must use costlab-auth"
    lines = [ln for ln in block.splitlines()[1:] if not ln.strip().startswith("tls ")]
    body = "\n".join(lines)
    body = body.replace("costlab-auth:8000", f"127.0.0.1:{auth_port}")
    body = body.replace("manga-style:8080", f"127.0.0.1:{app_port}")
    return "{\n\tadmin off\n}\n\n" + f"http://:{port} {{\n" + body + "\n"


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class Stub(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    log: list = []

    def record(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        self.log.append({"method": self.command, "path": self.path,
                         "headers": {k.lower(): v for k, v in self.headers.items()},
                         "cookies": self.headers.get_all("Cookie") or [], "body": body})

    def send(self, status: int, headers: dict | None = None, body: bytes = b"") -> None:
        self.send_response(status)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def log_message(self, *args):  # noqa: D401 - quiet
        pass


class AuthStub(Stub):
    def answer(self) -> None:
        self.record()
        if self.path.startswith("/__auth/verify"):
            if any(GOOD in c for c in (self.headers.get_all("Cookie") or [])):
                return self.send(204)
            nxt = self.headers.get("X-Forwarded-Uri", "/")
            return self.send(303, {"Location": f"/__auth/login?next={nxt}"})
        return self.send(200, {"Content-Type": "text/plain"}, b"auth:" + self.path.encode())

    do_GET = do_POST = answer


class AppStub(Stub):
    def answer(self) -> None:
        self.record()
        self.send(200, {"Content-Type": "application/json"}, json.dumps({"app": self.path}).encode())

    do_GET = do_POST = do_HEAD = answer


class QuietServer(ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        pass


class Stack:
    """real Caddy (production block) -> {auth stub, app stub}."""

    def __init__(self, caddy: str, block: str):
        self.caddy, self.block = caddy, block

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="manga-caddy-")
        tmp = Path(self.tmp.name)
        self.auth_log: list = []
        self.app_log: list = []
        self.auth = QuietServer(("127.0.0.1", 0), type("Auth", (AuthStub,), {"log": self.auth_log}))
        self.app = QuietServer(("127.0.0.1", 0), type("App", (AppStub,), {"log": self.app_log}))
        for server in (self.auth, self.app):
            threading.Thread(target=server.serve_forever, daemon=True).start()
        self.port = free_port()
        cfg = tmp / "Caddyfile"
        cfg.write_text(local_config(self.block, self.port, self.auth.server_port, self.app.server_port),
                       encoding="utf-8")
        env = dict(os.environ, XDG_CONFIG_HOME=str(tmp), XDG_DATA_HOME=str(tmp), HOME=str(tmp))
        self.log_path = tmp / "caddy.log"
        self.log_file = self.log_path.open("w")
        self.proc = subprocess.Popen([self.caddy, "run", "--config", str(cfg), "--adapter", "caddyfile"],
                                     env=env, stdout=self.log_file, stderr=subprocess.STDOUT)
        deadline = time.time() + 20
        while time.time() < deadline:
            if self.proc.poll() is not None:
                raise AssertionError("caddy exited:\n" + self.log_path.read_text())
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.5):
                    break
            except OSError:
                time.sleep(0.05)
        else:
            raise AssertionError("caddy never listened:\n" + self.log_path.read_text())
        return self

    def __exit__(self, *exc):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        self.log_file.close()
        for server in (self.auth, self.app):
            server.shutdown()
            server.server_close()
        self.tmp.cleanup()


def request(port: int, method: str, path: str, headers=None, body: bytes | None = None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        hdrs = {"Host": HOST}
        hdrs.update(headers or {})
        conn.request(method, path, body=body, headers=hdrs)
        resp = conn.getresponse()
        data = resp.read()
        return resp.status, {k.lower(): v for k, v in resp.getheaders()}, data
    finally:
        conn.close()


@unittest.skipUnless(CADDY, "CADDY_BIN not set: real Caddy routing of manga.akiba.tokyo.jp UNVERIFIED")
class MangaCaddyRouting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        block = site_block(CADDYFILE.read_text(encoding="utf-8"), HOST)
        cls.stack = Stack(CADDY, block).__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.stack.__exit__(None, None, None)

    def setUp(self):
        self.stack.auth_log.clear()
        self.stack.app_log.clear()

    def call(self, method, path, headers=None, body=None):
        return request(self.stack.port, method, path, headers, body)

    def test_admin_without_session_is_sent_to_the_login_page(self):
        for path in ("/admin", "/admin/", "/admin/n/shonen", "/admin/files/a/b.jpg"):
            status, headers, _ = self.call("GET", path)
            self.assertEqual(status, 303, path)
            self.assertTrue(headers.get("location", "").startswith("/__auth/login?next=/admin"), headers)
        self.assertEqual(self.stack.app_log, [], "no admin request may reach the app without a session")

    def test_admin_with_session_reaches_the_app_with_the_cookie(self):
        cookie = GOOD + "; other=1"
        status, _, _ = self.call("GET", "/admin", {"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertEqual([r["path"] for r in self.stack.app_log], ["/admin"])
        self.assertEqual(self.stack.app_log[0]["cookies"], [cookie],
                         "the app re-checks the session with costlab-auth and needs the same cookie")

    def test_admin_post_keeps_cookie_origin_and_body(self):
        status, _, _ = self.call("POST", "/admin/n/shonen/hide",
                                 {"Cookie": GOOD, "Origin": ORIGIN,
                                  "Content-Type": "application/x-www-form-urlencoded"}, b"back=top")
        self.assertEqual(status, 200)
        rec = self.stack.app_log[-1]
        self.assertEqual((rec["method"], rec["path"]), ("POST", "/admin/n/shonen/hide"))
        self.assertEqual(rec["cookies"], [GOOD])
        self.assertEqual(rec["headers"].get("origin"), ORIGIN)
        self.assertEqual(rec["body"], b"back=top")

    def test_login_pages_are_not_behind_the_login(self):
        status, _, body = self.call("GET", "/__auth/login?next=/admin")
        self.assertEqual((status, body), (200, b"auth:/__auth/login?next=/admin"))
        status, _, body = self.call("POST", "/__auth/login", {"Content-Type": "application/x-www-form-urlencoded"},
                                    b"username=a&password=b&next=/admin")
        self.assertEqual((status, body), (200, b"auth:/__auth/login"))
        self.assertEqual([r["path"] for r in self.stack.auth_log], ["/__auth/login?next=/admin", "/__auth/login"],
                         "the login page must not itself be sent through forward_auth")
        self.assertEqual(self.stack.app_log, [])

    def test_internal_is_not_reachable_from_outside(self):
        for path in ("/internal", "/internal/queue", "/internal/samples/shonen"):
            status, _, _ = self.call("GET", path)
            self.assertEqual(status, 404, path)
        self.assertEqual(self.stack.app_log, [])
        self.assertEqual(self.stack.auth_log, [])

    def test_public_paths_do_not_ask_for_login(self):
        paths = ("/", "/?lang=en", "/n/shonen?lang=ja", "/search?q=x", "/v1/tree", "/v1/styles/shonen", "/files/a/b.jpg",
                 "/static/site.css")
        for path in paths:
            status, _, _ = self.call("GET", path)
            self.assertEqual(status, 200, path)
        self.assertEqual(self.stack.auth_log, [], "public pages and the API never consult costlab-auth")
        self.assertEqual([r["path"] for r in self.stack.app_log], list(paths))


# ------------------------------------------------------------------------------ detection power
FORWARD_AUTH_RE = re.compile(r"\tforward_auth @admin costlab-auth:8000 \{\n(?:\t\t[^\n]*\n)*\t\}\n")

MUTATIONS = [
    ("copy_headers Cookie (Caddy 2.11+ strips the cookie)",
     lambda b: b.replace("\t\turi /__auth/verify\n", "\t\turi /__auth/verify\n\t\tcopy_headers Cookie\n")),
    ("cookie stripped before the app",
     lambda b: b.replace("\treverse_proxy manga-style:8080\n",
                         "\treverse_proxy manga-style:8080 {\n\t\theader_up -Cookie\n\t}\n")),
    ("forward_auth removed", lambda b: FORWARD_AUTH_RE.sub("", b)),
    ("forward_auth also over /__auth/*",
     lambda b: b.replace("\t@admin path /admin /admin/*\n", "\t@admin path /admin /admin/* /__auth/*\n")),
    ("/internal not blocked", lambda b: b.replace("\trespond @internal 404\n", "")),
]


def run_suite(caddyfile: Path) -> int:
    env = dict(os.environ, MANGA_CADDYFILE=str(caddyfile))
    return subprocess.run([sys.executable, __file__], env=env,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def power() -> int:
    if not CADDY:
        print("CADDY_BIN not set")
        return 1
    text = CADDYFILE.read_text(encoding="utf-8")
    block = site_block(text, HOST)
    failures = 0
    with tempfile.TemporaryDirectory(prefix="manga-caddy-power-") as tmp:
        for name, mutate in MUTATIONS:
            broken = mutate(block)
            if broken == block:
                print(f"NG   {name}: the mutation did not apply (the block changed shape)")
                failures += 1
                continue
            path = Path(tmp) / "Caddyfile"
            path.write_text(text.replace(block, broken), encoding="utf-8")
            code = run_suite(path)
            print(("ok   " if code else "NG   ") + f"{name}: " + (f"caught (exit {code})" if code else "NOT caught"))
            failures += 0 if code else 1
    print("all mutations were caught" if not failures else f"{failures} mutation(s) not caught")
    return 1 if failures else 0


def main() -> int:
    if "--power" in sys.argv:
        return power()
    if "--require" in sys.argv and not CADDY:
        print("CADDY_BIN is required", file=sys.stderr)
        return 1
    argv = [a for a in sys.argv if a != "--require"]
    result = unittest.main(argv=argv, exit=False, verbosity=2).result
    if result.skipped and "--require" in sys.argv:
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
