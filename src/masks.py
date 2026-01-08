import logging  # Импортируем библиотеки logging


# Логер для модуля masks
logger = logging.getLogger(__name__)

# Создаем handler для записи в файл
file_handler = logging.FileHandler('logs/masks.log', mode='w', encoding='utf-8')

# Создаем formatter с нужным форматом
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Добавляем formatter к handler
file_handler.setFormatter(formatter)

# Добавляем handler к логеру
logger.addHandler(file_handler)

# Устанавливаем уровень логирования
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    # Проверяем, что строка состоит только из цифр
    if not card_number.isdigit():
        logger.error(f"Номер карты содержит не только цифры: {card_number}")
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверяем длину номера карты
    if len(card_number) != 16:
        logger.error(f"Номер карты имеет неправильную длину: {card_number}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем маску
    masked_card = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
    logger.info(f"Успешно создана маска для карты: {masked_card}")
    return masked_card


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    # Проверяем, что строка состоит только из цифр
    if not account_number.isdigit():
        logger.error(f"Номер счета содержит не только цифры: {account_number}")
        raise ValueError("Номер счета должен содержать только цифры")

    # Проверяем минимальную длину номера счета
    if len(account_number) < 4:
        logger.error(f"Номер счета имеет неправильную длину: {account_number}")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Форматируем маску
    masked_account = "**" + account_number[-4:]
    logger.info(f"Успешно создана маска для счета: {masked_account}")
    return masked_account
