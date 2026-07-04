# 3GPP RAG

3GPP 規範資料保存與查詢系統 — 本地優先、漸進式建庫、可分級分享。

> **Status**(2026-06-14): Phase A Steps 0–8 完成 — 30 題 benchmark、RRF hybrid、jina/bge reranker、TSpec-md ingestion、evidence gate(拒答)、fact layer(scaffold)、LLM generation、Streamlit 查詢 MVP。現行 roadmap:全量建庫 → MCP server。

## 系統定位

把手上的 3GPP 規範文件(TS 36.521 LTE / TS 38.521 5G NR 等 PDF / docx)變成可以用自然語言查詢的本地知識庫,並能融入個人筆記、跨世代比較。差異化於 NotebookLM 之處在於:結構化世代差異引擎、來源精準引用、個人經驗分層、漸進式建庫(不暴力灌整份 PDF)。

## 兩個前端 / 同一份後端

- **Streamlit Web UI**(主):瀏覽器即可使用,可給同事 / 客戶 / 未來公開化
- **MCP Server**:**parked(2026-07-03,不建)** — 觸發自評 <5(隨手查 spec 的場景會用 NotebookLM,不花 Claude token)。日後要撿:重用 `src/generation` 的 `retrieve_and_gate` / `build_grounded_answer`,照 `../rag-3gpp-generic-anchor.md` :525-556 的 spec 建

兩者共用同一個介面中性的 RAG 後端(`src/retrieval/`、`src/generation/`)。

## 規劃文件

- 原始架構規劃:`../3gpp-splendid-wand.md`(工作區 root)
- 介面策略 + 正確性驗證的補充規劃:`../rag-3gpp-generic-anchor.md` — **「補充內容 4」(2026-05-16)為現行 source of truth**

## 快速使用(已建庫的機器)

```bash
# 瀏覽器查詢 UI:gate 徽章 + 來源面板不需 API key;勾「生成」才呼叫 LLM
.venv/Scripts/streamlit.exe run app/streamlit_app.py

# CLI 單題問答(生成需 .env 設 ANTHROPIC_API_KEY)
.venv/Scripts/python.exe scripts/answer.py --query "..." --source-format tspec_md

# 30 題 retrieval benchmark(sparse/dense/hybrid;--backend reranked 掛 reranker)
.venv/Scripts/python.exe scripts/evaluate.py --source-format tspec_md

# 每日備份:data/db/ → snapshots/YYYY-MM-DD.tar.gz
.venv/Scripts/python.exe scripts/backup.py
```

## 目錄結構(現況)

```
3gpp-rag/
├── data/
│   ├── raw/          # 原始 PDF (gitignored)
│   ├── db/           # SQLite + Chroma (gitignored)
│   └── eval/         # test bank (30 answerable + 12 OOS) + eval baselines
├── src/
│   ├── ingestion/    # PDF (PyMuPDF) + TSpec-LLM markdown 雙 adapter
│   ├── retrieval/    # sparse / dense / hybrid / rerank / evidence gate
│   ├── facts/        # rule-based fact 抽取(scaffold,parked)
│   ├── generation/   # LLM provider 抽象 + grounded answer
│   ├── compare/      # (stub) 世代對照
│   └── notes/        # (stub) 個人筆記
├── app/              # Streamlit 查詢 MVP
├── spike/            # 拋棄式腳本(不進主線)
├── scripts/          # ingest/embed/evaluate/answer/backup CLI
├── snapshots/        # backup.py 輸出 (gitignored)
└── pyproject.toml    # 設定集中在 src/config.py + .env(無 config.yaml)
```

## Setup on a new machine

Two scenarios — pick the one that matches your situation.

### Scenario A: new machine has internet (recommended)

```bash
# 1. Clone repo
git clone https://github.com/forsmileangel/3GPP-RAG.git wireless-consult/3gpp-rag
cd wireless-consult/3gpp-rag

# 2. Install Python 3.14+ if not present (uv can manage Python versions)
#    https://www.python.org/downloads/  or  winget install Python.Python.3.14

# 3. Install uv (Windows)
python -m pip install --user uv
# add %APPDATA%\Python\Python3XX\Scripts to PATH

# 4. Sync dependencies (creates .venv, installs everything from uv.lock)
uv sync

# 5. Restore secrets (NOT in git)
#    - Create .env from .env.example, fill in HF_TOKEN
#    - For HF_TOKEN: https://huggingface.co/settings/tokens (create read-only)
cp .env.example .env
# edit .env

# 6. Restore source PDFs (NOT in git — copyrighted)
#    Drop your TS 38.521-1 PDF into data/raw/
mkdir -p data/raw
# copy ts_138521-01_v17_05_00.pdf to data/raw/

# 7. Initialize the SQLite metadata DB (regenerates instantly)
uv run python scripts/init_db.py

# 8. Rebuild the index (BGE-M3 ~2.3 GB downloads on first run; needs HF_TOKEN)
#    PDF corpus:
uv run python scripts/ingest_toc.py && uv run python scripts/chunk_sections.py
#    TSpec markdown corpus (per spec, e.g. §6.2+6.3):
uv run python scripts/ingest_md.py --spec 38.521-1 --sections "6.2,6.3"
#    then embed whatever is un-embedded:
uv run python scripts/embed_chunks.py
```

### Scenario B: new machine has limited / no internet

Bring the whole `3gpp-rag/` folder via USB or cloud sync. Include:

| Item | Path | Size | Why |
|---|---|---|---|
| Source code + git history | everything except `.venv/` | small | so you can push back |
| `.env` | `.env` | tiny | has `HF_TOKEN` (gitignored) |
| Source PDFs | `data/raw/*.pdf` | MB–GB | gitignored, copyrighted |
| HuggingFace model cache | `~/.cache/huggingface/` (NOT in project!) | ~4 GB | so BGE-M3 doesn't re-download |
| Chroma vector DB | `data/db/chroma/` | tens–hundreds of MB | so embeddings don't re-run |
| Snapshots(或直接帶 `snapshots/*.tar.gz`) | `snapshots/` | ~15 MB+ | `scripts/backup.py` 的 data/db 打包,可替代逐檔複製 |

What you can skip (regeneratable on the new machine):
- `.venv/` — `uv sync` rebuilds from `uv.lock`
- `data/db/metadata.sqlite` — `scripts/init_db.py` recreates it
- `__pycache__/` directories

After copying:
```bash
cd 3gpp-rag
uv sync                                  # rebuild .venv from uv.lock (still needs internet for first time, OR pre-bundle wheels)
uv run python scripts/init_db.py
uv run python spike/quick_rag.py         # should hit all caches, run in seconds
```

If new machine has zero internet (most extreme case), pre-bundle wheels before unplugging:
```bash
# on the source machine while still online
uv pip download --dest vendor -r <(uv pip freeze)
# bring vendor/ along; on new machine:
uv pip install --no-index --find-links ./vendor -r requirements.txt
```

### Round-tripping

If you want to develop at home and push changes back:
```bash
# at home
git checkout -b home-work
# ... make changes ...
git push -u origin home-work
# back at office:
git fetch && git checkout home-work
```

## 設計紀律

1. **後端介面中性**:`src/retrieval/`、`src/generation/` 不依賴任何前端(Streamlit / MCP / CLI)
2. **正確性是 first-class**:`data/eval/test_questions.yaml` 跟程式碼同等重要
3. **絕不寫死絕對路徑**:所有路徑從環境變數(`.env`)讀,集中在 `src/config.py`
4. **拋棄式 vs 正式碼分清楚**:`spike/` 不進主 codebase

## 跨機器移植

詳見 `../3gpp-splendid-wand.md`(工作區 root)的「跨機器移植 / 公司擋權限的備案策略」段落;每日備份用 `scripts/backup.py`。

## License

(尚未決定 — 因含個人筆記,目前 repo 為 private)
