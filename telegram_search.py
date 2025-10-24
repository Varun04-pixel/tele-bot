from telethon import TelegramClient, events
import csv, os, asyncio
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
GROUP_USERNAME = 'absolute_cinema_freaks'  # your public group username
OWNER_ID = int(os.getenv("OWNER_ID"))      # your Telegram user ID
DELETE_AFTER = 100                          # time in seconds

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# --- Search Handler ---
@client.on(events.NewMessage(pattern=r'/search (.+)'))
async def search_handler(event):
    keyword = event.pattern_match.group(1).strip()
    results = []

    try:
        with open('search_results.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                message_text = row['Message']
                if message_text.startswith('/search'):
                    continue
                if keyword.lower() in message_text.lower():
                    results.append(f"{message_text} (Link: https://t.me/{GROUP_USERNAME}/{row['Link'].split('/')[-1]})")
    except FileNotFoundError:
        await event.reply("❌ CSV file not found. Please upload `search_results.csv`.")
        return

    if results:
        reply_text = f"Found {len(results)} result(s) for '{keyword}':\n\n" + "\n\n".join(results[:5])
    else:
        reply_text = f"No results found for '{keyword}'."

    await event.reply(reply_text)

# --- Auto-delete Handler ---
@client.on(events.NewMessage)
async def auto_delete(event):
    # Ignore messages sent by you (the owner)
    if event.sender_id != OWNER_ID:
        await asyncio.sleep(DELETE_AFTER)
        try:
            await event.delete()
        except:
            pass  # ignore if already deleted

print("🤖 Bot is running...")
client.run_until_disconnected()
