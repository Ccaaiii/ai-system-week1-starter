# Week 4 Baseline Report v1.0

學號：7114029039  
姓名：蔡忻辰  
專題名稱：PQC × IoT / Embedded / Product Security  
資料與執行版本：2026-10-06，使用 Week 3 的 Scenario / Evidence v0.1

## 1. Task & Dataset

本週延續 Week 2 的題目：根據 IoT 或嵌入式裝置的硬體條件和安全需求，從現有的 PQC 技術資料中找出值得進一步測試的候選方案。這不是要直接預測「唯一最好的演算法」，而是做候選方案的 **Retrieval + Ranking**，讓研究者先縮小後續要實作的範圍。

- **Unit：** 一筆 PQC deployment scenario。
- **Input：** `device_platform`、`cpu_architecture`、`available_ram_bytes`、`available_flash_bytes`、`crypto_function`、`required_security_category`、`application_scenario`。
- **Target：** 經人工確認、符合部署情境的 PQC candidate set。
- **Output：** 最多五個候選的 `parameter_set`，以及支持判斷的 Evidence record。
- **Dataset Spec：** `week03_dataset_spec.md` v0.2；實際 CSV 為 `pqc_scenario_dataset_v0.1.csv`（12 筆）和 `pqc_evidence_corpus_v0.1.csv`（18 筆）。
- **Coverage：** 兩個 `device_platform`，CPU architecture 都為 ARM Cortex-M4；Evidence 包含 ML-KEM、ML-DSA 的多種參數與 implementation。

原本 W3 決定以 `device_platform` 做 **Group Split**，希望 test set 是訓練時沒看過的硬體平台。但現在只有兩個 group，沒辦法合理分出互不重複的 train、validation、test 三組。因此 W4 先讓所有方法在**同一組 12 筆 Scenario** 做 *prototype comparison*，**不是正式的泛化測試**。本週沒有模型訓練，所以沒有假設 train/test 比例，也沒有臨時改用 random split。

另外，12 筆 `label_status` 全是 `needs_human_review`；`weak_label_candidates` 只是先前依照規則建立的候選清單，不是專家確認過的 Ground Truth。這會限制本週對 Recall@5 的解讀。

## 2. Baseline Plan

Week 2 已經提出 Manual Search 和 Rule-based Filtering。這週我保留人工搜尋當作原本流程的比較對象，但**目前沒有實際人工搜尋的計時與逐筆答案**，所以不把它寫成已經完成的實驗。

為了先有可重現的比較，我另外實作兩個很簡單的 reference，加上 Week 2 規劃的 Rule-based Filtering，共三個可執行的方法：

| Role | Method | 做法 | 預期弱點 |
| --- | --- | --- | --- |
| Naive reference | Naive Function-only | 只依 KEM / Digital Signature 找出相同功能的參數集合，最多列五個 | 沒檢查要求的安全等級，可能列出不能接受的候選 |
| Simple reference | Top-1 Secure | 先確認安全等級、CPU、基本 RAM / Flash 證據，再只保留 operation cycles 最少的候選一個 | 可能漏掉其他同樣符合條件、值得比較的方案 |
| **Credible baseline** | **Rule-based Filtering** | 同時檢查密碼功能、安全等級、CPU architecture、可用資源證據，保留最多五個候選 | 只能處理已知欄位；不代表完整部署可行性或最佳排序 |

我認為 Rule-based Filtering 是合理的 credible baseline，因為安全等級和密碼功能是清楚的硬性條件。先使用這些規則，比直接使用 LLM 更容易確認每個候選為什麼被保留或排除。

**Baseline 出處：** Manual Search 與 Rule-based Filtering 來自我的 W2 `week02_ai_problem_spec.md`；兩個 naive reference 是 W4 為了能實際量測差異而新增的簡單對照方法，不是聲稱它們原本就在 W2 中，也不是把課程 Week 1 的客服分類程式當成 PQC 的結果。

## 3. Fair Comparison & Experiment Spec

| 項目 | 固定設定 |
| --- | --- |
| Dataset | Scenario v0.1（12 rows）+ Evidence v0.1（18 rows） |
| Split | 本週為 prototype comparison；W3 規劃的 Group Split 暫緩 |
| Evaluation unit | 一筆 Scenario；三個方法使用相同 12 筆 |
| Information boundary | 各方法取得相同的部署條件與同一份 Evidence Corpus，可自行選擇是否使用全部條件 |
| 禁止當作 Input | `weak_label_candidates`、`label_source`、`label_status` |
| Primary Metric | Recall@5（正式數值待人工 Ground Truth）；本週另列 *weak-label diagnostic Recall@5* |
| Failure-oriented Metric | Security Level Violation Rate；另記錄 Cryptographic Function Mismatch |
| Threshold policy | N/A，直接依條件篩選並輸出至多五個候選 |
| Random seed | N/A，三個方法都沒有隨機性 |
| Runtime / Cost | 同一個 Python 環境、同一段資料；量測 101 次全資料運算的每 Scenario 中位時間，僅供參考 |

本週的 Recall@5 定義為：每一筆 Scenario 的前五名預測中，找到多少人工確認的相關候選，最後取所有 Scenario 平均。但目前人工 Ground Truth 尚未建立，因此**正式 Recall@5 = N/A**。表中能計算的是和既有 *weak label* 比對的診斷數值，不能拿去宣稱部署準確率。

Security Level Violation Rate 的算法是：**輸出候選中，`security_category` 低於 Scenario 要求的候選數量 / 全部輸出候選數量**。我的目標是 0%，因為安全等級不足會直接影響後續決策。

Rule-based 的 RAM / Flash 判斷只使用現有 benchmark 的 peak stack（`keygen_stack_bytes`、`operation_1_stack_bytes`、`operation_2_stack_bytes` 的最大值）和 `code_size_total_bytes`，並要求有至少一種 implementation 符合目前 CPU 類型。**peak stack 不等於完整 RAM 消耗，code size 也不等於整體 Flash 需求**，因此通過只能視為基本證據，不能宣稱真正部署一定成功。程式使用同一個 Evidence record 的 `operation_1_cycles_mean` 做固定排序，不把跨硬體的 cycles 拿來直接比較。

## 4. Results

我使用實際的兩份 CSV 執行三種方法，得到：

| Method | Weak-label Recall@5（診斷值） | Security Violation | Function Mismatch | 輸出候選總數 |
| --- | ---: | ---: | ---: | ---: |
| Naive Function-only | **1.0000** | **12 / 36 = 33.33%** | 0 | 36 |
| Top-1 Secure | **0.6111** | **0 / 12 = 0%** | 0 | 12 |
| **Rule-based Filtering** | **1.0000** | **0 / 24 = 0%** | **0** | **24** |

完整逐筆輸出在 `outputs/week04_predictions.csv`，摘要在 `outputs/week04_results.csv`。程式也會寫出實際的每 Scenario 運行時間，這些時間只包括本機運算，不包括人員查資料、理解結果或最後人工確認的成本，不能直接拿來當 Manual Search 的時間。

**我的解讀：**

Naive Function-only 雖然和 weak labels 的 Recall@5 一樣達到 1.0，但它把一些不符合安全等級的候選也放進來了，因此不適合作為實際的部署篩選方式。單靠 Recall@5 確實看不出這類問題。

Top-1 Secure 沒有安全等級違反，但每筆只留下單一候選；當某個 Scenario 原本有兩到三個符合條件的候選時，就無法讓研究者看到其他可以比較的方案。

Rule-based Filtering 在這 12 筆 prototype 上可以排除 security category 不足的候選，同時保留現有 weak labels 列出的候選集合。但這**不代表真正達到正式 Recall@5 = 1.0**：因為 W3 的 weak labels 本來就是按相近的規則建立，拿它評估 rule-based 很容易形成循環驗證。至於模型面對全新硬體是否還有相同表現，目前也不能下結論。

另外，現有 Scenario 的 RAM / Flash 數值都沒有在這次資料中額外排除候選；Rule-based 的改進主要來自安全等級檢查，而不是已經證明它處理記憶體限制的能力有多好。

## 5. Failure Analysis

這三筆來自**實際執行的 Baseline 輸出**。我把能直接確認的硬性條件違反，和只能透過 weak label 觀察到的候選遺漏分開寫，避免把尚未人工審核的答案當成 Ground Truth。

### Case 1 — S003：KEM 的安全等級不符

- **Unit：** S003，NUCLEO-L4R5ZI；KEM；Required Security Category = 5。
- **Naive Prediction：** ML-KEM-512、ML-KEM-768、ML-KEM-1024。
- **可確認的問題：** ML-KEM-512 的 Category 是 1，ML-KEM-768 是 3，都低於要求的 5；只有 ML-KEM-1024 符合安全等級。
- **原因：** Naive 方法只看 KEM 的功能類別，完全沒判斷 Security Category。
- **影響：** 不符合安全等級的演算法可能被放入下一階段實作名單。
- **Rule-based 結果：** 只保留 ML-KEM-1024。

### Case 2 — S011：Digital Signature 的安全等級不符

- **Unit：** S011，STM32F4 Discovery；Digital Signature；Required Security Category = 3。
- **Naive Prediction：** ML-DSA-44、ML-DSA-65、ML-DSA-87。
- **可確認的問題：** ML-DSA-44 的 Category = 2，低於要求的 3；ML-DSA-65 和 ML-DSA-87 分別為 3、5。
- **原因：** 同樣沒有檢查安全等級，但這次發生在數位簽章的部署需求上。
- **影響：** 若研究者沒有再確認，可能採用安全等級不符合需求的參數。
- **Rule-based 結果：** 保留 ML-DSA-65 和 ML-DSA-87。

### Case 3 — S001：Top-1 遺漏可比較的候選

- **Unit：** S001，NUCLEO-L4R5ZI；KEM；Required Security Category = 1。
- **Top-1 Secure Prediction：** ML-KEM-512。
- **Weak-label 參考集合：** ML-KEM-512、ML-KEM-768、ML-KEM-1024。
- **觀察到的差異：** Top-1 只保留單一候選，因此沒有列出 ML-KEM-768、ML-KEM-1024。
- **可能原因：** 方法為了追求簡單，只選第一個符合要求且 operation cycles 較低的候選。
- **影響：** 研究者沒有看到其他安全等級與效能可能不同的選項。
- **限制：** 目前只能說「相對 weak label 有遺漏」，因為三個候選是否全都值得實際測試，仍需要人工 Ground Truth 確認。

三筆錯誤的逐筆表格存放在 `outputs/week04_failure_cases.csv`。前兩筆是可以直接用資料中的 Security Category 驗證的違規，第三筆是依 weak label 得到的診斷性漏列，**不是已確認的正式 False Negative**。

另外，W3 Audit 已指出 bandwidth、latency、power、threat model 全部缺少資料，Evidence 也只涵蓋 ARM Cortex-M4。這些是目前真正的系統風險，但我沒有把它們假裝成這次實驗已經發生的錯誤預測。

## 6. Minimum Sufficient Solution

就目前這份 Dataset 和能驗證的條件而言，我會暫時選 **Rule-based Filtering + Human Review**。

原因不是「它已經百分之百正確」，而是它至少能用明確的規則排除安全等級不符合需求的候選，而且可以保留更多需要研究者比較的方案。加上它的判斷條件清楚，出現問題時容易回頭檢查是哪一條規則或哪一筆 Evidence 有問題。

但我還不能把它說成已通過正式驗收。現在沒有人工確認的 Ground Truth，沒有測到全新的硬體平台，也沒有完整的 bandwidth / latency / power 證據。這些限制還沒補齊前，最終選擇還是要人工確認。

目前**不需要直接升級 LLM 或更複雜的 AI 方法**，因為最明顯的問題在資料完整度與可驗證性，還沒有證據顯示較複雜模型能真正解決它們。

## 7. Solution Choice Note

**Current evidence：** 在同樣的 12 筆 Scenario 和 18 筆 Evidence 上，Naive Function-only 有 12 / 36 個安全等級違反；Top-1 Secure 沒有安全等級違反，但 weak-label Recall@5 只有 0.6111；Rule-based Filtering 沒有已知 Security Category 或 Function mismatch，且保留 weak labels 列出的全部候選。以上的 recall 都只是診斷性比較。

**Remaining failure / limitation：** 尚無人工 Ground Truth；Group Split 尚不能做；缺少 bandwidth、latency、power 和 threat model；不同 platform 的 benchmark coverage 不夠；候選 ranking 仍然只是一種簡單的固定排序。

**Minimum Sufficient Solution：** 先使用 Rule-based Filtering + Human Review，暫時不讓系統自行決定最後要部署哪個 PQC 參數。

**是否需要更複雜方法：** 現在不需要。複雜度會增加模型建置、維護與結果解釋的成本，但目前沒有證據顯示它能改善主要問題。

**Next Candidate：** 先補完 Ground Truth、加入新的 CPU / hardware platform，再測試 **Rule-based pre-filter + BM25 / Keyword-based ranking**。若未來 Evidence 擴充到有技術文件文字、實作說明與 application context，這種 ranking 才有機會改善同時符合硬性條件時的優先順序。現有 Corpus 主要是結構化 benchmark 欄位，所以現在還不適合宣稱 BM25 一定有幫助。

## 8. Reproducibility / Run Record

- **Scenario：** `data/pqc_scenario_dataset_v0.1.csv`
- **Evidence：** `data/pqc_evidence_corpus_v0.1.csv`
- **Notebook：** `notebooks/week04_baseline.ipynb`
- **可重現實作：** `src/week04_pqc_baselines.py`
- **Results：** `outputs/week04_results.csv`
- **Predictions：** `outputs/week04_predictions.csv`
- **Failure cases：** `outputs/week04_failure_cases.csv`
- **Missing manual record：** `outputs/week04_manual_search_record_template.csv`
- **Ground Truth review：** `outputs/week04_ground_truth_review_template.csv`
- **No random seed：** 不使用隨機模型或隨機切分。
- **Split：** 原規劃 Group Split by `device_platform`，本週因只有兩個 groups 而暫緩。
- **Original W2 manual-search baseline：** 目前未有人工逐筆搜尋紀錄與時間量測，不能填寫其成績或宣稱它已完成。
- **Commit message 建議：** `Complete Week 4 PQC baseline prototype and evidence`。

## 9. Mini Defense

### Q1. 為什麼你的 Baseline 合理？Baseline 出處是什麼？

我的題目是從 PQC Evidence 裡找適合部署需求的候選方案。Week 2 原本就有定義 Manual Search 和 Rule-based Filtering：人工搜尋代表研究者現在會做的工作，而 Rule-based Filtering 則是把密碼功能、安全等級和硬體限制轉成明確的篩選規則，所以是合理的簡單方法。這週因為還沒有人工計時資料，我先加了 Function-only 和 Top-1 兩個可執行的 reference 來比較。它們的限制也有明確說出來，沒有把它們當作正式的人工搜尋結果。

### Q2. 複雜模型多出的效益集中在哪些案例？

這週沒有測更複雜的 AI 模型，所以不能說它已經有提升。我有看到 Rule-based 相較 Function-only 的改善，主要是在 Security Category 不符合需求的案例；跟 Top-1 比較，則是可以保留更多符合條件的候選。至於 LLM 或語意排序是不是能處理多個候選都符合條件的情況，還要有更多文字 Evidence 和正式 Ground Truth 才能測。

### Q3. 如果複雜模型只提升 1–2%，你還會選它嗎？

我不會只看平均分數增加 1–2% 就選。如果改善的是一般案例，但運算、資料維護和人工確認成本增加很多，我覺得不一定值得。不過，如果改善真的發生在安全等級錯配、重要候選漏列這些會影響部署決策的問題，就值得再評估。但前提是先用獨立 Ground Truth 證明改善是真的，而不是只跟規則產生的 weak label 比對。

---

### 提交前仍需完成的事項

這份是**已完成資料驅動 baseline prototype 的報告**。正式繳交若要求「經驗證的 Recall@5」及「三筆相對人工 Ground Truth 的錯誤」，仍需要先人工確認 12 筆 Ground Truth；原 W2 的 Manual Search 也還沒有執行紀錄。不能把現有 weak-label agreement 冒充成正式模型效能。
