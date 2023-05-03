from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

kb_menu = InlineKeyboardMarkup(inline_keyboard=[
    InlineKeyboardButton("Добавить", callback_data="add_user"),
    InlineKeyboardButton("Изменить", callback_data="edit_user"),
])

kb_edit = InlineKeyboardMarkup(inline_keyboard=[
    InlineKeyboardButton("Имя", callback_data="change_name"), InlineKeyboardButton("Био", callback_data="change_bio"),
    InlineKeyboardButton("Тг ник", callback_data="change_tg"),
])


kb_accept_and_reject_edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("✅ Принять ✅", callback_data="accept_edit"),
     InlineKeyboardButton("❌ Отмена ❌", callback_data="reject_edit")]])


def create_ikb_records_list(rec_id: List[int], records_names: List[str],
                            std_id: int = None, step: int = None, cur_step: int = None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    if step:
        # Get records slice
        step_rec_name = records_names[cur_step:step:]
        rec_id = rec_id[cur_step:step:]
        # Create records list
        for i, name in enumerate(step_rec_name):
            cd_data = f'choose_{rec_id[i]}_{name}'
            ikb.add(InlineKeyboardButton(name + " 🪪", callback_data=cd_data))
        # Create page control buttons
        next, back = 'next_inline', 'back_inline'
        if cur_step == 0 and len(records_names) > step:
            ikb.add(InlineKeyboardButton("➡", callback_data=next))
        elif len(records_names) > step:
            ikb.add(InlineKeyboardButton("⬅", callback_data=back),
                    InlineKeyboardButton("➡", callback_data=next))
        elif cur_step != 0 and len(records_names) <= step:
            ikb.add(InlineKeyboardButton("⬅", callback_data=back))
    return ikb.row(InlineKeyboardButton("🔙 Назад в меню", callback_data="back_menu_edit"))


def back_info_user(inline: str):
    return InlineKeyboardMarkup(inline_keyboard=[InlineKeyboardButton("Назад", callback_data=inline)])
