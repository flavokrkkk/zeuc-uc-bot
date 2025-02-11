from datetime import datetime

from database.models.models import Purchase


def format_purchase_data(purchase: Purchase, data: dict[str, str]) -> str:
    us_packs_info = []
    for uc_pack in data['uc_packs']:
        errors = "\n" + "\n".join([
            "{uc_code} → {message}".format(uc_code=err['uc_code'], message=err['message'])
            for err in uc_pack['errors']
        ]) if uc_pack['errors'] else "Нет ошибок"

        pack_info = (
            f"<b>Сумма</b>: {uc_pack['total_sum']} ₽\n"
            f"<b>Количество UC</b>: {uc_pack['uc_amount']} UC x {uc_pack['quantity']}\n"
            f"<b>Количество активированных кодов</b>: {uc_pack['activated_codes']}\n"
            f"<b>Неуспешные Activation IDs</b>: {uc_pack.get('error_activation_ids')}\n"
            f"<b>Ошибки активации (Код → Ошибка)</b>: {errors}"
        ).strip()

        us_packs_info.append(pack_info)

    message_text = (
        f"<b>Заказ</b>: {purchase.payment_id}\n"
        f"<b>Дата покупки</b>: {datetime.fromtimestamp(purchase.created_at / 1000).strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"<b>Игрок</b>: {purchase.player_id}\n"
        f"<b>Сумма UC</b>: {purchase.uc_sum} ₽\n"
        f"<b>Сумма заказа</b>: {purchase.price} ₽\n"
        f"<b>Метод оплаты</b>: {purchase.payment_method}\n"
        f"<b>Статус</b>: {purchase.status}\n\n"
        f"<b>Информация по UC-пакетам:</b>\n\n" + "\n\n".join(us_packs_info)
    ).strip()

    return message_text