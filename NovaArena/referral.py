
# File to store referral data
REFERRAL_FILE = "user_referrals.json"

# Load referral data
if os.path.exists(REFERRAL_FILE):
    with open(REFERRAL_FILE, "r") as f:
        user_referrals = json.load(f)
else:
    user_referrals = {}

# Save referral data
def save_referral_data():
    with open(REFERRAL_FILE, "w") as f:
        json.dump(user_referrals, f)

async def referral_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    referral_link = f"https://t.me/NovaArenaGameBot?start={user_id}"

    # Count the number of referrals
    referrals = user_referrals.get(user_id, {"count": 0, "referred_users": []})
    referral_count = referrals["count"]

    # Create the referral story message
    referral_message = (
        f"🌀 **Your Epic Adventure Begins!** 🌀\n\n"
        f"🌟 **Summon Your Friends!** 🌟\n\n"
        f"🌐 **Your Magic Referral Link:**\n\n"
        f"🪄 {referral_link}\n\n"
        f"🏆 **You have already rallied {referral_count} brave adventurers to join the quest!**\n\n"
        "✨ **The more heroes you bring, the greater your fortune!**\n\n"
        "💰 **Rewards:**\n"
        "For every adventurer who joins using your link, you’ll be granted **10 ⭐️ Nova** to help you conquer even more challenges! 🏅\n\n"
        "🗺 **Referral Adventure:**\n"
        "Track your progress and gather your crew right here in the bot. The bigger your party, the more Nova you'll earn to aid in your journey! 🌠"
    )

    await update.message.reply_text(referral_message)