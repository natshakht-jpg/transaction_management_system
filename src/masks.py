def get_mask_card_number(card_number: int) -> str:
    """Функция  принимает на вход номер карты и возвращает ее маску."""
    card_str = str(card_number)
    return card_str[:4] + " " + card_str[4:6] + "** **** " + card_str[-4:]


def get_mask_account(account_number: int) -> str:
    """Функция  принимает на вход номер счета и возвращает его маску."""
    account_str = str(account_number)
    return "**" + account_str[-4:]
