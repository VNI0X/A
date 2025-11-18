from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import random
import asyncio
from pyrogram.types import ReplyKeyboardRemove

# ==========================
API_ID = 24168862
API_HASH = "916a9424dd1e58ab7955001ccc0172b3"
BOT_TOKEN = "8043728681:AAEjbMWi0SQTro4vB1xeyhKPQssLJ_PL59I"
OWNER_ID = 6183523384
# ==========================

app = Client(
    "aviator-bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Store user data temporarily for callback handling
user_data = {}
# Store player IDs
player_ids = {}
# Store user states (to know if we're waiting for player ID)
user_states = {}
# Store processing messages to edit later
processing_messages = {}

# from telegram import ReplyKeyboardRemove

@app.on_message(filters.command("remove"))
async def remove_keyboard(client, message):
    await message.reply(
        "✅ NEXT ROUND 💸 button hata diya gaya!",
        reply_markup=ReplyKeyboardRemove()
    )
    
# ✅ START COMMAND
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "❌ No Username"

    # Owner ko notify karega
    try:
        await client.send_message(
            OWNER_ID,
            f"🔔 ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ!\n\n🆔 ɪᴅ: {user_id}\n👤 ᴜsᴇʀɴᴀᴍᴇ: @{username}"
        )
    except Exception as e:
        print(f"Error notifying owner: {e}")

    # User ke liye welcome text
    welcome_text = (
        "🎯 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀᴠɪᴀᴛᴏʀ ʜᴀᴄᴋ ʙᴏᴛ! 🎯\n\n"
        "🚀 ᴏᴜʀ 8 ʏᴇᴀʀs ᴏғ ᴛʀᴀᴅɪɴɢ ᴇxᴘᴇʀᴛɪsᴇ ɢᴜᴀʀᴀɴᴛᴇᴇs ᴘʀᴏғɪᴛᴀʙʟᴇ sɪɢɴᴀʟs ᴀɴᴅ "
        "ᴅᴇᴘᴏsɪᴛ ᴘʀᴏᴍᴏ ᴄᴏᴅᴇs. 💵\n\n"
        "✨ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇɢɪsᴛᴇʀ ᴀɴᴅ sᴛᴀʀᴛ ᴡɪɴɴɪɴɢ! 👇️"
    )

    buttons = [
        [InlineKeyboardButton("ʀᴇɢɪsᴛᴇʀ ᴀɴᴅ ᴅᴇᴘᴏsɪᴛ", callback_data="home")],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="http://t.me/Jassan13th")]
    ]

    try:
        await message.reply_photo(
            photo="https://graph.org/file/3e3a889110da791d320d4-5aad5ef4fe56b20c48.jpg",
            caption=welcome_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        # Fallback to text message if photo fails
        print(f"Error sending photo: {e}")
        await message.reply(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ✅ Register Button Handle
@app.on_callback_query(filters.regex("register"))
async def register_callback(client, callback_query):
    await callback_query.answer()
    await callback_query.message.reply(
        "📤 ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴅᴇᴘᴏsɪᴛ sᴄʀᴇᴇɴsʜᴏᴛ ʜᴇʀᴇ ✅"
    )

# ✅ Screenshot Handle - Request Player ID
@app.on_message(filters.photo)
async def handle_screenshot(client, message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "❌ No Username"

    try:
        # Store the screenshot temporarily and request player ID
        user_states[user_id] = {
            "waiting_for_player_id": True,
            "photo_id": message.photo.file_id,
            "message_id": message.id
        }
        
        await message.reply("✅ sᴄʀᴇᴇɴsʜᴏᴛ ʀᴇᴄᴇɪᴠᴇᴅ! ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʟᴀʏᴇʀ ɪᴅ.")

    except Exception as e:
        print(f"Error handling screenshot: {e}")
        await message.reply("⚠️ sᴏʀʀʏ, ᴛʜᴇʀᴇ ᴡᴀs ᴀɴ ᴇʀʀᴏʀ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")

# ✅ Home Button Handle - Edit message with new buttons
@app.on_callback_query(filters.regex("home"))
async def home_callback(client, callback_query):
    await callback_query.answer()
    
    # New text and buttons for the home screen
    home_text = (
        "🏠 **Home**\n\n"
        "Select an option to continue:"
    )
    
    # Fixed: Use WebAppInfo object instead of string
    home_buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "ʀᴇɢɪsᴛᴇʀ",
                web_app=WebAppInfo(url="https://jalappwa2.com/#/register?invitationCode=84673101184")
            ),
            InlineKeyboardButton("sᴛᴀʀᴛ ɢᴀᴍᴇ", callback_data="register")
        ],
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_start")
        ]
    ]
)
    
    # Edit the message with new content
    await callback_query.edit_message_caption(
        caption=home_text,
        reply_markup=home_buttons
        
    )

# ✅ Back to Start Button Handle
@app.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client, callback_query):
    await callback_query.answer()
    
    # Original welcome text
    welcome_text = (
        "🎯 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀᴠɪᴀᴛᴏʀ ʜᴀᴄᴋ ʙᴏᴛ! 🎯\n\n"
        "🚀 ᴏᴜʀ 8 ʏᴇᴀʀs ᴏғ ᴛʀᴀᴅɪɴɢ ᴇxᴘᴇʀᴛɪsᴇ ɢᴜᴀʀᴀɴᴛᴇᴇs ᴘʀᴏғɪᴛᴀʙʟᴇ sɪɢɴᴀʟs ᴀɴᴅ "
        "ᴅᴇᴘᴏsɪᴛ ᴘʀᴏᴍᴏ ᴄᴏᴅᴇs. 💵\n\n"
        "✨ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇɢɪsᴛᴇʀ ᴀɴᴅ sᴛᴀʀᴛ ᴡɪɴɴɪɴɢ! 👇️"
    )

    buttons = [
        [InlineKeyboardButton("ʀᴇɢɪsᴛᴇʀ ᴀɴᴅ ᴅᴇᴘᴏsɪᴛ", callback_data="home")],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="http://t.me/Jassan13th")]
    ]
    
    # Edit the message back to the original start screen
    await callback_query.edit_message_caption(
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
def is_player_id_input(_, __, message):
    # Ye filter check karega ki user normal text bhej raha hai, command nahi
    return message.text and not message.text.startswith("/")

# ✅ Handle Player ID after screenshot
@app.on_message(filters.text & filters.create(is_player_id_input))
async def handle_player_id(client, message):
    user_id = message.from_user.id
    
    # Check if we're waiting for player ID from this user
    if user_id in user_states and user_states[user_id].get("waiting_for_player_id"):
        player_id = message.text.strip()
        username = message.from_user.username if message.from_user.username else "❌ No Username"
        
        # Store both screenshot and player ID
        user_data[str(message.id)] = {
            "user_id": user_id,
            "username": username,
            "photo_id": user_states[user_id]["photo_id"],
            "player_id": player_id
        }
        
        # Create confirmation buttons
        confirm_buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{message.id}"),
                InlineKeyboardButton("❌ Decline", callback_data=f"decline_{message.id}")
            ]
        ])
        
        # ✅ Owner ko photo send karo with player ID and buttons
        await client.send_photo(
            OWNER_ID,
            photo=user_states[user_id]["photo_id"],
            caption=f"📸 ɴᴇᴡ sᴄʀᴇᴇɴsʜᴏᴛ!\n\n🆔 {user_id}\n👤 @{username}\n🎮 ᴘʟᴀʏᴇʀ ɪᴅ: {player_id}",
            reply_markup=confirm_buttons
        )

        await message.reply("⏳ ʏᴏᴜʀ sᴄʀᴇᴇɴsʜᴏᴛ ᴀɴᴅ ᴘʟᴀʏᴇʀ ɪᴅ ʜᴀᴠᴇ ʙᴇᴇɴ sᴇɴᴛ ғᴏʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ✅")
        
        # Clear the waiting state
        del user_states[user_id]

# ✅ Handle Confirm/Decline Callbacks
@app.on_callback_query(filters.regex(r"^(confirm|decline)_"))
async def handle_confirmation(client, callback_query):
    try:
        # Extract data from callback
        data_parts = callback_query.data.split("_")
        action = data_parts[0]
        message_id = data_parts[1]
        
        user_info = user_data.get(message_id)
        
        if not user_info:
            await callback_query.answer("❌ This request has expired or already processed", show_alert=True)
            return
            
        user_id = user_info["user_id"]
        username = user_info["username"]
        player_id = user_info["player_id"]
        
        if action == "confirm":
            # Store player ID permanently
            player_ids[str(user_id)] = player_id
            
            # Send confirmation to user with NEXT ROUND button
            await client.send_message(
      user_id,
    (
        "🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!\n"
        "ʏᴏᴜʀ ᴅᴇᴘᴏsɪᴛ ɪs ᴄᴏɴғɪʀᴍᴇᴅ ✅\n"
        f"ʏᴏᴜʀ ᴘʟᴀʏᴇʀ ɪᴅ ({player_id}) ʜᴀs ʙᴇᴇɴ sᴀᴠᴇᴅ\n"
        "ʏᴏᴜ ᴡɪʟʟ sᴛᴀʀᴛ ʀᴇᴄᴇɪᴠɪɴɢ ᴠɪᴘ sɪɢɴᴀʟs sᴏᴏɴ 🚀"
    )
            )
            # Notify owner
            await callback_query.edit_message_caption(
                f"✅ CONFIRMED\n\n📸 Screenshot from:\n🆔 {user_id}\n👤 @{username}\n🎮 Player ID: {player_id}"
            )
            
            await callback_query.answer("User confirmed successfully!")
            
        elif action == "decline":
            # Send rejection to user
            await client.send_message(
                user_id,
                "❌ ʏᴏᴜʀ sᴄʀᴇᴇɴsʜᴏᴛ ᴡᴀs ɴᴏᴛ ᴀᴄᴄᴇᴘᴛᴇᴅ. ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴘɴ."
            )
            
            # Notify owner
            await callback_query.edit_message_caption(
                f"❌ DECLINED\n\n📸 Screenshot from:\n🆔 {user_id}\n👤 @{username}\n🎮 Player ID: {player_id}"
            )
            
            await callback_query.answer("User declined!")
        
        # Remove from temporary storage
        if message_id in user_data:
            del user_data[message_id]
            
    except Exception as e:
        print(f"Error in confirmation: {e}")
        await callback_query.answer("An error occurred", show_alert=True)


# ✅ Owner confirm command (backup)
@app.on_message(filters.command("confirm") & filters.user(OWNER_ID))
async def confirm_user(client, message):
    try:
        target_id = int(message.text.split(" ")[1])
        player_id = message.text.split(" ")[2] if len(message.text.split(" ")) > 2 else "N/A"
        
        # Store player ID
        player_ids[str(target_id)] = player_id
        
        # Send confirmation to user with NEXT ROUND button
        await client.send_message(
      user_id,
    (
        "🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!\n"
        "ʏᴏᴜʀ ᴅᴇᴘᴏsɪᴛ ɪs ᴄᴏɴғɪʀᴍᴇᴅ ✅\n"
        f"ʏᴏᴜʀ ᴘʟᴀʏᴇʀ ɪᴅ ({player_id}) ʜᴀs ʙᴇᴇɴ sᴀᴠᴇᴅ\n"
        "ʏᴏᴜ ᴡɪʟʟ sᴛᴀʀᴛ ʀᴇᴄᴇɪᴠɪɴɢ ᴠɪᴘ sɪɢɴᴀʟs sᴏᴏɴ 🚀"
    )
        )
        await message.reply(f"☑️ ᴜsᴇʀ {target_id} ᴄᴏɴғɪʀᴍᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴡɪᴛʜ ᴘʟᴀʏᴇʀ ɪᴅ: {player_id}")
    except:
        await message.reply("⚠️ ᴜsᴀɢᴇ: /confirm user_id player_id")

# ✅ Test Command (Owner Only)
@app.on_message(filters.command("test") & filters.user(OWNER_ID))
async def test_owner(client, message):
    await message.reply("✅ ʙᴏᴛ ɪs ᴀʙʟᴇ ᴛᴏ sᴇɴᴅ ᴍᴇssᴀɢᴇs ᴛᴏ ʏᴏᴜ.")

if __name__ == "__main__":
    print("🤖 Aviator Bot Running...")
    app.run()
