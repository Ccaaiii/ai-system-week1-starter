"""Simple rule-based baseline for customer intent classification.

This file intentionally uses only keyword rules. Week 1 is about understanding
datasets, baseline metrics, and failure cases before introducing model training.
"""

from __future__ import annotations


LABELS = [
    "order_delivery",
    "account_login",
    "refund_return",
    "product_info",
]


KEYWORDS = {
    "order_delivery": [
        "訂單",
        "物流",
        "配送",
        "出貨",
        "到貨",
        "包裹",
        "貨運",
        "追蹤",
        "送達",
        "收件",
        "地址",
        "超商",
        "取貨",
    ],
    "refund_return": [
        "退款",
        "退貨",
        "退費",
        "換貨",
        "取消",
        "七天",
        "鑑賞",
        "發票",
        "刷退",
        "退",
    ],
    "account_login": [
        "登入",
        "登不進",
        "密碼",
        "帳號",
        "會員",
        "驗證碼",
        "註冊",
        "鎖定",
        "手機",
        "信箱",
    ],
    "product_info": [
        "商品",
        "產品",
        "尺寸",
        "顏色",
        "規格",
        "材質",
        "庫存",
        "保固",
        "型號",
        "現貨",
        "重量",
    ],
}


def predict_intent(text: str) -> str:
    """Predict an intent with readable first-match keyword rules."""

    normalized = str(text).strip().lower()
    for label in LABELS:
        for keyword in KEYWORDS[label]:
            if keyword.lower() in normalized:
                return label
    return "product_info"


def predict_batch(texts: list[str]) -> list[str]:
    """Predict many customer messages."""

    return [predict_intent(text) for text in texts]
