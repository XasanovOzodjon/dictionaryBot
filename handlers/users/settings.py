# pip imports
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

# local imports
from data import get_db
from states.start import SETTINGS, CHECK_SETTINGS
from keyboards.inline.language import language_keyboard_s
from keyboards.inline.settings import get_settings_keyboard
from middlewares.check_subscribe import subscription_required
from keyboards.default.menu_keyboard import get_menu_keyboard
from keyboards.inline.translate_languages import create_translate_to_keyboard
from utils.users_servise import get_user_and_settings, get_settings, UserUpdate

@subscription_required
def settings_handler(update: Update, context):
    user, user_settings = get_user_and_settings(update.effective_user.id)
    if not context.user_data:
        UserUpdate(update, context)
    
    if not user or not user_settings:
        update.message.reply_text("Please start the bot using /start command.")
        return ConversationHandler.END

    if user_settings.language == 'en':
        text = "Settings:"
    elif user_settings.language == 'ru':
        text = "Настройки:"
    else:  # Uzbek
        text = "Sozlamalar:"

    update.message.reply_text(text, reply_markup=get_settings_keyboard(user_settings))
    return SETTINGS
    
def check_settings_callback(update: Update, context):
    query = update.callback_query
    query_data = query.data
    user_settings = get_settings(update.effective_user.id)
    
    if not context.user_data:
        UserUpdate(update, context)

    if query_data == "None":
        query.answer()
        return SETTINGS
    if query_data == "enable_tog":
        with next(get_db()) as db:
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.use_TOG = True
            
            # Save changes to database
            db.commit()
            UserUpdate(update, context)

            try:
                query.edit_message_reply_markup(reply_markup=get_settings_keyboard(user_settings))
            except Exception:
                # If keyboard update fails (e.g., same content), just continue
                pass
            return SETTINGS
    if query_data == "disable_tog":
        with next(get_db()) as db:
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.use_TOG = False
            
            # Save changes to database
            db.commit()
            UserUpdate(update, context)
            
            try:
                query.edit_message_reply_markup(reply_markup=get_settings_keyboard(user_settings))
            except Exception:
                # If keyboard update fails (e.g., same content), just continue
                pass
            return SETTINGS
    if query_data == "enable_ai":
        with next(get_db()) as db:
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.ai_assistant = True
            db.commit()
            UserUpdate(update, context)
            try:
                query.edit_message_reply_markup(reply_markup=get_settings_keyboard(user_settings))
            except Exception:
                # If keyboard update fails (e.g., same content), just continue
                pass
            return SETTINGS
    if query_data == "disable_ai":
        with next(get_db()) as db:
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.ai_assistant = False
            db.commit()
            UserUpdate(update, context)
            try:
                query.edit_message_reply_markup(reply_markup=get_settings_keyboard(user_settings))
            except Exception:
                # If keyboard update fails (e.g., same content), just continue
                pass
            return SETTINGS
    if query_data == "close_settings":
        update.callback_query.message.delete()
        update.callback_query.answer()
        update.effective_message.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Main Menu:",
            reply_markup=get_menu_keyboard(user_settings.language)
        )
        return ConversationHandler.END
    if query_data == "change_from":
        with next(get_db()) as db:
            
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
            return CHECK_SETTINGS   
    if query_data == "change_toto":
        with next(get_db()) as db:
            user_settings = get_settings(update.effective_user.id)

            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            
            # Check if there's actually a change to make
            if user_settings.translate_from == user_settings.translate_to:
                query.answer("Tillalar allaqachon bir xil!")
                return SETTINGS
            
            temp = user_settings.translate_from
            user_settings.translate_from = user_settings.translate_to
            if temp != 'auto':
                user_settings.translate_to = temp
            
            # Save changes to database
            db.commit()
            UserUpdate(update, context)
            # Update the keyboard with new settings
            try:
                query.edit_message_reply_markup(reply_markup=get_settings_keyboard(user_settings))
                query.answer("Tarjima tillari almashtirildi!")
            except Exception:
                # If keyboard update fails (e.g., same content), just answer the query
                query.answer("Tarjima tillari almashtirildi!")
            return SETTINGS   
    if query_data == "change_to":
        with next(get_db()) as db:
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
            return CHECK_SETTINGS
    if query_data == "close_settings":
        with next(get_db()) as db:
            user_settings = db.merge(user_settings)
            
            update.callback_query.message.delete()
            update.callback_query.answer()
            
            # Send main menu based on language
            if user_settings.language == 'en':
                text = "Main Menu:"
            elif user_settings.language == 'ru':
                text = "Главное меню:"
            else:  # Uzbek
                text = "Asosiy menu:"
                
            update.effective_message.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=get_menu_keyboard(user_settings.language)
            )
            return ConversationHandler.END    
    if query_data == "change_lang":
        with next(get_db()) as db:

            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            if user_settings.language == 'en':
                text = "choice your language:"
            elif user_settings.language == 'ru':
                text = "выберите ваш язык:"
            else:  # Uzbek
                text = "Tilni tanlang:"
            query.edit_message_text(
                text=text,
                reply_markup=language_keyboard_s
                )
            return CHECK_SETTINGS
            
    query.answer()
    
def change_settings_callback(update: Update, context):
    query = update.callback_query
    query_data = query.data
    user_settings = get_settings(update.effective_user.id)
    if not context.user_data:
        UserUpdate(update, context)
            
    if query_data in ['eng', 'rus', 'uzb']:
        if query_data == 'eng':
            new_lang = 'en'
        elif query_data == 'rus':
            new_lang = 'ru'
        elif query_data == 'uzb':
            new_lang = 'uz'
        with next(get_db()) as db:
            
            # Merge the object into current session to avoid session conflicts
            user_settings = db.merge(user_settings)
            user_settings.language = new_lang
            
            # Save changes to database
            db.commit()
            UserUpdate(update, context)
            if new_lang == 'en':
                text = "Settings:"
            elif new_lang == 'ru':
                text = "Настройки:"
            else:
                text = "Sozlamalar:"
            query.edit_message_text(
                text=text,
                reply_markup=get_settings_keyboard(user_settings)
                )
        return SETTINGS
    
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
                text = "Settings:"
            elif user_settings.language == 'ru':
                text = "Настройки:"
            else:
                text = "Sozlamalar:"
            query.edit_message_text(
                text=text,
                reply_markup=get_settings_keyboard(user_settings))
            return SETTINGS

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
                text = "Settings:"
            elif user_settings.language == 'ru':
                text = "Настройки:"
            else:
                text = "Sozlamalar:"
            query.edit_message_text(
                text=text,
                reply_markup=get_settings_keyboard(user_settings))
            return SETTINGS
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
            return CHECK_SETTINGS

    elif query_data == "page_info":
        update.callback_query.answer()
        return CHECK_SETTINGS
        
def register_handlers(dp):
    covn_hendler = ConversationHandler(
        entry_points=[CommandHandler("settings", settings_handler),
                      MessageHandler(Filters.text("Settings ⚙️"), settings_handler),
                      MessageHandler(Filters.text("Настройки ⚙️"), settings_handler),
                      MessageHandler(Filters.text("Sozlamalar ⚙️"), settings_handler)],
        states={
            SETTINGS: [CallbackQueryHandler(check_settings_callback)],
            CHECK_SETTINGS: [CallbackQueryHandler(change_settings_callback)],
        },
        fallbacks=[
            MessageHandler(Filters.text, lambda update, context: ConversationHandler.END),
        ],
        per_message=False,
    )
    dp.add_handler(covn_hendler)