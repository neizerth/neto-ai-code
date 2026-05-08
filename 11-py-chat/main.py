orders = [
    {"order_id": "A-1001", "item": "Наушники"},
    {"item": "Клавиатура"},
    {"order_id": "A-1003", "item": "Мышь"},
]

for order in orders:
    order_id = order.get("order_id", "без номера")
    print(f"Заказ {order_id} отправлен в обработку")

print("Обработка завершена")

