from utils.users_servise import get_user_and_settings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler
from keyboards.inline.transletor import get_transletor_keyborad
from keyboards.default.menu_keyboard import get_menu_keyboard
from models.settings import User_Settings
import threading
import time
from data import get_db
from keyboards.inline.translate_languages import create_translate_to_keyboard
from googletrans import Translator
from states.start import TRANSLATE, CHECK_TR

def transletor_handler(update: Update, context: CallbackContext):
    user, user_setings = get_user_and_settings(update.effective_user.id)
    if not user:
        update.message.reply_text("Please start the bot using /start command.")
        return

    if user_setings.language == 'en':
        text = "Translator:"
    elif user_setings.language == 'ru':
        text = "Переводчик:"
    else:
        text = "Tarjimon:"
    
    mode_message = update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )
    
    def delete_message_later():
        import time
        time.sleep(0.1)
        try:
            context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=mode_message.message_id
            )
        except Exception:
            pass

    threading.Thread(target=delete_message_later, daemon=True).start()
    
    update.message.reply_text(
        text=text,
        reply_markup=get_transletor_keyborad(user_setings)
    )
    return TRANSLATE


def tr(update: Update, context: CallbackContext):
    user, user_settings = get_user_and_settings(update.effective_user.id)
    text = update.message.text
    from_user = user_settings.translate_from
    to_tr = user_settings.translate_to
    translator = Translator()
    result = translator.translate(f"{text}", src=f'{from_user}', dest=f'{to_tr}')
    
    update.message.reply_text(result.text)
    return TRANSLATE


def check_call(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    user, user_settings = get_user_and_settings(update.effective_user.id)
    
    if query_data == "close_transletor":
        update.callback_query.message.delete()
        update.callback_query.answer()
        
        if user_settings.language == 'en':
            menu_text = "Main Menu:"
        elif user_settings.language == 'ru':
            menu_text = "Главное меню:"
        else:
            menu_text = "Asosiy menu:"
        
        update.effective_message.bot.send_message(
            chat_id=update.effective_chat.id,
            text=menu_text,
            reply_markup=get_menu_keyboard(user_settings.language)
        )
        query.answer()
        return ConversationHandler.END
    elif query_data in ['change_from', 'change_to', 'change_toto']:
        if query_data == "change_toto":
            with next(get_db()) as db:
                user, user_settings = get_user_and_settings(update.effective_user.id)
                
                # Merge the object into current session to avoid session conflicts
                user_settings = db.merge(user_settings)
                
                # Check if there's actually a change to make
                if user_settings.translate_from == user_settings.translate_to:
                    query.answer("Tillalar allaqachon bir xil!")
                    return TRANSLATE
                
                temp = user_settings.translate_from
                user_settings.translate_from = user_settings.translate_to
                if temp != 'auto':
                    user_settings.translate_to = temp
                
                # Save changes to database
                db.commit()
                
                # Update the keyboard with new settings
                try:
                    query.edit_message_reply_markup(reply_markup=get_transletor_keyborad(user_settings))
                    query.answer("Tarjima tillari almashtirildi!")
                except Exception:
                    # If keyboard update fails (e.g., same content), just answer the query
                    query.answer("Tarjima tillari almashtirildi!")
                return TRANSLATE
        
        if query_data == "change_to":
            with next(get_db()) as db:
                user, user_settings = get_user_and_settings(update.effective_user.id)
                
                # Merge the object into current session to avoid session conflicts
                user_settings = db.merge(user_settings)
                if user_settings.language == 'en':
                    text = "Choose the target language:"
                elif user_settings.language == 'ru':
                    text = "Выберите целевой язык:"
                else:  # Uzbek
                    text = "Maqsad tilini tanlang:"
                query.edit_message_text(
                    text=text,
                    reply_markup=create_translate_to_keyboard(text='translate_to_')
                    )
                return CHECK_TR
        
        if query_data == "change_from":
            with next(get_db()) as db:
                user, user_settings = get_user_and_settings(update.effective_user.id)
                
                # Merge the object into current session to avoid session conflicts
                user_settings = db.merge(user_settings)
                if user_settings.language == 'en':
                    text = "Choose the source language:"
                elif user_settings.language == 'ru':
                    text = "Выберите язык источника:"
                else:  # Uzbek
                    text = "Manba tilini tanlang:"
                query.edit_message_text(
                    text=text,
                    reply_markup=create_translate_to_keyboard(text='translate_from_')
                    )
                return CHECK_TR
            
    else:
        query.answer()
        return TRANSLATE


def change_transletor_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    
    if query_data.startswith("translate_from_"):
        new_from_lang = query_data.replace("translate_from_", "")
        with next(get_db()) as db:
            user, user_settings = get_user_and_settings(update.effective_user.id)
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.translate_from = new_from_lang
            
            # Save changes to database
            db.commit()
            
            # Refresh the object to get the latest state
            db.refresh(user_settings)
            
            if user_settings.language == 'en':
                text = "Translator:"
            elif user_settings.language == 'ru':
                text = "Переводчик:"
            else:
                text = "Tarjimon:"
            query.edit_message_text(
                text=text,
                reply_markup=get_transletor_keyborad(user_settings))
            return TRANSLATE
    if query_data.startswith("translate_to_"):
        new_to_lang = query_data.replace("translate_to_", "")
        with next(get_db()) as db:
            user, user_settings = get_user_and_settings(update.effective_user.id)
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.translate_to = new_to_lang
            db.commit()
            
            # Refresh the object to get the latest state
            db.refresh(user_settings)
            
            if user_settings.language == 'en':
                text = "Translator:"
            elif user_settings.language == 'ru':
                text = "Переводчик:"
            else:
                text = "Tarjimon:"
            query.edit_message_text(
                text=text,
                reply_markup=get_transletor_keyborad(user_settings))
            return TRANSLATE
    elif query_data.startswith("page_"):
            # Handle page navigation for different language selection contexts
            if query_data.startswith("page_from"):
                page = int(query_data.replace("page_from", ""))
                text_prefix = 'translate_from_'
            elif query_data.startswith("page_to"):
                page = int(query_data.replace("page_to", ""))
                text_prefix = 'translate_to_'
            else:
                # Default case for backward compatibility
                page = int(query_data.replace("translate_page_", ""))
                text_prefix = 'translate_to_'
            
            try:
                update.callback_query.edit_message_reply_markup(
                    reply_markup=create_translate_to_keyboard(page=page, text=text_prefix)
                )
            except Exception:
                # If keyboard update fails (e.g., same content), just continue
                pass
            update.callback_query.answer()
            return CHECK_TR

    elif query_data == "page_info":
        update.callback_query.answer()
        return CHECK_TR


def exit_translator_fallback(update: Update, context: CallbackContext):
    user, user_settings = get_user_and_settings(update.effective_user.id)
    
    if user_settings.language == 'en':
        menu_text = "Main Menu:"
    elif user_settings.language == 'ru':
        menu_text = "Главное меню:"
    else:
        menu_text = "Asosiy menu:"
    
    update.message.reply_text(
        text=menu_text,
        reply_markup=get_menu_keyboard(user_settings.language)
    )
    return ConversationHandler.END


def start_command_fallback(update: Update, context: CallbackContext):
    return ConversationHandler.END


def help_command_fallback(update: Update, context: CallbackContext):
    from .help import bot_help
    bot_help(update, context)
    return ConversationHandler.END


def register_handlers(dp):
    covn = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex(r"^(Translator 🌍|Переводчик 🌍|Tarjimon 🌍)$"),
            transletor_handler
        )
    ],
    states={
        TRANSLATE: [
            CallbackQueryHandler(check_call),
                MessageHandler(Filters.text & ~Filters.command, tr)],
        CHECK_TR: [
            CallbackQueryHandler(change_transletor_callback)
        ],
    },
    fallbacks=[
        MessageHandler(Filters.regex(r"^(Settings ⚙️|Настройки ⚙️|Sozlamalar ⚙️)$"), exit_translator_fallback),
        MessageHandler(Filters.regex(r"^(Help ❓|Помощь ❓|Yordam ❓)$"), exit_translator_fallback),
        MessageHandler(Filters.regex(r"^(Dictionary 📚|Словарь 📚|Lug'at 📚)$"), exit_translator_fallback),
        MessageHandler(Filters.regex(r"^(Search 🔎|Поиск 🔎|Qidirish 🔎)$"), exit_translator_fallback),
        CommandHandler("start", start_command_fallback),
        CommandHandler("help", help_command_fallback),
        MessageHandler(Filters.command, exit_translator_fallback),
    ],
    per_message=False,
    )
    dp.add_handler(covn)
