# AI System Week 1 Starter

案例：客服問題意圖分類

本 repo 是第一週課程 Starter Repo。你不需要訓練模型，也不會使用 ML、DL、LLM、RAG、FastAPI 或 MLflow。本週只練習從一個簡單 Rule-based Baseline 開始，觀察 Accuracy，並找出 Baseline 失敗的例子。

## 你這週要完成什麼

1. Fork 老師提供的 repo。
2. Clone 你自己的 fork。
3. 建立 Python 環境並安裝套件。
4. 執行環境檢查。
5. 執行 `notebooks/week01_baseline.ipynb`。
6. 找到 Accuracy 和一筆 Failure Case。
7. 填寫 `evidence/week01_note.md`。
8. Commit 並 Push 到你自己的 repo。

## 快速開始

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

安裝套件：

```bash
pip install --no-compile -r requirements.txt
```

檢查環境：

```bash
python check_env.py
```

啟動 Notebook。如果你的電腦已經有 Jupyter Notebook：

```bash
jupyter notebook
```

你也可以直接用 VS Code 或 Anaconda 開啟並執行：

```text
notebooks/week01_baseline.ipynb
```

如果你已經使用 Anaconda、VS Code 或學校電腦預先安裝的 Jupyter，也可以直接從該工具開啟 Notebook。這個 repo 的 `requirements.txt` 只安裝本週案例執行需要的 Python 套件與 Jupyter kernel。

## Repo 結構

```text
ai-system-week1-starter/
├── README.md
├── requirements.txt
├── check_env.py
├── data/
│   └── customer_intent_demo.csv
├── notebooks/
│   └── week01_baseline.ipynb
├── src/
│   └── rule_baseline.py
├── evidence/
│   └── week01_note.md
└── outputs/
    └── .gitkeep
```

## Dataset

資料位於 `data/customer_intent_demo.csv`，共 100 筆合成客服訊息，分成四類：

- `order_delivery`：訂單／配送
- `refund_return`：退款／退貨
- `account_login`：帳號／登入
- `product_info`：商品資訊

資料中刻意保留少量容易混淆的句子，讓你能看到 Rule-based Baseline 的限制。

## Baseline

Baseline 位於 `src/rule_baseline.py`。它只使用關鍵字規則，不訓練模型。第一週重點不是追求最高分，而是理解：

- Dataset 在哪裡
- Baseline 如何做出預測
- Metric 如何計算
- Failure Case 為什麼重要

## Evidence

請在執行 Notebook 後填寫：

```text
evidence/week01_note.md
```

你至少需要填入 Accuracy 和一筆 Failure Case。
