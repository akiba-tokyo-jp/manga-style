# manga-style: マンガの絵柄カタログ（manga.akiba.tokyo.jp）。公開ページ・Genko 向けの読み取り API・管理画面。
# build context は costlab-auth/manga。costlab-auth の image / .env / 鍵とは共用しない。
# ★ 秘密は image に入れない。管理画面の認証は costlab-auth（Caddy の forward_auth と、app 側の再確認）。
# Python 3.12.15 に固定（2026-10-21）。`3.12-slim` のままだと VPS に残った古いイメージ（3.12.13）で
# ビルドされ続ける（deploy は build に --pull を付けない）。版を書けば無い版を取りに行く。
FROM python:3.12.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /srv/manga

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 空の named volume は初回 mount 時にこの所有者・0700 を引き継ぐ。
RUN groupadd --system --gid 10002 manga \
 && useradd --system --uid 10002 --gid 10002 --no-create-home \
      --home-dir /nonexistent --shell /usr/sbin/nologin manga \
 && install -d -o 10002 -g 10002 -m 0700 /data

# 同じプロンプトを別のモデルで描いた比較の絵（records.json は git、files/ は tools/manga_catalog/prepare_compare.py が置く）。
# ★ app/ より先に置く: 約 2,700 枚あり、app の変更のたびに層を作り直さないため（中身が同じなら cache が効く）。
COPY compare/ ./compare/
COPY app/ ./app/

USER 10002:10002
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=20s --retries=3 \
  CMD ["python", "-c", "import sys,urllib.request\ntry:\n r=urllib.request.urlopen('http://127.0.0.1:8080/healthz',timeout=2)\n sys.exit(0 if r.status==200 else 1)\nexcept Exception:\n sys.exit(1)"]

# ★ 単一 worker（状態はメモリと /data/state.json。worker を増やすと食い違う）。
# ★ --no-proxy-headers: /internal/* は「コンテナ内の 127.0.0.1 から」だけを通すので、
#   X-Forwarded-For で送り元を書き換えさせない。
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", \
     "--workers", "1", "--no-proxy-headers", "--no-server-header"]
