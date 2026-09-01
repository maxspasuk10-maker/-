"""Клавиатуры бота."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_verification_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пройти верификацию", callback_data="start_verify")]
        ]
    )


def skip_kb(step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data=f"skip_{step}")]
        ]
    )


def class_selection_kb() -> InlineKeyboardMarkup:
    classes_9 = ["9-1", "9-2", "9-3", "9-4"]
    classes_10 = [
        "10 ф-1", "10 ф-2", "10 у/ф", "10 ф-м",
        "10 б-х-м", "10 пр", "10 мист",
    ]
    classes_11 = [
        "11 ф-1", "11 ф-2", "11 у/ф", "11 ф-м",
        "11 б-х-м", "11 пр-1", "11 пр-2", "11 мист",
    ]

    buttons = []
    for c in classes_9:
        buttons.append(InlineKeyboardButton(text=c, callback_data=f"class_{c}"))
    for c in classes_10:
        buttons.append(InlineKeyboardButton(text=c, callback_data=f"class_{c}"))
    for c in classes_11:
        buttons.append(InlineKeyboardButton(text=c, callback_data=f"class_{c}"))

    rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
    rows.append([InlineKeyboardButton(text="Пропустить", callback_data="skip_class")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def psl_score_kb(user_id: int) -> InlineKeyboardMarkup:
    """Клавиатура оценки PSL для модератора."""
    scores = [
        1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5,
        6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0,
    ]
    buttons = [
        InlineKeyboardButton(text=str(s), callback_data=f"score_{user_id}_{s}")
        for s in scores
    ]
    rows = [buttons[i : i + 5] for i in range(0, len(buttons), 5)]
    rows.append(
        [
            InlineKeyboardButton(
                text="Оценить + Написать фидбек",
                callback_data=f"feedback_{user_id}",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def result_kb(user_id: int, invite_link: str | None = None) -> InlineKeyboardMarkup:
    buttons = []
    if invite_link:
        buttons.append(
            [InlineKeyboardButton(text="Вступить в группу", url=invite_link)]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="Посмотреть детальную информацию",
                callback_data=f"details_{user_id}",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def details_back_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="« Назад", callback_data=f"back_result_{user_id}")]
        ]
    )
