from datetime import date, timedelta

def calculate_priority(due_date: date, importance: int) -> float:
    """
    Рассчитывает приоритет задачи.
    :param due_date: дата дедлайна (date object)
    :param importance: важность (целое число от 1 до 10)
    :return: значение приоритета (чем выше, тем срочнее)
    """
    if not isinstance(due_date, date):
        raise TypeError("due_date must be a date")
    if not isinstance(importance, int) or importance < 1 or importance > 10:
        raise ValueError("importance must be an integer between 1 and 10")
    
    today = date.today()
    days_left = (due_date - today).days
    
    # Базовый приоритет: чем меньше дней, тем выше приоритет
    if days_left <= 0:
        # Просроченные задачи получают максимальный приоритет
        base_priority = 100.0
    else:
        base_priority = 100.0 / days_left
    
    # Модификатор важности: умножаем на importance (1..10)
    priority = base_priority * importance
    
    # Ограничим значение сверху (чтобы не уходило в бесконечность)
    return min(priority, 1000.0)
