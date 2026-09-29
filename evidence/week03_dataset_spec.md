專題名稱：PQC × IoT / Embedded / Product Security
姓名：蔡忻辰
學號：7114029039

一、Source / Owner
我的資料不是直接使用一份現成的 PQC Dataset，而是從 PQC 標準文件和嵌入式裝置的 benchmark 資料整理出來。
目前主要使用的來源有：
NIST FIPS 203，主要提供 ML-KEM 的標準、參數和安全等級。
NIST FIPS 204，主要提供 ML-DSA 的標準、參數和安全等級。
pqm4 benchmark，主要提供 ARM Cortex-M4 上執行 PQC 演算法時的速度、記憶體使用量和程式大小等資料。
我目前把資料分成兩部分。
第一部分是 Scenario Dataset，用來表示一個 IoT 或 Embedded 裝置實際使用 PQC 的情境。
第二部分是 Evidence Corpus，用來存放不同 PQC 演算法的 benchmark 和標準資料。
目前這份 Dataset 是作業用的 prototype，之後如果真的拿來做論文，還需要加入更多硬體平台和其他來源的 benchmark。

二、Unit Alignment
承接 Week 2 的 AI Problem Spec，我的 Unit 是一個 PQC deployment scenario。
也就是一筆資料代表一個 IoT 或 Embedded 裝置在特定硬體和安全需求下，需要選擇 PQC 演算法的情境。
目前 Scenario Dataset 有 12 筆資料。
每一筆主要包含：
裝置平台
CPU 架構
RAM
Flash
需要的密碼功能
Security Category
使用情境
例如某一筆可能是 ARM Cortex-M4 裝置，需要使用 KEM 建立量子安全連線，並要求 Security Category 3。
這種情況下，系統要從現有的 PQC Evidence 中找出值得繼續測試的候選方案。
Week 2 和 Dataset 的對應是：
Unit：一個 PQC deployment scenario
Input：硬體條件、密碼功能、安全需求和使用情境
Target：符合需求而且值得進一步測試的 PQC candidate
Output：最多提供 5 個候選方案和對應的技術 Evidence

三、Time Range
目前 Dataset 主要有記錄資料整理和擷取的日期。
但是目前沒有完整記錄每一筆 benchmark 最原始的 publication date 或 commit date。
所以現在還不適合直接做 Time Split。
如果之後真的要模擬某個時間點做 PQC 選擇，就需要再補上論文年份、標準發布日期或 benchmark commit date，避免使用到當時還不存在的資料。

四、Fields
Scenario Dataset 目前主要欄位有：
scenario_id
device_platform
cpu_architecture
available_ram_bytes
available_flash_bytes
crypto_function
required_security_category
application_scenario
bandwidth_limit_kbps
max_latency_ms
power_limit_mw
threat_model
weak_label_candidates
label_source
label_status
其中前面的硬體和需求欄位可以當成 Input。
weak_label_candidates、label_source 和 label_status 屬於 Target 或 Label 相關資訊，所以之後不能直接拿來當 Input。
另外 Evidence Corpus 主要包含：
algorithm_family
parameter_set
crypto_function
security_category
implementation
cpu_architecture
keygen_cycles
sign 或 encapsulation cycles
verify 或 decapsulation cycles
stack usage
code size
key size
signature 或 ciphertext size
benchmark source
standard source
版本資訊

五、Label / Codebook
我的 Target 是 relevant PQC candidate set。
不過目前沒有完整的人工 Ground Truth，所以現在先使用 weak label。
目前 weak label 的產生方式主要看三個條件：
第一，cryptographic function 要符合，例如需要 KEM 就不能放 Digital Signature。
第二，Security Category 要符合需求。
第三，目前要有相對應的 Cortex-M4 benchmark Evidence。
例如需求是 KEM，Security Category 至少為 3，目前可能的候選就是 ML-KEM-768 和 ML-KEM-1024。
但這只是先用規則篩選出候選，不代表這些一定就是最終正確答案。
目前 12 筆 Scenario 都標記為 needs_human_review。
也就是之後如果真的要計算 Week 2 設定的 Recall@5 或 Top-3 Hit Rate，還需要研究者人工確認最後的 relevant candidate。

六、Inclusion / Exclusion
目前會納入 Dataset 的資料需要符合以下條件：
能確認 PQC algorithm 或 parameter set
能確認是 KEM 還是 Digital Signature
能確認 Security Category
有可以追溯的原始來源
有硬體或 CPU architecture 資訊
至少有一項效能或資源使用 Evidence
例如執行 cycles、stack memory 或 code size。
目前會排除：
找不到原始來源的資料
無法確認使用哪個 PQC algorithm 的資料
不知道 benchmark hardware 的資料
無法確認 parameter 或 implementation 的資料
和目前 ML-KEM、ML-DSA 範圍沒有直接關係的資料
目前沒有把 pqm4 所有演算法全部放進來，而是先限制在 NIST 已標準化的 ML-KEM 和 ML-DSA，避免一次混入太多不同狀態的 PQC 演算法。

七、Population / Coverage
我的 Target Population 是有明確硬體限制和 PQC 需求的 IoT 或 Embedded deployment scenario。
目前 Dataset 有：
12 筆 Scenario
18 筆 PQC Evidence
2 種 hardware platform
1 種 CPU architecture
目前 CPU architecture 都是 ARM Cortex-M4。
密碼功能則包含 KEM 和 Digital Signature。
目前 PQC 範圍主要是 ML-KEM 和 ML-DSA。
目前最大的 Coverage Limitation 是只有 Cortex-M4。
所以現在這份 Dataset 不能直接代表 ESP32、RISC-V、Cortex-M33 或其他 MCU。
也不能說目前結果可以泛化到所有 IoT / Embedded 裝置。

八、Train / Validation / Test Rule
我希望 Test set 模擬的是新的 hardware platform。
也就是 Test 裡的裝置平台最好是在 Train 裡沒有出現過的。
所以目前比較適合的 Split Strategy 是 Group Split。
Group key 使用 device_platform。
原因是同一個 hardware platform 的 CPU、RAM 和 Flash 等條件都很接近。
如果直接用 Random Split，很可能同一個 platform 的資料一部分進 Train，一部分進 Test。
這樣 Test 可能會太簡單，最後的結果也可能太樂觀。
但是目前 Audit 後發現只有 2 個 hardware platform。
如果要分 Train、Validation、Test 三組，而且又要求 platform 完全不重複，其實目前資料不夠。
所以目前我的決定是先不硬切正式的三組 Dataset。
之後增加更多 hardware platform，再真正做 Group Split。

九、Leakage Risks
目前我認為有三個比較重要的 Leakage Risk。
第一個是 Target-derived Leakage。
weak_label_candidates、label_source 和 label_status 這些欄位本身已經包含最後答案相關資訊。
所以這些欄位不能拿來當模型 Input。
第二個是 Split Leakage。
如果同一個 hardware platform 同時出現在 Train 和 Test，就可能讓 Test 結果太好看。
同一份 benchmark 或高度相似的 implementation 如果跨 Train 和 Test，也會有類似問題。
第三個是 Future Leakage。
目前沒有完整保存每一筆 benchmark 的發布時間。
所以如果以後要模擬某個時間點做 PQC 選擇，就需要先補時間資訊，避免使用到未來才出現的資料。

十、Quality Issues
這次 Dataset Audit 實際檢查後：
Scenario Dataset 有 12 筆資料。
Evidence Corpus 有 18 筆資料。
目前沒有發現 exact duplicate。
scenario_id 和 record_id 也都沒有重複。
目前比較明顯的問題是：
bandwidth_limit_kbps 全部缺值
max_latency_ms 全部缺值
power_limit_mw 全部缺值
threat_model 全部缺值
也就是這四個欄位目前 Missing Rate 都是 100%。
這代表現在這份 Dataset 可以用來檢查 CPU、RAM、Flash、cryptographic function 和 Security Category。
但是還不能完整支援 Week 2 原本提到的 bandwidth、latency、power 和 threat model。

十一、Version / Provenance
目前 Dataset Version 設定為 dataset_v0.2。
Audit 日期是 2026-09-29。
目前 Evidence Corpus 會保留：
benchmark source
NIST standard source
implementation
compiler
CPU architecture
benchmark file version
retrieved date
這樣之後如果資料更新，至少可以知道目前使用的是哪一版資料。
目前資料整理時，不會把不同 implementation 的 benchmark 直接合併。
不同平台上的 performance 也不會直接當成可以公平比較。

十二、Known Limitations
目前這份 Dataset 有幾個比較明顯的限制。
第一，目前只有兩個 hardware platform，而且全部都是 ARM Cortex-M4。
第二，目前只整理 ML-KEM 和 ML-DSA。
第三，bandwidth、latency、power 和 threat model 都還沒有實際資料。
第四，目前 12 筆 Scenario 的 Label 都只是 weak label，還沒有人工確認。
第五，只有兩個 hardware group，所以目前還沒辦法做完整的 Train、Validation、Test Group Split。
第六，目前沒有完整記錄每筆 benchmark 最原始的 publication time。
因此我現在不會說這份 Dataset 已經可以完整驗證 Week 2 的 AI Problem。
目前比較適合把它當成 prototype 和 Dataset Audit 用的第一版資料。