# Week 1 Evidence

學號：7114029039

姓名：蔡忻辰

## Check-off

1. Dataset 在哪裡？
`data/customer\_intent\_demo.csv`
2. Baseline 程式在哪裡？
src/rule\_baseline.py
3. 本週 Accuracy = 0.950
4. 請填寫一個 Failure Case：

   * 輸入訊息：退貨物流已收走但沒有更新
   * 正確答案：refund\_return
   * Baseline 預測：order\_delivery
5. 你覺得這個 Baseline 為什麼會錯？請用一句話說明。
因程式優先檢查訂單及配送類的關鍵字，看到物流就直接判成order\_delivery，沒有考慮這則訊息真正要問的是退貨進度。
6. 這是否代表現在一定要使用 AI？為什麼？請用一句話說明。

&#x20;	不一定，可先加入退貨與物流同時出現時的判斷規則，再測正確率，評估是否需要用 AI。

