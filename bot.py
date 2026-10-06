import telebot
from telebot import types

# --- 🛠 ያንተ መረጃዎች ---
API_TOKEN = '8693308102:AAFS-b4om4C8r6IgCD6GQ__Jo7yKHheOUT4'
ADMIN_ID = 1477437632

bot = telebot.TeleBot(API_TOKEN)

# --- 🗄 ጊዜያዊ የዳታቤዝ መዝገብ ---
user_data = {}
active_tasks = []

# 1. Start Command & Reply Keyboard ማስተካከያ
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    
    # ዩዘር መመዝገቢያ
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0.0, 'completed_tasks': [], 'referred_by': None, 'referrals': 0}

    # የኪቦርድ በተኖችን እዚህ ጋር በትክክል እናዘጋጃለን
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    
    btn1 = types.KeyboardButton("💼 ስራዎችን ስራ (Earn)")
    btn2 = types.KeyboardButton("👥 ሰዎችን ጋብዝ (Referral)")
    btn3 = types.KeyboardButton("💰 የኔ ሂሳብ (Balance)")
    btn4 = types.KeyboardButton("💳 ገንዘብ ማውጫ (Withdraw)")
    
    # በተኖቹን በሁለት መስመር መደርደር
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    
    # አድሚን ከሆንክ የአድሚን ገጽ መጨመር
    if user_id == ADMIN_ID:
        btn_admin = types.KeyboardButton("🛠 የአድሚን ገጽ (Admin Panel)")
        markup.row(btn_admin)
        
    welcome_text = f"ሰላም {message.from_user.first_name}! ወደ Ethio JumpTask ቦት በሰላም መጣህ። ከታች ያሉትን በተኖች በመጫን ስራ መጀመር ትችላለህ።"
    
    # መልዕክቱን ከተቀናጁት በተኖች ጋር አብሮ መላክ
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 2. Main Menu - በተኖቹ ሲነኩ የሚሰሩት ስራዎች
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0.0, 'completed_tasks': [], 'referred_by': None, 'referrals': 0}

    if message.text == "💼 ስራዎችን ስራ (Earn)":
        if not active_tasks:
            bot.send_message(message.chat.id, "❌ ለአሁን አዲስ የተጫነ ማስታወቂያ ወይም ስራ የለም! ቆይተው ይሞክሩ።")
            return
        
        markup = types.InlineKeyboardMarkup()
        for task in active_tasks:
            if task['id'] not in user_data[user_id]['completed_tasks']:
                btn = types.InlineKeyboardButton(f"🎯 {task['name']} ({task['reward']} ETB)", callback_data=f"view_{task['id']}")
                markup.add(btn)
        bot.send_message(message.chat.id, "የሚከተሉትን ስራዎች በመስራት እውነተኛ ብር ያግኙ፡", reply_markup=markup)

    elif message.text == "👥 ሰዎችን ጋብዝ (Referral)":
        bot_info = bot.get_me()
        referral_link = f"https://t.me{bot_info.username}?start={user_id}"
        msg = f"👥 **የመጋበዣ ፕሮግራም**\n\nየእርስዎን ሊንክ ለጓደኞችዎ ያጋሩ! አንድ ሰው በሊንክዎ ሲገባ **0.50 ETB** ያገኛሉ።\n\n🔗 የእርስዎ ሊንክ፡\n{referral_link}"
        bot.send_message(message.chat.id, msg)

    elif message.text == "💰 የኔ ሂሳብ (Balance)":
        data = user_data[user_id]
        bot.send_message(message.chat.id, f"📊 **የአካውንትዎ መረጃ**\n\n💵 ያለዎት ብር: {data['balance']:.2f} ETB\n🎁 የጋበዙት ሰው ብዛት: {data['referrals']} ሰው")

    elif message.text == "💳 ገንዘብ ማውጫ (Withdraw)":
        data = user_data[user_id]
        if data['balance'] >= 25.0:
            bot.send_message(message.chat.id, "💰 ማውጣት የሚፈልጉትን የብር መጠን እና የቴሌብር ስልክ ቁጥርዎን ጽፈው ይላኩ።")
        else:
            bot.send_message(message.chat.id, "❌ **ይቅርታ!** ገንዘብ ለማውጣት ቢያንስ **25.00 ETB** ሊኖርዎት ይገባል።")

    elif message.text == "🛠 የአድሚን ገጽ (Admin Panel)" and user_id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        btn_add = types.InlineKeyboardButton("➕ አዲስ ስራ ጨምር", callback_data="admin_add_task")
        markup.add(btn_add)
        bot.send_message(message.chat.id, "እንኳን ወደ አድሚን ማዘዣ ጣቢያ መጡ።", reply_markup=markup)

# --- ቦቱን ማስነሻ ---
print("🚀 አዲሱ ቦት በተሳካ ሁኔታ ስራ ጀምሯል...")
bot.infinity_polling()
