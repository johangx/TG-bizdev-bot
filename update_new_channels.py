import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'service_account.json', scopes=SCOPES
)

gc = gspread.authorize(credentials)
spreadsheet_id = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'
sheet = gc.open_by_key(spreadsheet_id).sheet1

# New channel data from CSV (rows 24-63)
updates = [
    {'row': 24, 'admin': '@HamsterKombat_Official', 'community': 'N/A'},
    {'row': 25, 'admin': '@Blum, @BlumCryptoTradingBot, @BlumCrypto_Chat, @BlumSupport', 'community': 'N/A'},
    {'row': 26, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 27, 'admin': '@taping_Guru, @tapswap_bot', 'community': 'N/A'},
    {'row': 28, 'admin': '@xempire', 'community': 'N/A'},
    {'row': 29, 'admin': '@memefi_coin_bot', 'community': 'N/A'},
    {'row': 30, 'admin': '@alexisright, @seed_coin_bot', 'community': 'N/A'},
    {'row': 31, 'admin': '@catsgang_bot', 'community': 'N/A'},
    {'row': 32, 'admin': '@notcoin_bot', 'community': 'N/A'},
    {'row': 33, 'admin': 'N/A', 'community': 'https://t.me/TelegramTipsKo\nhttps://t.me/TelegramTipsBR\nhttps://t.me/TelegramTipsFA\nhttps://t.me/TelegramTipsIT\nhttps://t.me/TelegramTipsFR\nhttps://t.me/TelegramTipsTR\nhttps://t.me/TelegramTipsMS\nhttps://t.me/TelegramTipsDE\nhttps://t.me/TelegramTipsPL\nhttps://t.me/TelegramTipsAR\nhttps://t.me/TelegramTipsID\nhttps://t.me/TelegramTipsES'},
    {'row': 34, 'admin': 'N/A', 'community': 'https://t.me/TelegramTips'},
    {'row': 35, 'admin': '@JohnStonesA, @tomarket_ai_bot', 'community': 'N/A'},
    {'row': 36, 'admin': '@dogs_rescue_chat', 'community': 'N/A'},
    {'row': 37, 'admin': '@borz', 'community': 'N/A'},
    {'row': 38, 'admin': '@Davronbek', 'community': 'https://t.me/durov_russia\nhttps://t.me/durovschat'},
    {'row': 39, 'admin': '@mr_wcoin, @wcoin_tapbot', 'community': 'N/A'},
    {'row': 40, 'admin': '@CTotheMoon, @ctothemoon, @hello_yescoin, @justin_yescoin, @theYescoin_bot', 'community': 'N/A'},
    {'row': 41, 'admin': '@TimeFarmCryptoBot, @chronotech, @timefarmcommunitychat, @timefarmsupportbot', 'community': 'N/A'},
    {'row': 42, 'admin': '@Bridgetplayer1, @Jeribond22, @Lockmanh, @Marshle47, @kennethkhx, @tontimton', 'community': 'https://t.me/toncoin_en\nhttps://t.me/toncoin_uz\nhttps://t.me/toncoin_it\nhttps://t.me/toncoin_tur\nhttps://t.me/toncoin_es\nhttps://t.me/toncoin_cn\nhttps://t.me/claytoncoinbot\nhttps://t.me/toncoin_id\nhttps://t.me/emojistoncoin\nhttps://t.me/toncoin_chat\nhttps://t.me/toncoin_rus\nhttps://t.me/Toncoin_mining_rus'},
    {'row': 43, 'admin': '@Ads_ProxyMTProto, @ads_proxymtproto', 'community': 'N/A'},
    {'row': 44, 'admin': '@Bums_Support1, @bums, @bums_corner', 'community': 'N/A'},
    {'row': 45, 'admin': '@DegensCryptoBot', 'community': 'N/A'},
    {'row': 46, 'admin': '@GoatJune1, @Wilma_chief, @goatjune1, @realgoats_bot, @realgoats_channel', 'community': 'N/A'},
    {'row': 47, 'admin': '@ActivtyLauncher_bot, @activity_cooperation', 'community': 'N/A'},
    {'row': 48, 'admin': 'N/A', 'community': 'https://t.me/chat_clayton_ru\nhttps://t.me/tonclayton\nhttps://t.me/claytoncoinbot'},
    {'row': 49, 'admin': '@drops_on_hot, @firedrops_board, @hot_wallet, @hotonnear_chat, @hotprotocol_bot', 'community': 'N/A'},
    {'row': 50, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 51, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 52, 'admin': '@dotcoin_bot, @dotcoin_help_support', 'community': 'N/A'},
    {'row': 53, 'admin': '@bits, @bits_global_chat', 'community': 'N/A'},
    {'row': 54, 'admin': '@Bridge_StakeBot, @DuckChain_Bridge_bot, @DuckChain_Support_Bot', 'community': 'N/A'},
    {'row': 55, 'admin': '@CatizenAI, @catizenbot', 'community': 'N/A'},
    {'row': 56, 'admin': '@tapps_bot', 'community': 'N/A'},
    {'row': 57, 'admin': '@catsdogs_game_bot', 'community': 'N/A'},
    {'row': 58, 'admin': '@FintopioNews, @fintopio', 'community': 'N/A'},
    {'row': 59, 'admin': '@bill_bdbz, @buzzit1_bot, @sandy_support', 'community': 'N/A'},
    {'row': 60, 'admin': '@rocky_rabbit_bot', 'community': 'N/A'},
    {'row': 61, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 62, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 63, 'admin': 'N/A', 'community': 'N/A'}
]

print("Updating Google Sheet with new channel data...")

for update in updates:
    try:
        # Update admin column (B)
        sheet.update_cell(update['row'], 2, update['admin'])
        print(f"✅ Row {update['row']} - Admin: {update['admin']}")
        
        # Update community column (C)
        sheet.update_cell(update['row'], 3, update['community'])
        print(f"✅ Row {update['row']} - Community: {update['community']}")
        
    except Exception as e:
        print(f"❌ Error updating row {update['row']}: {e}")

print("\n🎯 **Google Sheet Update Complete!**")
print(f"✅ Updated {len(updates)} rows (24-63) with new channel data") 