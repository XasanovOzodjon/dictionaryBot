from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.misc.languages import languages

def create_translate_to_keyboard(page=1, languages_per_page=9, text = 'translate_to_') -> InlineKeyboardMarkup:
    """
    Tarjima qilish uchun tillar klaviaturasini yaratadi
    """
    language_list = list(languages.items())
    total_languages = len(language_list)
    total_pages = (total_languages + languages_per_page - 1) // languages_per_page
    
    start_index = (page - 1) * languages_per_page
    end_index = start_index + languages_per_page
    current_languages = language_list[start_index:end_index]
    
    buttons = []
    
    # Tillarni 3 ta ustunda joylashtirish
    for i in range(0, len(current_languages), 3):
        row = []
        for j in range(3):
            if i + j < len(current_languages):
                lang_name, lang_code = current_languages[i + j]
                # Til nomini qisqartirish (maksimum 10 belgi)
                display_name = lang_name if len(lang_name) <= 10 else lang_name[:7] + "..."
                row.append(InlineKeyboardButton(
                    display_name,
                    callback_data=f"{text}{lang_code}"
                ))
        buttons.append(row)
    
    # Navigatsiya tugmalari
    nav_buttons = []
    
    # Orqaga tugmasi
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("◀️ Orqaga", callback_data=f"translate_page_{page-1}"))
    
    # Sahifa raqami
    nav_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="page_info"))
    
    # Oldinga tugmasi
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Oldinga ▶️", callback_data=f"translate_page_{page+1}"))
    
    if nav_buttons:
        buttons.append(nav_buttons)
    
    return InlineKeyboardMarkup(buttons)