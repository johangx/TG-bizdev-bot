# Telegram Channel Admin Outreach Bot 🤖

A powerful Telegram bot for automating outreach to channel administrators and finding business development opportunities.

## Features ✨

- **Channel Scanning**: Automatically scan Telegram channels for admin information
- **Contact Extraction**: Extract phone numbers, emails, and usernames from channel descriptions and messages
- **Admin Detection**: Find channel administrators and moderators
- **Message Broadcasting**: Send automated messages to multiple users
- **Google Sheets Integration**: Update and manage contact data in Google Sheets
- **Business Development**: Perfect for sales outreach and partnership building

## Quick Start 🚀

### Prerequisites

- Python 3.7+
- Telegram API credentials
- Google Sheets API (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/johangx/telegram-admin-outreach-bot.git
   cd telegram-admin-outreach-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Telegram credentials**
   - Get your API credentials from [@BotFather](https://t.me/botfather)
   - Create a `.env` file with your credentials:
   ```env
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_BOT_TOKEN=your_bot_token
   ```

4. **Run the bot**
   ```bash
   python telegram_admin_dm_bot.py
   ```

## Main Scripts 📁

### Core Bot
- **`telegram_admin_dm_bot.py`** - Main bot for admin outreach
- **`enhanced_telegram_bot.py`** - Enhanced version with additional features

### Channel Scanning
- **`scan_yoo_stars.py`** - Scan specific channels for admin info
- **`scan_tech_tab.py`** - Scan tech channels for business opportunities
- **`scan_new_channels_bot.py`** - Automated channel discovery

### Message Broadcasting
- **`send_gm_message.py`** - Send "Good Morning" messages
- **`send_group_message.py`** - Send messages to group members

### Google Sheets Integration
- **`sheets_update_service_account.py`** - Update Google Sheets with service account
- **`sheets_update_simple.py`** - Simple Google Sheets update

## Usage Examples 💡

### Scan a Channel for Admins
```python
python scan_yoo_stars.py
```

### Send Messages to Users
```python
python send_gm_message_to_users.py
```

### Update Google Sheets
```python
python sheets_update_service_account.py
```

## Configuration ⚙️

### Environment Variables
- `TELEGRAM_API_ID` - Your Telegram API ID
- `TELEGRAM_API_HASH` - Your Telegram API Hash
- `TELEGRAM_BOT_TOKEN` - Your bot token
- `GOOGLE_SHEETS_CREDENTIALS` - Path to Google service account JSON

### Channel Lists
- `channels.txt` - List of channels to scan
- `new_channels_results.csv` - Results from channel scanning

## Features in Detail 🔍

### 1. Channel Scanning
- Automatically detect channel administrators
- Extract contact information from descriptions
- Scan recent messages for additional contacts
- Find linked groups and invite links

### 2. Contact Extraction
- Phone numbers (international format)
- Email addresses
- Telegram usernames
- t.me links and invite links

### 3. Admin Outreach
- Automated message sending
- Personalized outreach campaigns
- Follow-up message scheduling
- Response tracking

### 4. Data Management
- CSV export of results
- Google Sheets integration
- Contact database management
- Outreach campaign tracking

## Business Use Cases 💼

- **Sales Outreach**: Find decision makers in target industries
- **Partnership Building**: Connect with channel owners for collaborations
- **Market Research**: Understand channel demographics and engagement
- **Lead Generation**: Build contact lists for marketing campaigns
- **Network Building**: Expand professional network in specific niches

## Safety & Ethics ⚠️

- **Respect Rate Limits**: Don't spam or overwhelm users
- **Follow Telegram Terms**: Comply with platform guidelines
- **Privacy First**: Don't collect unnecessary personal information
- **Opt-out Respect**: Honor unsubscribe requests immediately
- **Professional Conduct**: Maintain professional communication standards

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ for the Telegram community**
