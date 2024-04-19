import json

from django.conf import settings
from django.urls import reverse
from yookassa import Payment, Configuration

import uuid

Configuration.account_id = settings.YOO_SHOP_ID
Configuration.secret_key = settings.YOO_API_TOKEN


def create_yoo_payment(payment_amount, payment_currency, sub_period, metadata: dict = {}) -> dict:
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "save_payment_method": True,
        "amount": {
            "value": payment_amount,
            "currency": payment_currency,
        },
        "metadata": metadata,
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": settings.YOO_REDIRECT_URL,
        },
        "capture": True,
        "description": f"Оформление подписки на срок {sub_period}",
    }, idempotence_key)

    return json.loads(payment.json())
