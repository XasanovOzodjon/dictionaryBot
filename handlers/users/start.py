from telegram.ext import (
    CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, Filters
)
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.check_subscribe import subscription_required
from keyboards.default.menu_keyboard import get_menu_keyboard
from keyboards.inline.language import language_keyboard
from keyboards.inline.translate_languages import create_translate_to_keyboard
from states.start import LANGUAGE, TRANSLATE_TO, USE_TOG, AI_ASSISTANT
from models.users import User
from models.settings import User_Settings
from data import get_db
import logging


@subscription_required
def bot_start(update, context):
    """Foydalanuvchi /start bosganda ishlaydi"""
    logging.info(f"Start handler called for user {update.effective_user.id}")
    user_id = update.effective_user.id
    session = next(get_db())
    
    try:
        # Foydalanuvchi tekshirish
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            user = User(
                telegram_id=user_id,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
                username=update.effective_user.username
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            text = f"👋 Welcome {user.first_name}!\nTo get started, please select your preferred language:"
            reply_markup = language_keyboard
            
            # Xabar jo'natish
            if update.message:
                update.message.reply_text(text, reply_markup=reply_markup)
            elif update.callback_query:
                update.callback_query.edit_message_text(text, reply_markup=reply_markup)
            
            return LANGUAGE

        # Foydalanuvchi bor, ammo settings yo'q
        settings = session.query(User_Settings).filter_by(from_user=user_id).first()
        if not settings:
            text = f"👋 Welcome {user.first_name}! To continue, please select your preferred language:"
            reply_markup = language_keyboard
            
            # Xabar jo'natish
            if update.message:
                update.message.reply_text(text, reply_markup=reply_markup)
            elif update.callback_query:
                update.callback_query.edit_message_text(text, reply_markup=reply_markup)
            
            return LANGUAGE

        if settings.language == "en":
            text = f"👋 Welcome {user.first_name}! You in main menu."
        elif settings.language == "ru":
            text = f"👋 Добро пожаловать {user.first_name}! Вы в главном меню."
        else:
            text = f"👋 Xush kelibsiz {user.first_name}! Siz asosiy menyudasiz."

        reply_markup = get_menu_keyboard(settings.language)

        if update.message:
            update.message.reply_text(text, reply_markup=reply_markup)
        elif update.callback_query:
            update.callback_query.edit_message_text(text, reply_markup=reply_markup)

        return ConversationHandler.END
        
    finally:
        session.close()


def get_language(update, context):
    """Foydalanuvchi interfeys tilini tanladi"""
    db = next(get_db())
    user_id = update.effective_user.id
    selected_language = update.callback_query.data

    try:
        # User_Settings yaratish
        new_settings = User_Settings(
            from_user=user_id,
            language=selected_language,
        )
        db.add(new_settings)
        db.commit()
        context.user_data['language'] = selected_language

        # Til tanlangandan keyin translate_to tilini tanlashni so'rash
        if selected_language == "en":
            text = "🌍 Select the target language to translate into:"
        elif selected_language == "ru":
            text = "🌍 Выберите целевой язык для перевода:"
        else:
            text = "🌍 Tarjimon qaysi tilga tarjima qilsin:"

        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=create_translate_to_keyboard()
        )
        return TRANSLATE_TO
        
    finally:
        db.close()


def get_translate_to(update, context):
    """Foydalanuvchi translate_to tilini tanlaganda ishlaydi"""
    db = next(get_db())
    user_id = update.effective_user.id
    callback_data = update.callback_query.data

    try:
        if callback_data.startswith("translate_to_"):
            selected_language = callback_data.replace("translate_to_", "")
            user_settings = db.query(User_Settings).filter_by(from_user=user_id).first()
            if user_settings:
                user_settings.translate_to = selected_language
                db.commit()

            update.callback_query.answer()
            if user_settings and user_settings.language == "en":
                success_text = "Great! Do you use the TOG method ❓"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("yes", callback_data="use_tog_yes"), InlineKeyboardButton("no", callback_data="use_tog_no")],
                    [InlineKeyboardButton("What is Tog metod", callback_data="tog_info")]
                ])
            elif user_settings and user_settings.language == "ru":
                success_text = "Отлично! Используете ли вы метод TOG ❓"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Да", callback_data="use_tog_yes"), InlineKeyboardButton("нет", callback_data="use_tog_no")],
                    [InlineKeyboardButton("Что такое метод Tog", callback_data="tog_info")]
                ])
            else:
                success_text = "Ajoyib! Siz TOG usulidan foydalanasizmi ❓"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Ha", callback_data="use_tog_yes"), InlineKeyboardButton("Yo'q", callback_data="use_tog_no")],
                    [InlineKeyboardButton("Tog usuli nima?", callback_data="tog_info")]
                ])

            update.callback_query.edit_message_text(
                text=success_text,
                reply_markup=keyboard
            )
            return USE_TOG

        elif callback_data.startswith("page_"):
            # Handle page navigation - default translate_to_ context for start handler
            page = int(callback_data.replace("page_to", ""))
            try:
                update.callback_query.edit_message_reply_markup(
                    reply_markup=create_translate_to_keyboard(page=page, text='translate_to_')
                )
            except Exception:
                # If keyboard update fails (e.g., same content), just continue
                pass
            update.callback_query.answer()
            return TRANSLATE_TO

        elif callback_data == "page_info":
            update.callback_query.answer()
            return TRANSLATE_TO
            
    finally:
        db.close()

def handle_use_tog(update, context):
    """Foydalanuvchi TOG usulidan foydalanishini tanlaganda ishlaydi"""
    db = next(get_db())
    user_id = update.effective_user.id
    callback_data = update.callback_query.data

    try:
        user_settings = db.query(User_Settings).filter_by(from_user=user_id).first()
        if callback_data == "tog_info":
            if user_settings and user_settings.language == "en":
                info_text = "TOG metod is ...\nDo you use the TOG method ❓"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("yes", callback_data="use_tog_yes"), InlineKeyboardButton("no", callback_data="use_tog_no")],
                ])
            elif user_settings and user_settings.language == "ru":
                info_text = "TOG metod is ...\nИспользуете ли вы метод TOG ❓"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Да", callback_data="use_tog_yes"), InlineKeyboardButton("нет", callback_data="use_tog_no")],
                ])
            else:
                info_text = "TOG metod is ...\nSiz TOG usulidan foydalanasizmi ❓"
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Ha", callback_data="use_tog_yes"), InlineKeyboardButton("Yo'q", callback_data="use_tog_no")],
                ])
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=info_text,
                reply_markup=keyboard
                )
            return USE_TOG
        
        if user_settings:
            if callback_data == "use_tog_yes":
                user_settings.use_TOG = True
            elif callback_data == "use_tog_no":
                user_settings.use_TOG = False
            db.commit()

        update.callback_query.answer()
        if user_settings and user_settings.language == "en":
            success_text = "Great! Do you use AI assistant?"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes", callback_data="ai_assistant_yes"), InlineKeyboardButton("No", callback_data="ai_assistant_no")],
            ])
        elif user_settings and user_settings.language == "ru":
            success_text = "Отлично! Вы используете AI помощника?"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Да", callback_data="ai_assistant_yes"), InlineKeyboardButton("Нет", callback_data="ai_assistant_no")],
            ])
        else:
            success_text = "Ajoyib! Siz AI yordamchisidan foydalanasizmi?"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Ha", callback_data="ai_assistant_yes"), InlineKeyboardButton("Yo'q", callback_data="ai_assistant_no")],
            ])
        update.callback_query.edit_message_text(
            text=success_text,
            reply_markup=keyboard
        )
        return AI_ASSISTANT

    finally:
        db.close()
        
def handle_ai_assistant(update, context):
    """Foydalanuvchi AI yordamchisidan foydalanishini tanlaganda ishlaydi"""
    db = next(get_db())
    user_id = update.effective_user.id
    callback_data = update.callback_query.data

    try:
        user_settings = db.query(User_Settings).filter_by(from_user=user_id).first()
        if user_settings:
            if callback_data == "ai_assistant_yes":
                user_settings.ai_assistant = True
            elif callback_data == "ai_assistant_no":
                user_settings.ai_assistant = False
            db.commit()
        update.callback_query.answer()
        if user_settings and user_settings.language == "en":
            success_text = "Setup complete!"
        elif user_settings and user_settings.language == "ru":
            success_text = "Настройка завершена!"
        else:
            success_text = "Sozlamalar yakunlandi!"
        
        # Edit message to remove inline keyboard
        update.callback_query.edit_message_text(
            text=success_text,
            reply_markup=None
        )
        
        # Send menu keyboard as a reply keyboard
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Menu:",
            reply_markup=get_menu_keyboard(user_settings.language)
        )
        return ConversationHandler.END
    finally:
        db.close()


   
def register_handlers(dp):
    """ConversationHandler va boshqa handlerlarni ro'yxatdan o'tkazish"""
    start_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot_start)],
        states={
            LANGUAGE: [CallbackQueryHandler(get_language)],
            TRANSLATE_TO: [CallbackQueryHandler(get_translate_to)],
            USE_TOG: [CallbackQueryHandler(handle_use_tog)],
            AI_ASSISTANT: [CallbackQueryHandler(handle_ai_assistant)],
        },
        fallbacks=[CommandHandler("start", bot_start)],
        per_message=False,
    )
    dp.add_handler(start_handler)
    dp.add_handler(MessageHandler(Filters.text(['🔙 Orqaga', '🔙 Back', '🔙 Назад']), bot_start))