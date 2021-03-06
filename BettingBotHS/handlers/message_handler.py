from shared_utils import *
import pytz
from config import *
import asyncio
import re
import sys
import os
import random
os.environ['TZ'] = 'America/Chicago'
from datetime import datetime
from bet_db import BettingBotDBHandler
from bot_logger import BotLogger

from .bet_handler import BetHandler

ALLOWED_CHANNELS_BETS = ['picks']

CMD_HELP = "!help"
CMD_SHOW_PICKS = "!showpicks"
CMD_PICK = "!pick "
CMD_BALANCE = "!balance"
CMD_LEADER = "!leaderboard"
CMD_EVENT_INFO = "!eventinfo "
CMD_CHECK_EVENT = "!checkevent "
CMD_RESOLVE_EVENT = "!resolveevent "
CMD_REFILL = "!refill "

#USAGE = """`
USAGE = """
FantasyBot:
Commands:
!help
""".strip()
#`
#""".strip()



class MessageHandler:
    def __init__(self, config, client):
        self.client = client
        self.logger = BotLogger()
        self.bet_handler = BetHandler()
        self.bet_db_handler = BettingBotDBHandler(self.logger)
        self.deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')
        self.start_time = datetime.now()
    
    def log_message(self, message):
        timestamp = datetime.now().isoformat()
        sys.stdout.write("[%s] [%s] [%s] [%s] %s\n" % (
            timestamp, message.server, message.channel, message.author, message.content)
        )
        self.logger.info_log("command_log: [%s] [%s] [%s] [%s] %s\n" % (timestamp, message.server, message.channel, message.author, message.content))
        sys.stdout.flush()

    def check_user(self, user):
        if user.lower() in ALLOWED_USERS:
            return True
        else:
            return False

    def check_super_user(self, user):
        if user.lower() in ALLOWED_SUPER_USERS:
            return True
        else:
            return False

    def check_power_user(self, user):
        if user.lower() in POWER_USERS:
            return True
        else:
            return False

    async def handle(self, message):
        if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
            if not message.channel.is_private:
                return True
        if message.author.id == self.client.user.id:
            return
        if await self.handle_cmd(message):
            return

    async def handle_cmd(self, message, my_message=None):

        if message.content.startswith(CMD_SHOW_PICKS):
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_show_picks(message, CMD_SHOW_PICKS, my_message)
            return True

        if message.content.startswith(CMD_PICK):
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_pick(message, CMD_PICK, my_message)
            return True

        if message.content.startswith(CMD_BALANCE):
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_balance(message, CMD_BALANCE, my_message)
            return True

        if message.content.startswith(CMD_LEADER):
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_leader(message, CMD_LEADER, my_message)
            return True

        if message.content.startswith(CMD_EVENT_INFO):
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_event_info(message, CMD_EVENT_INFO, my_message)
            return True

        if message.content.startswith(CMD_CHECK_EVENT):
            print("SUPER_USER", self.check_super_user(str(message.author)))
            if not self.check_super_user(str(message.author)) and message.channel.is_private:
                return True
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_check_event(message, CMD_CHECK_EVENT, my_message)
            return True

        if message.content.startswith(CMD_RESOLVE_EVENT):
            print("SUPER_USER", self.check_super_user(str(message.author)))
            if not self.check_super_user(str(message.author)) and message.channel.is_private:
                return True
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_resolve_event(message, CMD_RESOLVE_EVENT, my_message)
            return True

        if message.content.startswith(CMD_REFILL):
            print("SUPER_USER", self.check_super_user(str(message.author)))
            if not self.check_super_user(str(message.author)) and message.channel.is_private:
                return True
            if str(message.channel.name) not in ALLOWED_CHANNELS_BETS:
                if not message.channel.is_private:
                    return True
            await self.handle_refill(message, CMD_REFILL, my_message)
            return True

        if message.content.startswith(CMD_HELP):
            await self.respond(message, USAGE)
            return True

    async def respond(self, message, response, my_message=None, wrapper = '```\n'):
        self.log_message(message)
        if len(response) > 2000:
            print(response)
            sys.stdout.write('response is very long: ' + str(len(response)) + '\n')
            sys.stdout.flush()
            response = 'Unfortunately response is too long'
        if my_message is None:
            if isinstance(response, list):
                for tmp_response in response:
                    my_message = await self.client.send_message(message.channel, wrapper + tmp_response + wrapper.replace('\n', ''))
            else:
                my_message = await self.client.send_message(message.channel, wrapper + response + wrapper.replace('\n', ''))
        else:
            await self.client.edit_message(my_message, '```\n' + response + '```')
        await self.check_edit(message, my_message)

    async def respond_image(self, message, response, my_message=None):
        self.log_message(message)
        my_message = await self.client.send_file(message.channel, response)

    async def handle_show_picks(self, message, cmd, my_message):
        response = self.bet_handler.handle_show_picks(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_pick(self, message, cmd, my_message):
        response = self.bet_handler.handle_pick(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_balance(self, message, cmd, my_message):
        response = self.bet_handler.handle_balance(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_leader(self, message, cmd, my_message):
        response = self.bet_handler.handle_leader(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_event_info(self, message, cmd, my_message):
        response = self.bet_handler.handle_event_balance(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_check_event(self, message, cmd, my_message):
        response = self.bet_handler.handle_check_event(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_resolve_event(self, message, cmd, my_message):
        response = self.bet_handler.handle_resolve_event(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def handle_refill(self, message, cmd, my_message):
        response = self.bet_handler.handle_refill(message.content[len(cmd):], message, self.bet_db_handler)
        await self.respond(message, response, my_message)

    async def check_edit(self, message, sent):
        original_content = message.content
        for _ in range(0, 30):
            if message.content != original_content:
                await self.handle_cmd(message, sent)
                return
            await asyncio.sleep(1)
