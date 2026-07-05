# ROADMAP.md — 3gpp-rag 完成度與階段規劃

> 由 Claude Fable 5 於 2026-07-05 交接前撰寫。搭配 `AGENTS.md`(協作協議)使用。
> 每個 R 階段動工前照 AGENTS.md §1 流程:brain 攤 plan → Hank 核准 → hands 實作 → brain review → Hank 拍板 commit。
> 完成一項就在本檔打勾並補一行結果(數字!),讓本檔持續是實況。

---

## A. 完成度評估(對照原始目標,2026-07-05)

原始目標:anchor doc(`../rag-3gpp-generic-anchor.md` 補充內容 4)的 Phase A 驗收 + 企劃書 vision。

| 面向 | 完成度 | 現況依據 |
|---|---|---|
| 資料層(schema / 雙 ingestion / anchor 正確性) | ~90% | 7 表+雙 FTS5;pdf+md 雙軌隔離已證;全量 38.521-1(3,221 節/5,643 chunks);多 spec 未擴 |
| 檢索(sparse/dense/RRF hybrid/rerank) | **100%** | hybrid hit@5 30/30;jina hit@1 26/30 ≥0.8 ✅(§6.2/6.3 index 量測) |
| 量尺/評測體系 | ~85% | 30 answerable + 12 OOS、hit@1/3/5/MRR、gate 混淆矩陣;缺 answer-eval;全量 index 重驗 = R0 |
| Evidence gate(拒答) | ~90% | refusal precision 100%;大 index 重校驗待(R0);5 題詞彙重疊 OOS 為現實上限(已誠實記載) |
| Generation(grounded + 引用) | ~85% | gate 防火牆雙重守;引用=provenance;**真 API 未煙測**(無 key) |
| UI(Streamlit) | ~80% | 查詢 MVP 可用(無 key 來源+gate;選配生成);citation/PDF-jump 未做 |
| **citation ≥0.9(Phase A 驗收)** | **未過:87%** | = hybrid-md hit@1 上限;R1 jina-on-md 是補齊路徑 |
| MCP server | N/A | 2026-07-03 觸發自評 <5 → parked(README 有紀錄;seam 已備) |
| compare(D1 世代對照)/ notes(D2 筆記) | 0% | 空 stub、DB 表已建;原 plan 明定後移 |
| Tailscale 異地存取 / beta tester | 0% | Phase A 收官最後兩項 |
| **總評** | 核心引擎 **~90% 可日用**;完整 vision **~60%** | |

---

## B. 階段規劃 R0–R8(建議順序;各項獨立可重排,依 Hank)

### ✅ R0 — Step 10 收尾(2026-07-05 由 Fable 5 完成)
- **結果**:facts 重抽 95,152 筆、孤兒 0;整合 review 0 P0/P1;313+45 測試綠。新 baseline(誠實記載,未調參):
  - `pdf_ab`:資料不動(SQL 證),統計漂移如預測 — sparse hit@1 22→19、**hybrid 22→23(MRR .85→.88)**、hit@5 全 30/30,GATE OK。
  - `md_ab`(全量 index):**hybrid hit@1 26→13、hit@5 27→22=73% GATE FAIL**;sparse 22→9。根因 = **量尺過時**:§6.2A–I/§6.3A–G 變體家族(CA/DC/SUL/UL-MIMO)與基礎條款共用詞彙,30 題是為窄 index 寫的、未指明「非 CA」,在全量 index 上題目本身歧義 → **R2 的急迫性有了數字**。
  - `gate_eval`:refusal precision 100→75%(出現 1 FP)、recall 17→25%、citation 45%(FAIL,= hit@1 崩的直接反映)、coverage 71% PASS。
  - `last_eval`(mixed):hybrid 20/27/29 GATE OK — **注意:是 pdf 子集(無變體家族)把分數撐住,不是 md 問題變小**;bge 依舊無增益(16/30)。
- **給 R1/R2 的含義**:R1 jina-on-md 在新 index 上的預期要下修(檢索天花板變低);**R2(題庫消歧義:指明 non-CA/單載波、或 expected_section 接受變體家族)是恢復量尺有效性的關鍵路徑,優先級高於 R1**。

### R1 — jina-on-md 長跑(citation ≥0.9 驗收判定)
- **目標**:Phase A 唯一未過的量化驗收。§6.2/6.3 時代 jina hit@1 26/30=87%;新 index 重跑定生死。
- **做法**:`evaluate.py --backend reranked --reranker jina --source-format tspec_md --report data/eval/jina_md_eval.md`,CPU 數小時 → 過夜獨立行程(AGENTS.md 陷阱 #1/#11)。
- **驗收**:citation(=hit@1)≥0.9 → Phase A 該項 PASS;不足則誠實記載差距與原因分析(別調參硬過)。
- **注意**:jina = Tier 1 only(license);跑完把「CPU 機日常 hybrid / 離線高精度 jina」的採用結論按新數字更新。

### R2 — 題庫世代交替(需 Hank 深度參與:審題)
- **目標**:量尺跟上全量 index。
- **做法**:① q39–q42 重標 answerable(加 expected_section/keywords,對 R18 md 文本驗證);② 對 §5/§6.4/§6.5/§7 新出題(照 Step 1 工作流:對原文出題→scope-validate→Hank 審題);③ 補 ≥4 個新 scope-boundary OOS(38.521-2 FR2 或 annex 外題材)。
- **牽動的 test lock**(改前先看):`test_answerable_count_unchanged`(鎖 30)、`test_oos_questions_well_formed`(≥4 scope_boundary)— 隨題庫版本一起改,commit 訊息記新分母。
- **驗收**:全部 scope-validated;新舊分母的 baseline 各自留檔(可比性)。

### R3 — LLM-judge answer-eval(Step 7 的 deferred 項)
- **目標**:量生成答案品質(正確性/引用忠實度/幻覺),補上「answer readiness」驗收。
- **做法**:新 `scripts/evaluate_answers.py`(不碰 evaluate.py);對 answerable 題跑 `generate_answer` → LLM judge 評分(正確/部分/錯誤 + 引用是否支持答案);需 ANTHROPIC_API_KEY,控制成本(題數 × 2 calls)。先真 API 煙測 1–2 題(至今未做過!)再全跑。
- **驗收**:answer 正確率、citation faithfulness 報表;結論寫入 Notion 研究與評估。

### R4 — 多 spec 擴充(語料 = 實用性的硬上限)
- **目標**:從單 spec 到多 spec。磁碟已有 50 檔(`spike/tspec_probe_out/3GPP-clean/`):38.521-1/2/3/4(R18)、36.521-1/2/3(R18 LTE)、38.331(R17 RRC)。
- **建議順序**:38.521-2(FR2,同族先驗跨 part)→ 36.521-1(**LTE — 翻 q31 hard-OOS、為 R5 世代對照備料**)→ 38.331(RRC,翻 q35)。每輪 = ingest → embed(過夜)→ 題庫補該 spec 題 → 重驗(含 spec_id filter 隔離證明)。
- **前置**:corpus 位置正式化決策(留 spike/ 或搬 data/raw/md/ — gitignored 皆可,R8);36 系列檔名/格式先 dry-run census(36.521-1 有 13 檔,格式可能有 38 系沒有的怪癖 — census 先行,比照 Step 10 N2)。
- **風險**:跨 spec section_number 重複是**正常**(UNIQUE 是 per-spec);evaluate subtree 已 per-source,但混 spec 查詢的 spec_id filter 要驗。

### R5 — compare / D1 世代對照(依賴 R4 的 LTE 語料)
- **目標**:NR↔LTE 條款映射 + 差異摘要(`cross_gen_mapping` 表已建)。原 plan D1(splendid-wand :292-298)。
- **做法**:brain 先攤設計(映射怎麼建:規則式條款號對齊 + 人工核可 vs LLM 輔助);MVP = 給定 NR 條款 → 找對應 LTE 條款 → 並排呈現。**先做 spike 量測可行性再進 src/**(本專案慣例)。
- **驗收**:10 組已知對應(如 NR 6.2.1 ↔ LTE 6.2.2)的映射正確率。

### R6 — notes / D2 個人筆記
- **目標**:個人筆記 CRUD + 掛進檢索(`personal_notes` 表已建;visibility 分級)。
- **做法**:src/notes/ CRUD → note 向量化進檢索混排(來源標示區分規範 vs 筆記)→ Streamlit 筆記面板。
- **驗收**:筆記可增改查、檢索結果正確標示來源層級。

### R7 — Tailscale + beta tester(Phase A 正式收官)
- **前置**:R1 過(citation gate)+ R0-R2 穩定。
- **做法**:Tailscale 起 Streamlit 異地存取(手機/平板可用)→ 邀 1–2 位同事(名單 Hank 定)→ 收集 `data/eval/tester_feedback/`。
- **驗收**(anchor doc :622-629):≥2/3 tester「會用」(NPS ≥7/10)。⚠ Tier 邊界:分享給同事前對照工作區 CLAUDE.md §5(Tier 3 = 只給容器不給資料;不確定就問 Hank)。

### R8 — 維運雜項(空檔做)
- config.yaml(§5.3 tier `data_source` switch — 等 Tier 2/3 真要動再做)
- 備份節奏(目前手動 backup.py;可排 Windows 工作排程器每日)
- corpus 位置正式化 + README 隨版更新
- `_heading_parser` 逗號 typo(`7.6A.4,1.1`,1 例)維持只記不修

---

## C. 分工建議(每階段通用)

| 工作 | 誰 |
|---|---|
| 攤 plan、風險分析、review、裁量 | Codex(brain) |
| 實作、測試、跑 benchmark、整理數字 | Opus 4.8(hands) |
| 出題審題、方向、commit 拍板、tier 判斷 | Hank |
| 長跑(embed/jina) | 獨立 OS 行程過夜,誰掛的誰驗收 |
