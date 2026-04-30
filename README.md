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

## Setup(待 Phase 0 完成後補完整步驟)

```bash
# 預備:這個 repo 假設你已 clone 到 wireless-consult/3gpp-rag/
cd wireless-consult/3gpp-rag

# 安裝依賴(uv)
uv sync

# 設定環境變數
cp .env.example .env
# 編輯 .env,填入 API key

# 跑 Phase 0 spike
python spike/quick_rag.py
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
