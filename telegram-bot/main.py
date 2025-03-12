import logging
import os
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
import firebase_admin
from firebase_admin import credentials, auth

# Firebase initialization
cred = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred)
API_KEY = 'AIzaSyCoNPITPZ2zko2WpKPs0ZH6WloAn8GVxrY'

# Telegram bot token
TOKEN = '7819216862:AAFPFOXjpBncG7oNXZFeD1QCZ410NcF3dN0'

# API endpoints
UPLOAD_FILE_API = "http://localhost:8000/api/v1/file_manager/upload_file"
LIST_FILES_API = "http://localhost:8000/api/v1/file_manager/list_files"
DOWNLOAD_FILE_API = "http://localhost:8000/api/v1/file_manager/download_file"

# User session storage
user_sessions = {}

# Conversation states
LOGIN_EMAIL, LOGIN_PASSWORD, UPLOAD_FILE = range(3)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /login to authenticate.')

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your email:")
    return LOGIN_EMAIL

async def login_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    await update.message.reply_text("Enter your password:")
    return LOGIN_PASSWORD

async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    password = update.message.text
    email = context.user_data['email']
    
    try:
        # Authenticate user with Firebase
        user = auth.get_user_by_email(email)
        user_id = update.effective_user.id
        
        # Verify password by signing in (you may use a custom backend or Firebase Auth REST API)
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            user_data = response.json()
            user_sessions[user_id] = user_data['idToken']
            await update.message.reply_text("✅ Login successful!")
        else:
            await update.message.reply_text("❌ Login failed. Check credentials and try again.")
    except Exception as e:
        logger.error(f"Error during login: {e}")
        await update.message.reply_text("❌ Login failed. Check credentials and try again.")
    
    return ConversationHandler.END

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
        await update.message.reply_text("✅ Logged out successfully.")
    else:
        await update.message.reply_text("You are not logged in.")

async def view_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        await update.message.reply_text("Please login first.")
        return
    
    token = user_sessions[user_id]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(LIST_FILES_API, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            
            if isinstance(data, list):
                files = [item.get("file_name") for item in data if "file_name" in item]
                
                if files:
                    await update.message.reply_text("Available files:\n" + "\n".join(files))
                else:
                    await update.message.reply_text("No files found.")
            else:
                await update.message.reply_text("❌ Unexpected API response format. Expected a list of files.")
        except Exception as e:
            logger.error(f"Error parsing API response: {e}")
            await update.message.reply_text("❌ Failed to parse API response.")
    else:
        await update.message.reply_text("❌ Failed to fetch files.")

async def upload_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please send the file to upload.")
    return UPLOAD_FILE

async def handle_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        await update.message.reply_text("Please login first.")
        return ConversationHandler.END
    
    document = update.message.document
    if not document:
        await update.message.reply_text("Please send a valid file.")
        return ConversationHandler.END
    
    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(os.getcwd(), document.file_name)
    await file.download_to_drive(file_path)
    
    token = user_sessions[user_id]
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, 'rb') as f:
        files = {'file': (document.file_name, f)}
        response = requests.post(UPLOAD_FILE_API, headers=headers, files=files)
    
    os.remove(file_path)
    
    if response.status_code == 200:
        await update.message.reply_text(f"✅ File {document.file_name} uploaded successfully!")
    else:
        await update.message.reply_text("❌ File upload failed.")
    
    return ConversationHandler.END

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        await update.message.reply_text("Please login first.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /download <filename>")
        return
    
    filename = context.args[0]
    token = user_sessions[user_id]
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        list_response = requests.get(LIST_FILES_API, headers=headers)
        
        if list_response.status_code != 200:
            await update.message.reply_text("❌ Failed to fetch file metadata.")
            return
        
        files_metadata = list_response.json()
        file_info = next((item for item in files_metadata if item.get("file_name") == filename), None)
        
        if not file_info:
            await update.message.reply_text(f"❌ File '{filename}' not found.")
            return
        
        file_id = file_info.get("uid")
        
        download_params = {"file_id": file_id}
        download_response = requests.get(DOWNLOAD_FILE_API, headers=headers, params=download_params)
        
        if download_response.status_code == 200:
            temp_filename = os.path.join(os.getcwd(), filename)
            with open(temp_filename, "wb") as f:
                f.write(download_response.content)

            with open(temp_filename, "rb") as f:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=f)

            os.remove(temp_filename)
        else:
            await update.message.reply_text("❌ File download failed.")
    
    except Exception as e:
        logger.error(f"Error during file download: {e}")
        await update.message.reply_text("❌ An error occurred while downloading the file.")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        await update.message.reply_text("You are not logged in.")
        return
    
    token = user_sessions[user_id]
    
    try:
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get("email")
        
        if email:
            await update.message.reply_text(
                f"✅ Logged in as:\n"
                f"Email: {email}\n"
            )
        else:
            await update.message.reply_text("❌ Unable to retrieve account details.")
    except Exception as e:
        logger.error(f"Error verifying Firebase token: {e}")
        await update.message.reply_text("❌ Failed to verify your session. Please log in again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
        Available Commands:
        /start - Show welcome message
        /login - Authenticate with email and password
        /whoami - Check the current session
        /logout - Log out of the current session
        /view - List all available files
        /upload - Upload a new file
        /download <filename> - Download a file by name
        /help - Show this help message
        /cancel - Cancel current operation
    """
    await update.message.reply_text(help_text)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login_start)],
        states={
            LOGIN_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_email)],
            LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    upload_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', upload_start)],
        states={
            UPLOAD_FILE: [MessageHandler(filters.Document.ALL, handle_upload)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(login_conv_handler)
    application.add_handler(upload_conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("logout", logout))
    application.add_handler(CommandHandler("view", view_files))
    application.add_handler(CommandHandler("download", download_file))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("whoami", whoami))

    application.run_polling()

if __name__ == '__main__':
    main()