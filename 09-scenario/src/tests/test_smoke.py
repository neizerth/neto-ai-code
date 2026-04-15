from services.shopping_service import build_shopping_list


def test_empty_input() -> None:
    result = build_shopping_list("", "2", "Список продуктов")
    assert result.ok is False

