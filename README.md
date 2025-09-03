# Telegram Business Development Bot 🤖

A powerful Python bot that automates Telegram outreach for business development by identifying channel administrators and associated community chats.

## ✨ Key Features

- **🔍 Admin Detection**: Automatically finds administrators and owners of Telegram channels
- **💬 Community Chat Discovery**: Identifies associated discussion groups and community chats linked to broadcast channels
- **📱 Direct Messaging**: Sends personalized messages to discovered contacts
- **📊 Google Sheets Integration**: Exports all data to organized spreadsheets
- **⚡ MTProto API**: Uses personal account authentication for maximum access
- **🌐 Multi-language Support**: Can read and process content in various languages including Russian

## 🚀 What This Bot Can Do

This bot is specifically designed to help business development teams by:

1. **Scanning Telegram Channels**: Input channel links and the bot will analyze them thoroughly
2. **Finding Admins**: Extract admin handles, owner information, and contact details from channel descriptions
3. **Discovering Community Chats**: When direct admin access isn't available, the bot finds associated community groups, discussion channels, and support chats
4. **Smart Contact Mapping**: Maps found contacts to the correct channels and organizes data properly
5. **Automated Outreach**: Send personalized messages to discovered contacts for business development

## 🎯 Perfect For

- **Business Development Teams**: Automate outreach to channel administrators
- **Marketing Agencies**: Find decision-makers in relevant Telegram communities
- **Startup Founders**: Connect with community leaders and influencers
- **Content Creators**: Identify potential collaboration opportunities
- **Crypto/Web3 Projects**: Find admins of relevant blockchain and crypto channels

## 📋 Requirements

- Python 3.7+
- Telegram account (not a bot account)
- Google Sheets API access
- Telegram API credentials (api_id and api_hash)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/johangx/TG-bizdev-bot.git
cd TG-bizdev-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your credentials:
```bash
cp env.example .env
# Edit .env with your Telegram and Google Sheets credentials
```

4. Run the quick start script:
```bash
python quick_start.py
```

## 🔧 Configuration

### Telegram API Setup
1. Go to https://my.telegram.org/
2. Log in with your phone number
3. Go to 'API development tools'
4. Create a new application
5. Copy your `api_id` and `api_hash`

### Google Sheets Setup
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a service account
4. Download the JSON key file
5. Share your spreadsheet with the service account email

## 📖 Usage Examples

### Basic Channel Scanning
```python
python telegram_admin_dm_bot.py
```

### Send Messages to Users
```python
python send_gm_message_to_users.py
```

### Update Google Sheets
```python
python sheets_update_final.py
```

### Find Community Chats
```python
python community_chat_finder.py
```

## 🔍 How It Works

1. **Channel Analysis**: The bot reads channel descriptions, pinned messages, and recent content
2. **Admin Detection**: Extracts admin handles, owner information, and contact details
3. **Community Discovery**: Finds linked community groups, support channels, and discussion forums
4. **Data Validation**: Ensures found links are relevant and properly formatted
5. **Sheet Updates**: Organizes all data into Google Sheets with proper formatting

## 📊 Output Format

The bot exports data to Google Sheets with:
- **Column A**: Telegram channel links
- **Column B**: Admin handles and contact information
- **Column C**: Associated community chat links (with line breaks for multiple links)

## 🚨 Important Notes

- **Rate Limiting**: Built-in delays to respect Telegram and Google Sheets API limits
- **Privacy Settings**: Some users may have restrictions preventing direct messages
- **Language Support**: Can process content in multiple languages including Russian
- **Session Management**: Creates session files for persistent authentication

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is for legitimate business development purposes only. Please respect Telegram's Terms of Service and user privacy. Use responsibly and ethically.

## 🆘 Support

If you encounter any issues:
1. Check the error messages in the terminal
2. Verify your API credentials are correct
3. Ensure your Google Sheets permissions are set up properly
4. Check that your Telegram account is not restricted

---

**Built with ❤️ for business development teams who want to automate their Telegram outreach efficiently and ethically.**
