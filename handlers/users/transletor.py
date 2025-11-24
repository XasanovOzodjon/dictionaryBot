# standard imports
import threading

# pip imports
from googletrans import Translator
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler

# local imports
from data import get_db
from states.start import TRANSLATE, CHECK_TR
from utils.users_servise import UserUpdate, get_settings
from keyboards.default.menu_keyboard import get_menu_keyboard
from keyboards.inline.transletor import get_transletor_keyborad
from keyboards.inline.translate_languages import create_translate_to_keyboard


def transletor_handler(update: Update, context: CallbackContext):
    # Check if user data exists and has language setting
    if not context.user_data or not context.user_data.get('language'):
        update.message.reply_text("Please start the bot using /start command.")
        return
    
    # Update user data if needed
    if not context.user_data:
        UserUpdate(update, context)
    
    
    lang = context.user_data.get('language')

    if lang == 'en':
        text = "Translator:"
    elif lang == 'ru':
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
        reply_markup=get_transletor_keyborad(t_from=context.user_data.get('translate_from'), t_to=context.user_data.get('translate_to'), lang=context.user_data.get('language'))
    )
    return TRANSLATE


def tr(update: Update, context: CallbackContext):
    
    if not context.user_data:
        UserUpdate(update, context)
        
    text = update.message.text
    from_user = context.user_data.get('translate_from')
    to_tr = context.user_data.get('translate_to')
    translator = Translator()
    result = translator.translate(f"{text}", src=f'{from_user}', dest=f'{to_tr}')
    
    update.message.reply_text(result.text)
    return TRANSLATE


def check_call(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    if not context.user_data:
        UserUpdate(update, context)
    
    lang = context.user_data.get('language')
    
    if query_data == "close_transletor":
        update.callback_query.message.delete()
        update.callback_query.answer()

        if lang == 'en':
            menu_text = "Main Menu:"
        elif lang == 'ru':
            menu_text = "Главное меню:"
        else:
            menu_text = "Asosiy menu:"
        
        update.effective_message.bot.send_message(
            chat_id=update.effective_chat.id,
            text=menu_text,
            reply_markup=get_menu_keyboard(lang)
        )
        query.answer()
        return ConversationHandler.END
    elif query_data in ['change_from', 'change_to', 'change_toto']:
        if query_data == "change_toto":
            with next(get_db()) as db:
                user_settings = get_settings(update.effective_user.id)

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
                UserUpdate(update, context)
                
                # Update the keyboard with new settings
                try:
                    query.edit_message_reply_markup(reply_markup=get_transletor_keyborad(t_from=context.user_data.get('translate_from'), t_to=context.user_data.get('translate_to'), lang=context.user_data.get('language')))
                    query.answer("Tarjima tillari almashtirildi!")
                except Exception:
                    # If keyboard update fails (e.g., same content), just answer the query
                    query.answer("Tarjima tillari almashtirildi!")
                return TRANSLATE
        
        if query_data == "change_to":
            with next(get_db()) as db:
                user_settings = get_settings(update.effective_user.id)
                
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
                user_settings = get_settings(update.effective_user.id)
                
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

    user_settings = get_settings(update.effective_user.id)
    
    if query_data.startswith("translate_from_"):
        new_from_lang = query_data.replace("translate_from_", "")
        with next(get_db()) as db:
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.translate_from = new_from_lang
            
            # Save changes to database
            db.commit()
            UserUpdate(update, context)

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
                reply_markup=get_transletor_keyborad(t_from=context.user_data.get('translate_from'), t_to=context.user_data.get('translate_to'), lang=context.user_data.get('language')))
            return TRANSLATE
        
    if query_data.startswith("translate_to_"):
        new_to_lang = query_data.replace("translate_to_", "")
        with next(get_db()) as db:
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.translate_to = new_to_lang
            db.commit()
            UserUpdate(update, context)
            
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
                reply_markup=get_transletor_keyborad(t_from=context.user_data.get('translate_from'), t_to=context.user_data.get('translate_to'), lang=context.user_data.get('language')))
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
    if not context.user_data:
        UserUpdate(update, context)
    
    lang = context.user_data.get('language')
    
    if lang == 'en':
        menu_text = "Main Menu:"
    elif lang == 'ru':
        menu_text = "Главное меню:"
    else:
        menu_text = "Asosiy menu:"
    
    update.message.reply_text(
        text=menu_text,
        reply_markup=get_menu_keyboard(lang)
    )
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
        CommandHandler("start", lambda update, context: ConversationHandler.END),
        CommandHandler("help", lambda update, context: ConversationHandler.END),
        MessageHandler(Filters.command, exit_translator_fallback),
    ],
    per_message=False,
    )
    dp.add_handler(covn)
