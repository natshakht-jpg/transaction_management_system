def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    # Проверяем, что строка состоит только из цифр
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверяем длину номера карты
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем маску
    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    # Проверяем, что строка состоит только из цифр
    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    # Проверяем минимальную длину номера счета
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Форматируем маску
    return "**" + account_number[-4:]
