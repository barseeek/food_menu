import json

from django.conf import settings
from django.urls import reverse
from yookassa import Payment, Configuration

import uuid

Configuration.account_id = settings.YOO_SHOP_ID
Configuration.secret_key = settings.YOO_API_TOKEN


def create_yoo_payment(request, payment_amount, payment_currency, metadata) -> dict:
    if metadata is None:
        metadata = {}
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
        "description": f"Оформление подписки",
    }, idempotence_key)
    request.session["payment_id"] = payment["id"]
    request.session["subscription_data"] = metadata.copy()
    return json.loads(payment.json())
