# AGENTS.md — 3gpp-rag AI 協作手冊

> 給接手本專案的 AI(Codex、Claude Opus/Sonnet、或其他)與未來的 Hank。
> 由 Claude Fable 5 於 2026-07-05 交接前撰寫(Fable 5 訂閱至 2026-07-07)。
> **本檔 = 協作協議與生存指南;`ROADMAP.md` = 接下來做什麼;兩檔一起讀。**

---

## 0. 這個專案是什麼(一句話)

evaluation-first 的 3GPP 規範本地 RAG:精確引用(§section/table/page)+ evidence gate 拒答 + 可回歸 benchmark,差異化於 NotebookLM 之處在「可驗證」而非「能聊天」。Tier 1 個人自用(license 議題已 close,見工作區 CLAUDE.md §5,**不要重提 NC 風險**)。

## 0.1 讀我順序(新 AI 上工第一件事)

1. 本檔(協議 + 陷阱)
2. `ROADMAP.md`(完成度 + 下一步 R0–R8)
3. 工作區 `../CLAUDE.md`(Hank 的合作協議 §4、三層揭露模型 §5、網路使用準則 §4.6 — **全部仍然有效**)
4. `~/.claude/plans/forsmileangel-3gpp-rag-crystalline-parnas.md`(歷史各 step 的完整計畫與決策,累積制、最新在上)
5. Claude auto-memory(`~/.claude/projects/D--My-project-wireless-consult/memory/`)— Claude 系 AI 適用
6. 真實狀態以 **git log + 實跑測試** 為準;文件若與實況矛盾,以實況為準並回頭修文件。

## 1. 角色與協作協議(2026-07-07 後)

| 角色 | 擔綱 | 職責 |
|---|---|---|
| **大腦(brain)** | Codex | 拆解任務、攤 plan 給 Hank、對實作做 fresh-context review、裁量技術取捨 |
| **手(hands)** | Claude Opus 4.8(或 Sonnet 5) | 依核准的 plan 實作、寫測試、跑 benchmark、回報結果 |
| **裁決者** | **Hank(永遠)** | 核准 plan、審題、拍板 commit/push、決定方向 |

**流程(§4.1 的雙 AI 適配版)— 任何「改 code」都走這條**:

```
brain 攤 plan(拆到 function 級)→ Hank 核准
    → hands 實作 + 測試(可先對 plan 提出質疑 — 見交互詰問)
    → brain 以 fresh context 獨立 review(P0/P1/P2)
    → 跑 test/benchmark gate
    → 彙整給 Hank → Hank 拍板才 commit
```

**交互詰問(cross-examination)規則**:
- hands 認為 plan 有錯:先陳述證據(file:line、實測輸出),不逕自偏離 plan;小偏差可做但必須在回報中標明「偏離點 + 理由」。
- brain review 與 hands 意見相左:各自把「主張 + 證據 + 若照對方做會發生什麼」寫成對照,**交 Hank 裁決**,不空轉互改。
- 兩邊都不可用「我覺得」當論據 — 本專案的文化是**跑給你看**(spike、dry-run、grep census)。

## 2. 鐵則(違反 = 事故)

1. **commit / push 只在 Hank 明示**。一次明示只覆蓋那一次。
2. **`spike/` 永不 commit**(gitignored 的拋棄式腳本與 corpus;staging 一律逐檔明列,不用 `git add -A`)。
3. **凍結檔與 byte-match**:`scripts/evaluate.py` 與 `data/eval/*.md` baseline 非該 step 明確授權不動;改動後必須證明「不帶新旗標跑 = 輸出與 committed baseline byte 相同」。已驗收模組(retrieval/gate/…)同理 — 加性優先。
4. **誠實量測**:新 index/新法 = 新 baseline,如實記載不調參美化;量測沒跑完不宣稱結果;失敗照實報(本專案 fact layer 就是量測後誠實 park 的先例)。
5. **介面中性**:`src/retrieval`、`src/generation` 永不 import streamlit/MCP/CLI;前端是後端的客戶。
6. **過時記憶揭露**(CLAUDE.md §4.6):用到可能 post-cutoff 的 SDK/API 寫法要標註並先驗證(anthropic SDK、MCP SDK、chromadb…)。網路掃描只在重大選型時做、由 Hank GO。
7. **溝通繁體中文**、避免過度 Python idiom(Hank 是 C 背景);**Notion 只放摘要**,本地 md 是 source of truth。
8. **每步各帶測試 gate**;獨立 review 抓到 P0/P1 先修再走。
9. Hank AFK(AskUserQuestion 60s 逾時)時:與已核准計畫一致且可回復的事可續行(先備份);**不可回復或超出核准範圍的事必須停等**。

## 3. 開發迴圈指令(Windows,repo root)

```powershell
# 測試(日常 gate;e2e 需要 corpus 在 spike/tspec_probe_out/)
.venv\Scripts\python.exe -m pytest tests -m "not e2e" -q
.venv\Scripts\python.exe -m pytest tests -q                    # 含 e2e
.venv\Scripts\ruff.exe check src scripts tests app

# 30 題 benchmark(混集合必帶 --source-format!)
.venv\Scripts\python.exe scripts\evaluate.py --source-format tspec_md --report data\eval\md_ab_eval.md
.venv\Scripts\python.exe scripts\evaluate.py --source-format pdf_pymupdf --report data\eval\pdf_ab_eval.md
# gate 評測(42 題含 OOS)
.venv\Scripts\python.exe scripts\evaluate.py --gate --gate-backend hybrid --gate-mode balanced --source-format tspec_md
# reranker 掛載:--backend reranked --reranker jina|bge(jina CPU 很慢,見陷阱 #11)

# 建庫(md 路徑)
.venv\Scripts\python.exe scripts\ingest_md.py --root spike\tspec_probe_out\3GPP-clean\Rel-18\38_series --spec 38.521-1 --version i00 [--sections "6.2,6.3"] [--force] [--dry-run]
.venv\Scripts\python.exe scripts\embed_chunks.py               # 撿 vector_id IS NULL
.venv\Scripts\python.exe scripts\extract_facts.py --spec 38.521-1 --source-format tspec_md

# 應用
.venv\Scripts\streamlit.exe run app\streamlit_app.py           # 無 key 可用來源+gate
.venv\Scripts\python.exe scripts\answer.py --query "..." --source-format tspec_md   # 生成需 .env ANTHROPIC_API_KEY

# 備份(改 DB 前必跑)
.venv\Scripts\python.exe scripts\backup.py                     # data/db -> snapshots/*.tar.gz
```

## 4. 架構地圖

```
corpus(spike/tspec_probe_out, gitignored;可用 .env HF_TOKEN 重下)
  └─ src/ingestion/  md_parser(discover/parse/emit,冪等 --force 連 Chroma 一起刪)
       ├─ _heading_parser  anchor 唯一真源(§編號;含 \_ band-combo 與小寫插入條款)
       ├─ _table_parser    三格式表格(grid/HTML/simple)
       ├─ _artifact_cleaner pandoc 清理(行號保持不變是合約)
       └─ chunker → embedder(BGE-M3 → Chroma "chunks" 單一 collection,pdf+md 共用)
  └─ SQLite data/db/metadata.sqlite:specs/sections/chunks(+chunks_fts)/facts(+facts_fts)/...
src/retrieval/   sparse(FTS5 BM25)/ dense / hybrid(RRF k=60)/ rerank(jina|bge)/ gate(拒答)
src/generation/  retrieve_and_gate → build_grounded_answer(gate=防火牆,REFUSE 不碰 LLM;引用=hits provenance)
src/facts/       rule-based 抽取(parked — 量測後結論:condition-disambiguation 牆,勿重啟 v3)
app/             Streamlit 薄前端(所有 st.* 在 main() 內)
scripts/         CLI 們;evaluate.py = 量尺(凍結級)
```

評分邏輯:expected_section 走 per-source subtree(parent 鏈);gate 只吃 query-agnostic 訊號(expected_* 是 eval oracle,**絕不進 runtime**)。

## 5. 血淚陷阱清單(繼任者最值錢的一節)

1. **embed_chunks 是單一 SQL 交易**:中斷 = 全部重來(Chroma upsert 冪等所以重跑安全,但白費)。長跑用獨立 OS 行程(session 背景任務曾被 harness 中止)。
2. **`--force` 的 Chroma 刪除在 SQL 交易之外**:emit 失敗 → 向量已刪、SQL 回滾 → vector_id 掛著但向量沒了。**改 DB 前必跑 backup.py**(此風險已實際發生過一次,靠全量重嵌自癒)。
3. **`sections` 有 `UNIQUE(spec_id, section_number)`**:語料真有重複條款號 → `_merge_duplicate_sections` 併入首現+warning。**SQLite FK enforcement 是關的**(無 PRAGMA)→ facts 刪除不會 cascade,重抽 facts 用 `extract_facts.py`(按 spec_id 刪能清孤兒)。
4. **anchor 截斷 bug 的教訓**:3GPP 條款號有 `\_` band-combination(`6.2D.1\_1.1`)與小寫插入條款(`6.4.2.1a`)兩族;regex 改動前先 census 全 corpus,byte-match 前提要「結構性」證明不是只靠測試綠。
5. **PowerShell 陷阱**:`Select-String` 預設**不分大小寫**(曾令 census 失真 — 大小寫敏感要 `-CaseSensitive`);native exe 的 stderr 會包成 NativeCommandError 假警報(exit code 才是真相);`uv` 不在 PATH,用 `py -m uv`。
6. **評測混集合**:Chroma 是 pdf+md 單一 collection,evaluate 不帶 `--source-format` 會混源;`last_eval.md`/`jina_eval.md` 是混跑(歷史產物,參考價值最低)。
7. **gate 閾值 index-sensitive**:config 註解記載校準日期與題庫規模;index 大小變要重驗(coverage-dominant 權重的由來:窄 index 上 RRF top_score 飽和)。answer_floor 距最弱 answerable 只 ~0.03。
8. **R17 vs R18**:題庫 scope-validation 讀的是 **R17 PDF**(data/raw),md corpus 是 **R18 i00** — 同 spec 名不同版本,出新題要對 md 文本驗證漂移。
9. **page=0 哨兵**:md 無頁碼,page=0 表「無頁」;UI/引用格式化都據此略過 p.0,不要「修好它」。
10. **sparse `_TOKEN_RE` 不含 `_`**:使用者直接查「6.2D.1_1」會被切開 — 已知限制,非 bug。
11. **jina-reranker-v3**:CC BY-NC 4.0 = **Tier 1 個人用 only**(Tier 2/3 用 bge/Apache);CPU 上 ~3.3s/doc,整輪 30 題數小時 — 排過夜。revision 已 pin(供應鏈+重現性)。
12. **q39–q42 的 OOS 標籤已過時**(全量 index 後 §6.4/6.5 in-scope)— gate 混淆矩陣把它們算 FN 是已知假警報,重標排在 ROADMAP R2(牽動兩個 test lock,需 Hank 審題)。
13. **fact layer 是 parked 不是半成品**:2026-06-13 量測結論(瓶頸=BM25 挑不出同參數多 cell 的正確條件格,非抽取、非 LLM)。別「順手完成它」。
14. **模型/日期**:系統時鐘與文件日期偶有漂移,新紀錄以當下系統日期為準,別回改舊標記。

## 6. 交接時點狀態(2026-07-05)

- **HEAD `c5db8f0`**(origin 同步)= Steps 0–9 完成:30 題量尺、RRF hybrid(30/30)、jina reranker(26/30)、md_parser、evidence gate(precision 100%)、fact scaffold(parked)、generation、Streamlit MVP、收尾同步。
- **Step 10 進行中(工作樹有未 commit 變更)**:anchor 修復(N1+N1b)+ 全量 38.521-1 建庫(3,221 sections / 5,643 chunks 全嵌入)已完成;**剩 N5(facts 重抽)→ N6(三評測新 baseline)→ N7(整合 review + commit)** — 即 `ROADMAP.md` 的 R0。
- MCP server:2026-07-03 照觸發規則取消(parked),seam 已備。
- `.env` 無 ANTHROPIC_API_KEY → 生成路徑只過 fake-provider 測試,真 API 煙測未做。

## 7. 外部資源

- GitHub:`forsmileangel/3GPP-RAG`(private)
- Notion 主頁:https://www.notion.so/352fec73b1638106b6d2f519e4ce0a41(摘要+入口;子頁 4「研究與評估」收評測紀錄;「fable 5 對這個資料庫的規劃」= 本交接的 Notion 版)
- corpus 重下:HuggingFace TSpec-LLM(.env 有 HF_TOKEN;50 檔清單見 ROADMAP R4)
