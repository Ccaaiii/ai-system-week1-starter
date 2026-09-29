# Week 3 - Dataset Audit Summary

學號：7114029039    
姓名：蔡忻辰
專題名稱：PQC × IoT / Embedded / Product Security

## Dataset Overview

Scenario Dataset

- Rows：12
- Exact Duplicate：0
- scenario_id 重複：0
- Hardware Platform：2 種
- CPU Architecture：1 種

Evidence Corpus

- Rows：18
- Exact Duplicate：0
- record_id 重複：0
- Algorithm Family：ML-KEM、ML-DSA

## Finding 1：Optional Input Coverage 不足

Problem

Week 2 有定義 bandwidth、latency、power 和 threat model，但目前 Dataset 沒有這些資料。

Evidence

- bandwidth_limit_kbps：12 / 12 missing
- max_latency_ms：12 / 12 missing
- power_limit_mw：12 / 12 missing
- threat_model：12 / 12 missing

這四個欄位 Missing Rate 都是 100%。

Impact

目前 Dataset 可以用來檢查 CPU、RAM、Flash、cryptographic function 和 Security Category。

但是還不能完整測試 bandwidth、latency、energy 或 threat model 相關的 deployment constraint。

Decision

目前先保留這些欄位，不自行填入假資料。

後續如果找到有提供 network、latency、power 或 threat model 資訊的 benchmark 或 paper，再加入 Dataset。

## Finding 2：目前不能直接使用 Random Split

Problem

我的 Test set 希望模擬新的 hardware platform。

如果直接使用 Random Split，同一個 platform 很可能同時出現在 Train 和 Test。

Evidence

目前只有 2 個 device platform。

每一個 platform 都有 6 筆 Scenario。

CPU architecture 則全部都是 ARM Cortex-M4。

Impact

如果同一個 platform 同時出現在 Train 和 Test，系統可能只是記住類似的硬體條件，而不是真的可以泛化到新的 hardware platform。

這可能讓 Test 結果看起來比實際情況更好。

Decision

之後使用 Group Split，並以 device_platform 作為 Group。

但目前只有 2 個 Group，所以現在先不硬做 Train、Validation、Test 三組。

之後增加更多 platform 後再進行正式 Split。

## Finding 3：Label 還不是正式 Ground Truth

Problem

目前 weak_label_candidates 是透過規則建立的 candidate，不是研究者逐筆人工確認的答案。

Evidence

12 / 12 Scenario 的 label_status 都是 needs_human_review。

也就是目前 100% 的 Label 都還需要人工確認。

Impact

目前不適合直接使用這些 Label 計算 Week 2 設定的 Recall@5 或 Top-3 Hit Rate。

如果直接這樣做，等於把規則產生的 weak label 當成真正 Ground Truth。

Decision

目前 weak label 只作為 Dataset prototype。

正式進行模型評估以前，需要由研究者逐筆確認 relevant candidate。

## Finding 4：Hardware Coverage 太集中

Problem

目前 Dataset 的 hardware coverage 不夠廣。

Evidence

目前只有 2 個 hardware platform。

CPU architecture 只有 ARM Cortex-M4。

目前整理的 PQC algorithm 也只有 ML-KEM 和 ML-DSA。

Impact

目前結果不能直接代表 ESP32、RISC-V、Cortex-M33 或其他 MCU。

也不能直接宣稱目前方法可以泛化到所有 IoT 或 Embedded 裝置。

Decision

將這個問題列入 Known Limitation。

後續再加入不同 hardware platform 和 CPU architecture，之後重新做 Dataset Audit。

## Finding 5：目前沒有 Exact Duplicate

Problem

檢查 Dataset 是否有完全相同的重複資料。

Evidence

Scenario Dataset exact duplicate = 0。

Evidence Corpus exact duplicate = 0。

Impact

目前沒有發現完全重複的資料造成樣本被重複計算。

但是同一 platform 或同一 algorithm 的不同 implementation 還是可能高度相關。

Decision

目前不需要因為 exact duplicate 刪除資料。

不過之後進行 Split 時，還是需要另外確認 platform、source 和 implementation 是否跨 Train 和 Test。

## Overall Decision

目前這份 Dataset 已經可以用來完成 Week 3 的 Dataset Audit。

但是目前還不適合直接拿來做完整的模型訓練與正式評估。

目前最需要補強的部分是：

1. 增加不同 hardware platform
2. 增加不同 CPU architecture
3. 人工確認 weak label
4. 補 bandwidth、latency、power 和 threat model
5. 補完整的時間與版本資訊
6. 資料增加後再重新做正式 Group Split