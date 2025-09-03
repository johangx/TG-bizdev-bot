#!/usr/bin/env python3
"""
Enhanced Community Chat Discovery Tool

This specialized script finds associated community chats, discussion groups, and support channels
for given Telegram broadcast channels. It's designed to work when direct admin access isn't available.

Key Capabilities:
1. **Direct Link Detection**: Finds community links directly mentioned in channel descriptions
2. **Community Indicators**: Identifies text patterns that suggest community presence
3. **Message Scanning**: Analyzes recent messages for group links and community mentions
4. **Link Validation**: Ensures found links are relevant and properly formatted
5. **Smart Filtering**: Focuses on community chats that are actually related to the main channel

What It Finds:
- Discussion groups linked to broadcast channels
- Support and help channels
- Community forums and chat groups
- Bot support channels
- Official community spaces

Perfect for business development teams who need to:
- Find decision-makers when direct admin access is limited
- Discover community engagement opportunities
- Map out the full ecosystem around a channel
- Identify multiple contact points for outreach

Author: Johan
License: MIT
"""

import asyncio
import re
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel, Message
from dotenv import load_dotenv
