# pip imports
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

# local imports
from data import get_db
from models.dict import Dict, TOG
from keyboards.default.dict import get_dict_keyboard
from middlewares.check_subscribe import subscription_required
from utils.users_servise import get_user_and_settings, UserUpdate
from states.dict import (ONE_GET_KEY, ONE_GET_VALUE, ONE_GET_OBRAZ, ONE_GET_GARMANIZATION, ONE_SAVE)


@subscription_required
def add_one_dict_handler(update: Update, context):
    user, user_settings = get_user_and_settings(update.effective_user.id)

    if not context.user_data:
        UserUpdate(update, context)
        
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if context.user_data.get('use_tog'):
        if lang == "en":
            text = "Method TOG is enabled.✅❗️"
        elif lang == "ru":
            text = "Метод TOG включен.✅❗️"
        else:
            text = "TOG usuli yoqilgan.✅❗️"
    else:
        if lang == "en":
            text = "Method TOG is disabled.🚫❗️"
        elif lang == "ru":
            text = "Метод TOG отключен.🚫❗️"
        else:
            text = "TOG usuli o'chirilgan.🚫❗️"

    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    if lang == "en":
        update.message.reply_text("Please enter the word (key) you want to add:")
    elif lang == "ru":
        update.message.reply_text("Пожалуйста, введите слово (ключ), которое вы хотите добавить:")
    else:
        update.message.reply_text("Iltimos, qo'shmoqchi bo'lgan so'zni (kalit) kiriting:")
    
    return ONE_GET_KEY
    

def get_key(update: Update, context):
    context.user_data['new_word_key'] = update.message.text

    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if lang == "en":
        update.message.reply_text("Please enter the translation (value) of the word:")
    elif lang == "ru":
        update.message.reply_text("Пожалуйста, введите перевод (значение) слова:")
    else:
        update.message.reply_text("Iltimos, so'zning tarjimasini (qiymatini) kiriting:")

    return ONE_GET_VALUE

def get_value(update: Update, context):
    context.user_data['new_word_value'] = update.message.text

    context.user_data['new_word_key'] = update.message.text

    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if context.user_data.get('use_tog') == False:

        if lang == "en":
            update.message.reply_text(f"Please confirm to save the new word.\n Word: {context.user_data['new_word_key']}\n Translation: {context.user_data['new_word_value']}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Confirm ✅", callback_data="confirm_save"), InlineKeyboardButton("Cancel ❌", callback_data="cancel_save")]
            ]))
        elif lang == "ru":
            update.message.reply_text(f"Пожалуйста, подтвердите сохранение нового слова.\n Слово: {context.user_data['new_word_key']}\n Перевод: {context.user_data['new_word_value']}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Подтвердить ✅", callback_data="confirm_save"), InlineKeyboardButton("Отменить ❌", callback_data="cancel_save")]
            ]))
        else:
            update.message.reply_text(f"Iltimos, yangi so'zni saqlashni tasdiqlang.\n So'z: {context.user_data['new_word_key']}\n Tarjima: {context.user_data['new_word_value']}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Tasdiqlash ✅", callback_data="confirm_save"), InlineKeyboardButton("Bekor qilish ❌", callback_data="cancel_save")]
            ]))
        return ONE_GET_OBRAZ
        
    else:
        if lang == "en":
            update.message.reply_text(f"Please enter the obraz for the word({context.user_data['new_word_key']}):")
        elif lang == "ru":
            update.message.reply_text(f"Пожалуйста, введите образ для слова({context.user_data['new_word_key']}):")
        else:
            update.message.reply_text(f"Iltimos, so'z({context.user_data['new_word_key']}) uchun obraz kiriting:")

        return ONE_GET_OBRAZ

def save_one_dict_whithout_tog(update: Update, context):
    query = update.callback_query
    query.answer()

    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')
    user, user_settings = get_user_and_settings(update.effective_user.id)
    
    if query.data == "confirm_save":
        with next(get_db()) as db:
            new_dict_entry = Dict(
                key=context.user_data['new_word_key'],
                value=context.user_data['new_word_value'],
                user_id=user.id
            )
            db.add(new_dict_entry)
            db.commit()
            UserUpdate(update, context)
        

        if lang == "en":
            query.edit_message_text("The new word has been saved successfully! ✅")
            query.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END

        elif lang == "ru":
            query.edit_message_text("Новое слово успешно сохранено! ✅")
            query.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
        else:
            query.edit_message_text("Yangi so'z muvaffaqiyatli saqlandi! ✅")
            query.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END

    elif query.data == "cancel_save":
        if lang == "en":
            query.edit_message_text("The operation has been cancelled. ❌")
            query.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END

        elif lang == "ru":
            query.edit_message_text("Операция была отменена. ❌")
            query.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
        else:
            query.edit_message_text("Amal bekor qilindi. ❌")
            query.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END

def get_obraz(update: Update, context):
    context.user_data['new_word_obraz'] = update.message.text

    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if lang == "en":
        update.message.reply_text(f"Please enter the garmanization for the word({context.user_data['new_word_key']}) - obraz({context.user_data['new_word_obraz']}):")
    elif lang == "ru":
        update.message.reply_text(f"Пожалуйста, введите гарманизацию для слова({context.user_data['new_word_key']}) - образ({context.user_data['new_word_obraz']}):")
    else:
        update.message.reply_text(f"Iltimos, so'z({context.user_data['new_word_key']}) - obraz({context.user_data['new_word_obraz']}) uchun garmanization kiriting:")

    return ONE_GET_GARMANIZATION

def get_garmanization(update: Update, context):
    context.user_data['new_word_garmanization'] = update.message.text

    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if lang == "en":
        update.message.reply_text(f"Please confirm to save the new word.\n Word: {context.user_data['new_word_key']}\n Translation: {context.user_data['new_word_value']}\n Obraz: {context.user_data['new_word_obraz']}\n Garmanization: {context.user_data['new_word_garmanization']}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Confirm ✅", callback_data="confirm_save"), InlineKeyboardButton("Cancel ❌", callback_data="cancel_save")]
        ]))
    elif lang == "ru":
        update.message.reply_text(f"Пожалуйста, подтвердите сохранение нового слова.\n Слово: {context.user_data['new_word_key']}\n Перевод: {context.user_data['new_word_value']}\n Образ: {context.user_data['new_word_obraz']}\n Гармонизация: {context.user_data['new_word_garmanization']}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Подтвердить ✅", callback_data="confirm_save"), InlineKeyboardButton("Отменить ❌", callback_data="cancel_save")]
        ]))
    else:
        update.message.reply_text(f"Iltimos, yangi so'zni saqlashni tasdiqlang.\n So'z: {context.user_data['new_word_key']}\n Tarjima: {context.user_data['new_word_value']}\n Obraz: {context.user_data['new_word_obraz']}\n Garmanization: {context.user_data['new_word_garmanization']}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Tasdiqlash ✅", callback_data="confirm_save"), InlineKeyboardButton("Bekor qilish ❌", callback_data="cancel_save")]
        ]))

    return ONE_SAVE

def save_one_dict(update: Update, context):
    query = update.callback_query
    query.answer()
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')
    
    user, user_settings = get_user_and_settings(update.effective_user.id)

    if query.data == "confirm_save":
        db = next(get_db())
        new_dict_entry = Dict(
            key=context.user_data['new_word_key'],
            value=context.user_data['new_word_value'],
            user_id=user.id
        )
        db.add(new_dict_entry)
        db.commit()
        db.refresh(new_dict_entry)
        UserUpdate(update, context)

        if user_settings.use_TOG:
            new_tog_entry = TOG(
                dict_id=new_dict_entry.id,
                obraz=context.user_data['new_word_obraz'],
                garm=context.user_data['new_word_garmanization']
            )
            db.add(new_tog_entry)
            db.commit()
            UserUpdate(update, context)

        db.close()

        if lang == "en":
            query.edit_message_text("The new word has been saved successfully! ✅")
            query.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
        elif lang == "ru":
            query.edit_message_text("Новое слово успешно сохранено! ✅")
            query.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
        else:
            query.edit_message_text("Yangi so'z muvaffaqiyatli saqlandi! ✅")
            query.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
    elif query.data == "cancel_save":
        if lang == "en":
            query.edit_message_text("The operation has been cancelled. ❌")
            query.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
        elif lang == "ru":
            query.edit_message_text("Операция была отменена. ❌")
            query.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END
        else:
            query.edit_message_text("Amal bekor qilindi. ❌")
            query.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(lang))
            return ConversationHandler.END

    context.user_data.clear()
    UserUpdate(update, context)
    return ConversationHandler.END

def cancel_handler(update: Update, context):
    if not context.user_data:
        UserUpdate(update, context)
    if 'language' not in context.user_data:
        update.message.reply_text("Please start the bot using /start command.")
        return
    lang = context.user_data.get('language')

    if lang == "en":
        update.message.reply_text("Operation cancelled. ❌", reply_markup=get_dict_keyboard(lang))
        update.message.reply_text("Dictionary Menu📚", reply_markup=get_dict_keyboard(lang))
    elif lang == "ru":
        update.message.reply_text("Операция отменена. ❌", reply_markup=get_dict_keyboard(lang))
        update.message.reply_text("Меню словаря📚", reply_markup=get_dict_keyboard(lang))
    else:
        update.message.reply_text("Amal bekor qilindi. ❌", reply_markup=get_dict_keyboard(lang))
        update.message.reply_text("Lug'at menu📚", reply_markup=get_dict_keyboard(lang))


    return ConversationHandler.END

def register_handlers(dp):
    conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text(["➕ Add One Word", "➕ Добавить одно слово", "➕ Bitta so'z qo'shish"]), add_one_dict_handler)],
        states={
            ONE_GET_KEY: [MessageHandler(Filters.text & ~Filters.command, get_key)],
            ONE_GET_VALUE: [MessageHandler(Filters.text & ~Filters.command, get_value)],
            ONE_GET_OBRAZ: [MessageHandler(Filters.text & ~Filters.command, get_obraz), CallbackQueryHandler(save_one_dict_whithout_tog)],
            ONE_GET_GARMANIZATION: [MessageHandler(Filters.text & ~Filters.command, get_garmanization)],
            ONE_SAVE: [CallbackQueryHandler(save_one_dict)],
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)],
        allow_reentry=True
    )
    dp.add_handler(conv)