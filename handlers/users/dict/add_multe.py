# pip imports
from telegram import (
    Update, ReplyKeyboardRemove, 
    InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ConversationHandler, CommandHandler, 
    MessageHandler, Filters, CallbackQueryHandler
    )

# local imports
from data import get_db
from models.dict import Dict, TOG
from states.dict import GIVE_MULTE, MULTE_SAVE
from keyboards.default.dict import get_dict_keyboard
from middlewares.check_subscribe import subscription_required
from utils.users_servise import get_user_and_settings, UserUpdate


@subscription_required
def add_multe_dict_handler(update: Update, context):
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if context.user_data.get('use_tog'):
        if lang == "en":
            text = "Method TOG is enabled.✅❗️"
            send_message = "Please enter the words (keys) you want to add:\n\nKey1 - Value1:Obraz1 - Garmanizatsiya1\nKey2 - Value2:Obraz2 - Garmanizatsiya2\n...\n\nEach new word must be on a new line."
        elif lang == "ru":
            text = "Метод TOG включен.✅❗️"
            send_message = "Пожалуйста, введите слова (ключи), которые вы хотите добавить:\n\nКлюч1 - Значение1:Образ1 - Гармонизация1\nКлюч2 - Значение2:Образ2 - Гармонизация2\n...\n\nКаждое новое слово должно быть на новой строке."
        else:
            text = "TOG usuli yoqilgan.✅❗️"
            send_message = "Iltimos, qo'shmoqchi bo'lgan so'zlarni quyidagi formatda kiriting:\n\nKalit1 - Qiymat1:Obraz1 - Garmanizatsiya1\nKalit2 - Qiymat2:Obraz2 - Garmanizatsiya2\n...\n\nHar bir yangi so'z yangi qatorda bo'lishi kerak."
    else:
        if lang == "en":
            text = "Method TOG is disabled.🚫❗️"
            send_message = "Please enter the words (keys) you want to add:\n\nKey1 - Value1\nKey2 - Value2\n...\n\nEach new word must be on a new line."
        elif lang == "ru":
            text = "Метод TOG отключен.🚫❗️"
            send_message = "Пожалуйста, введите слова (ключи), которые вы хотите добавить:\n\nКлюч1 - Значение1\nКлюч2 - Значение2\n...\n\nКаждое новое слово должно быть на новой строке."
        else:
            text = "TOG usuli o'chirilgan.🚫❗️"
            send_message = "Iltimos, qo'shmoqchi bo'lgan so'zlarni quyidagi formatda kiriting:\n\nKalit1 - Qiymat1\nKalit2 - Qiymat2\n...\n\nHar bir yangi so'z yangi qatorda bo'lishi kerak."

    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    update.message.reply_text(send_message)

    return GIVE_MULTE

def get_multe(update: Update, context):
    context.user_data['multe_input'] = update.message.text
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')
    texts = []
    error_lines = []
    lines = update.message.text.strip().split('\n')
    words = []
    
    for line_num, line in enumerate(lines, 1):
        if not line.strip():
            continue
        
        # Split by first '-' to separate key and rest
        first_dash_idx = line.find('-')
        if first_dash_idx == -1:
            if lang == "en":
                error_lines.append(f"Line {line_num}: '{line}' - Format error (missing - symbol)")
            elif lang == "ru":
                error_lines.append(f"Строка {line_num}: '{line}' - Ошибка формата (отсутствует символ -)")
            else:
                error_lines.append(f"Qator {line_num}: '{line}' - Format xato (- belgisi yo'q)")
            continue
            
        key = line[:first_dash_idx].strip()
        rest = line[first_dash_idx + 1:].strip()
        
        if not key:
            if lang == "en":
                error_lines.append(f"Line {line_num}: '{line}' - Key is empty")
            elif lang == "ru":
                error_lines.append(f"Строка {line_num}: '{line}' - Ключ пустой")
            else:
                error_lines.append(f"Qator {line_num}: '{line}' - Kalit bo'sh")
            continue

        if context.user_data.get('use_tog'):
            colon_idx = rest.find(':')
            if colon_idx == -1:
                if lang == "en":
                    error_lines.append(f"Line {line_num}: '{line}' - TOG format error (missing : symbol)")
                elif lang == "ru":
                    error_lines.append(f"Строка {line_num}: '{line}' - Ошибка TOG формата (отсутствует символ :)")
                else:
                    error_lines.append(f"Qator {line_num}: '{line}' - TOG format xato (: belgisi yo'q)")
                continue
                
            value = rest[:colon_idx].strip()
            obraz_garm_part = rest[colon_idx + 1:].strip()
            
            if not value:
                if lang == "en":
                    error_lines.append(f"Line {line_num}: '{line}' - Translation is empty")
                elif lang == "ru":
                    error_lines.append(f"Строка {line_num}: '{line}' - Перевод пустой")
                else:
                    error_lines.append(f"Qator {line_num}: '{line}' - Tarjima bo'sh")
                continue
                
            if not obraz_garm_part:
                if lang == "en":
                    error_lines.append(f"Line {line_num}: '{line}' - Obraz part is empty")
                elif lang == "ru":
                    error_lines.append(f"Строка {line_num}: '{line}' - Часть образа пустая")
                else:
                    error_lines.append(f"Qator {line_num}: '{line}' - Obraz qismi bo'sh")
                continue
            
            last_dash_idx = obraz_garm_part.rfind('-')
            if last_dash_idx == -1:
                # Garmanizatsiya yo'q - bu xato
                if lang == "en":
                    error_lines.append(f"Line {line_num}: '{line}' - Missing garmanization part (no - symbol)")
                elif lang == "ru":
                    error_lines.append(f"Строка {line_num}: '{line}' - Отсутствует часть гармонизации (нет символа -)")
                else:
                    error_lines.append(f"Qator {line_num}: '{line}' - Garmanizatsiya qismi yo'q (- belgisi yo'q)")
                continue
            else:
                obraz = obraz_garm_part[:last_dash_idx].strip()
                garmanization = obraz_garm_part[last_dash_idx + 1:].strip()
                
                # Garmanizatsiya bo'sh bo'lsa xato
                if not garmanization:
                    if lang == "en":
                        error_lines.append(f"Line {line_num}: '{line}' - Garmanization is empty")
                    elif lang == "ru":
                        error_lines.append(f"Строка {line_num}: '{line}' - Гармонизация пустая")
                    else:
                        error_lines.append(f"Qator {line_num}: '{line}' - Garmanizatsiya bo'sh")
                    continue
                
            texts.append(f"Key: {key}\nValue: {value}\nObraz: {obraz}\nGarmanizatsiya: {garmanization}\n")
            words.append({
                'key': key,
                'value': value,
                'obraz': obraz,
                'garmanization': garmanization
            })
        else:
            value = rest
            if not value:
                if lang == "en":
                    error_lines.append(f"Line {line_num}: '{line}' - Translation is empty")
                elif lang == "ru":
                    error_lines.append(f"Строка {line_num}: '{line}' - Перевод пустой")
                else:
                    error_lines.append(f"Qator {line_num}: '{line}' - Tarjima bo'sh")
                continue
                
            texts.append(f"Key: {key}\nValue: {value}\n")
            words.append({
                'key': key,
                'value': value
            })

    # Show errors if any
    if error_lines:
        error_count = len(error_lines)
        if lang == "en":
            error_msg = f"❌ {error_count} lines have errors and were skipped:\n\n" + "\n".join(error_lines)
        elif lang == "ru":
            error_msg = f"❌ {error_count} строк содержат ошибки и были пропущены:\n\n" + "\n".join(error_lines)
        else:
            error_msg = f"❌ {error_count} ta qatorda xato bor va o'tkazib yuborildi:\n\n" + "\n".join(error_lines)
        
    
    if texts:
        preview_text = "\n".join(texts)
        if lang == "en":
            preview_header = f"✅ Here is the preview of the words that will be saved({len(texts)}):"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Confirm ✅", callback_data="confirm_save"), InlineKeyboardButton("Cancel ❌", callback_data="cancel_save")]
            ])
        elif lang == "ru":
            preview_header = f"✅ Вот предварительный просмотр слов, которые будут сохранены({len(texts)}):"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Подтвердить ✅", callback_data="confirm_save"), InlineKeyboardButton("Отмена ❌", callback_data="cancel_save")]
            ])
        else:
            preview_header = f"✅ Saqlanishi kerak bo'lgan so'zlarning ko'rinishi({len(texts)}):"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Tasdiqlash ✅", callback_data="confirm_save"), InlineKeyboardButton("Bekor qilish ❌", callback_data="cancel_save")]
            ])
        
        context.user_data['words_to_save'] = words
        if error_msg:  
            update.message.reply_text(f"{error_msg}\n\n{preview_header}\n\n{preview_text}", reply_markup=keyboard)
        else:
            update.message.reply_text(f"{preview_header}\n\n{preview_text}", reply_markup=keyboard)
    else:
        if lang == "en":
            update.message.reply_text("❌ No valid words found. Please check the format and try again.")
        elif lang == "ru":
            update.message.reply_text("❌ Действительных слов не найдено. Пожалуйста, проверьте формат и попробуйте снова.")
        else:
            update.message.reply_text("❌ Hech qanday to'g'ri so'z topilmadi. Iltimos, formatni tekshirib qaytadan urinib ko'ring.")
        return ConversationHandler.END
    
    return MULTE_SAVE
def cancel_handler(update: Update, context):
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    
    lang = context.user_data.get('language')

    if lang == "en":
        update.message.reply_text("Operation cancelled. ❌")
        update.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(lang))
    elif lang == "ru":
        update.message.reply_text("Операция отменена. ❌")
        update.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(lang))
    else:
        update.message.reply_text("Amal bekor qilindi. ❌")
        update.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(lang))


def save_multe(update: Update, context):
    query = update.callback_query
    query.answer()
    
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        query.edit_message_text("Please start the bot using /start command.")
        return ConversationHandler.END
    lang = context.user_data.get('language')

    user, user_settings = get_user_and_settings(update.effective_user.id)

    if query.data == "confirm_save":
        if 'words_to_save' not in context.user_data:
            if lang == "en":
                query.edit_message_text("❌ No words to save found. Please try again.")
            elif lang == "ru":
                query.edit_message_text("❌ Сохраненные слова не найдены. Пожалуйста, попробуйте снова.")
            else:
                query.edit_message_text("❌ Saqlanadigan so'zlar topilmadi. Iltimos, qaytadan urinib ko'ring.")
            return ConversationHandler.END
        
        words = context.user_data['words_to_save']
        db = next(get_db())

        saved_words = []
        duplicate_words = []

        try:
            for word in words:
                # Check if key already exists for this user
                existing_word = db.query(Dict).filter(
                    Dict.key == word['key'],
                    Dict.user_id == user.id
                ).first()
                
                if existing_word:
                    duplicate_words.append(word['key'])
                    continue
                    
                # Save new word
                try:
                    new_dict = Dict(
                        user_id=user.id,
                        key=word['key'],
                        value=word['value']
                    )
                    db.add(new_dict)
                    db.commit()
                    db.refresh(new_dict)
                    
                    if user_settings.use_TOG and 'obraz' in word:
                        new_tog = TOG(
                            dict_id=new_dict.id,
                            obraz=word['obraz'],
                            garm=word['garmanization']
                        )
                        db.add(new_tog)
                        db.commit()
                
                    saved_words.append(word['key'])
                    
                except Exception as e:
                    # If any error occurs, rollback and continue
                    db.rollback()
                    duplicate_words.append(word['key'])
                    
        finally:
            db.close()

        # Prepare response message
        response_parts = []
        
        if saved_words:
            saved_count = len(saved_words)
            if user_settings.language == "en":
                response_parts.append(f"✅ {saved_count} words have been saved successfully!")
            elif user_settings.language == "ru":
                response_parts.append(f"✅ {saved_count} слов успешно сохранены!")
            else:
                response_parts.append(f"✅ {saved_count} ta so'z muvaffaqiyatli saqlandi!")
                
        if duplicate_words:
            duplicate_count = len(duplicate_words)
            duplicate_list = ", ".join(duplicate_words)
            if user_settings.language == "en":
                response_parts.append(f"❌ {duplicate_count} words were skipped (already exist):\n{duplicate_list}")
            elif user_settings.language == "ru":
                response_parts.append(f"❌ {duplicate_count} слов были пропущены (уже существуют):\n{duplicate_list}")
            else:
                response_parts.append(f"❌ {duplicate_count} ta so'z o'tkazib yuborildi (allaqachon mavjud):\n{duplicate_list}")
        
        final_message = "\n\n".join(response_parts)
        query.edit_message_text(final_message)
        query.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(user_settings.language))
            
    elif query.data == "cancel_save":
        if user_settings.language == "en":
            query.edit_message_text("The operation has been cancelled. ❌")
            query.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(user_settings.language))
        elif user_settings.language == "ru":
            query.edit_message_text("Операция была отменена. ❌")
            query.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(user_settings.language))
        else:
            query.edit_message_text("Amal bekor qilindi. ❌")
            query.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(user_settings.language))

    context.user_data.clear()
    UserUpdate(update, context)
    return ConversationHandler.END


def register_handlers(dp):
    conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text(["➕ Add Multiple Words", "➕ Добавить несколько слов", "➕ Bir nechta so'z qo'shish"]), add_multe_dict_handler)],
        states={
            GIVE_MULTE: [MessageHandler(Filters.text & ~Filters.command, get_multe)],
            MULTE_SAVE: [CallbackQueryHandler(save_multe)],
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)],
        allow_reentry=True
    )
    dp.add_handler(conv)