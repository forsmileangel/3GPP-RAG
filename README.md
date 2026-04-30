# 3GPP RAG

3GPP 規範資料保存與查詢系統 — 本地優先、漸進式建庫、可分級分享。

> **Status**: Phase 0 (spike + reality check) — 尚未進入正式開發

## 系統定位

把手上的 3GPP 規範文件(TS 36.521 LTE / TS 38.521 5G NR 等 PDF / docx)變成可以用自然語言查詢的本地知識庫,並能融入個人筆記、跨世代比較。差異化於 NotebookLM 之處在於:結構化世代差異引擎、來源精準引用、個人經驗分層、漸進式建庫(不暴力灌整份 PDF)。

## 兩個前端 / 同一份後端

- **Streamlit Web UI**(主):瀏覽器即可使用,可給同事 / 客戶 / 未來公開化
- **MCP Server**(後置可選):讓 Claude Code 內問 3GPP 問題時自動接 RAG

兩者共用同一個介面中性的 RAG 後端(`src/retrieval/`、`src/generation/`)。

## 規劃文件

- 原始架構規劃:`~/.claude/plans/3gpp-splendid-wand.md`
- 介面策略 + 正確性驗證的補充規劃:`~/.claude/plans/rag-3gpp-generic-anchor.md`

## 目錄結構(規劃中,實際隨開發演進)

```
3gpp-rag/
├── data/
│   ├── raw/          # 原始 PDF / docx (gitignored)
│   ├── processed/    # 解析後 JSON (gitignored)
│   ├── db/           # SQLite + Chroma (gitignored)
│   └── eval/         # test Q&A bank + tester feedback
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   └── ...
├── app/              # Streamlit
├── spike/            # Phase 0 拋棄式腳本
├── scripts/          # evaluate.py, backup.sh 等
├── pyproject.toml
└── config.yaml
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

# 8. Re-run Phase 0 spike to repopulate Chroma vector cache
#    (BGE-M3 ~2.3 GB downloads on first run; needs HF_TOKEN)
uv run python spike/quick_rag.py
```

### Scenario B: new machine has limited / no internet

Bring the whole `3gpp-rag/` folder via USB or cloud sync. Include:

| Item | Path | Size | Why |
|---|---|---|---|
| Source code + git history | everything except `.venv/` | small | so you can push back |
| `.env` | `.env` | tiny | has `HF_TOKEN` (gitignored) |
| Source PDFs | `data/raw/*.pdf` | MB–GB | gitignored, copyrighted |
| HuggingFace model cache | `~/.cache/huggingface/` (NOT in project!) | ~4 GB | so BGE-M3 doesn't re-download |
| Chroma vector DB | `data/db/chroma_spike/` | hundreds of MB | so embeddings don't re-run |
| Spike outputs | `spike/extracted.json`, `spike/last_run.json` | small | optional, just runtime working files |

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
3. **絕不寫死絕對路徑**:所有路徑從 `config.yaml` 或環境變數讀
4. **拋棄式 vs 正式碼分清楚**:`spike/` 不進主 codebase

## 跨機器移植

詳見 `~/.claude/plans/3gpp-splendid-wand.md` 的「跨機器移植 / 公司擋權限的備案策略」段落。

## License

(尚未決定 — 因含個人筆記,目前 repo 為 private)
