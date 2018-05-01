from shared_utils import *
from config import *
import asyncio
import re
import sys
from datetime import datetime
from deck_db import DeckDBHandler
from bot_logger import BotLogger

from .sim_handler import SimHandler
from .deck_handler import DeckHandler



CMD_DECK = "!deck "
CMD_SEARCH = "!search "
CMD_COMPARE = "!compare "
CMD_COMPARE_ALL = "!compareall "
CMD_SIMILAR = "!similar "
CMD_UPDATE = "!update "
CMD_DATA = "!data"
CMD_SIM = "!sim "
CMD_SIM_LHS = "!simlhs "
CMD_HELP = "!help"
CMD_COUNTDOWN = "!countdown"
CMD_UPTIME = "!uptime"
#CMD_CHANNEL = "!channel"
#CMD_OWNER = "!owner"

USAGE = """`
OptimalBot:
Commands:
!deck
!compare
!similar
!update
!data
!search

!help
`
""".strip()

def log_message(message):
    timestamp = datetime.now().isoformat()
    sys.stdout.write("[%s] [%s] [%s] [%s] %s\n" % (
        timestamp, message.server, message.channel, message.author, message.content)
    )
    sys.stdout.flush()


class MessageHandler:
    def __init__(self, config, client):
        self.client = client
        self.deck_handler = DeckHandler()
        self.sim_handler = SimHandler()
        self.logger = BotLogger()
        self.deck_db_handler = DeckDBHandler(self.logger)
        self.deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')
        self.start_time = datetime.now()

    async def handle(self, message):
        if str(message.channel.name) not in ALLOWED_CHANNELS:
            if not message.channel.is_private:
                return True
        if message.author.id == self.client.user.id:
            return
        if await self.handle_cmd(message):
            return

    async def handle_cmd(self, message, my_message=None):
        if message.content.startswith(CMD_UPDATE):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck_update(message, CMD_UPDATE, my_message)
            return True
        
        if message.content.startswith(CMD_SEARCH):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck_search(message, CMD_SEARCH, my_message)
            return True

        if message.content.startswith(CMD_COMPARE):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_compare(message, CMD_COMPARE, my_message)
            return True

        if message.content.startswith(CMD_COMPARE_ALL):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_compare_all(message, CMD_COMPARE_ALL, my_message)
            return True

        if message.content.startswith(CMD_SIMILAR):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_similar(message, CMD_SIMILAR, my_message)
            return True

        if message.content.startswith(CMD_DECK):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck(message, CMD_DECK, my_message)
            return True
        else:
            deckstring_matches = self.deckstring_re.findall(message.content)
            deck_name = None
            tmp_split = message.content.split('\n')
            for line in tmp_split:
                if line[:3] == '###':
                    deck_name = " ".join(line.split()[1:])
                    break
            for deck_code in deckstring_matches:
                self.logger.info_log('\n    %s\n    %s\n    MATCH: %s' % (message.author, message.content, deck_code))
                if deck_name:
                    self.logger.info_log('\nFound deck name: %s' % deck_name)
                self.deck_db_handler.process_deck(message, deck_code, name=deck_name)

        if message.content.startswith(CMD_DATA):
            await self.data_check(message, CMD_DATA, my_message)
            return True

        if message.content.startswith(CMD_HELP):
            await self.respond(message, USAGE)
            return True

        if message.content.startswith(CMD_COUNTDOWN):
            season_end = "05-01-2018 02:00:00"
            season_end_asia = "05-31-2018 11:00:00"
            season_end_eu = "05-31-2018 18:00:00"
            tmp = message.content.split(' ')
            if len(tmp) == 1:
                end_time = datetime.strptime(season_end, "%m-%d-%Y %H:%M:%S")
            elif tmp[1].lower() == 'na':
                end_time = datetime.strptime(season_end, "%m-%d-%Y %H:%M:%S")
            elif tmp[1].lower() == 'eu':
                end_time = datetime.strptime(season_end_eu, "%m-%d-%Y %H:%M:%S")
            elif tmp[1].lower() == 'asia':
                end_time = datetime.strptime(season_end_asia, "%m-%d-%Y %H:%M:%S")

            await self.respond(message, '`' + str(end_time - datetime.now()).split('.')[0] + ' left in season`')

            return True

        if message.content.startswith(CMD_UPTIME):
            await self.respond(message, str(datetime.now() - self.start_time).split('.')[0])
            return True

        if message.content.startswith(CMD_SIM):
            if not message.channel.is_private:
                return True
            await self.handle_sim(message, CMD_SIM, my_message)
            return True

        if message.content.startswith(CMD_SIM_LHS):
            if not message.channel.is_private:
                return True
            await self.handle_sim(message, CMD_SIM_LHS, my_message, is_conquest=False)
            return True
            

        #if message.content.startswith(CMD_CHANNEL):
        #    await self.respond(message, str(message.channel.name))

        #if message.content.startswith(CMD_OWNER):
        #    await self.respond_image(message, basedir + 'drlight.jpeg')
        
        return False

    def wrap_response(response):
        return '`' + response + '`'

    async def respond(self, message, response, my_message=None):
        log_message(message)
        if len(response) > 2000:
            sys.stdout.write('response is very long: ' + str(len(response)) + '\n')
            sys.stdout.flush()
        if my_message is None:
            my_message = await self.client.send_message(message.channel, response)
        else:
            await self.client.edit_message(my_message, response)
        await self.check_edit(message, my_message)

    async def respond_image(self, message, response, my_message=None):
        log_message(message)
        my_message = await self.client.send_file(message.channel, response)

    async def handle_sim(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def data_check(self, message, cmd, my_message):
        response = self.sim_handler.data_check()
        await self.respond(message, response, my_message)

    async def handle_deck(self, message, cmd, my_message, collectible=None):
        response = self.deck_handler.handle(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_deck_update(self, message, cmd, my_message):
        response = self.deck_handler.handle_update(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_deck_search(self, message, cmd, my_message):
        response = self.deck_handler.handle_search(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_compare(self, message, cmd, my_message):
        response = self.deck_handler.handle_compare(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_compare_all(self, message, cmd, my_message):
        response = self.deck_handler.handle_compare_all(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_similar(self, message, cmd, my_message):
        response = self.deck_handler.handle_similar(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def check_edit(self, message, sent):
        original_content = message.content
        for _ in range(0, 30):
            if message.content != original_content:
                await self.handle_cmd(message, sent)
                return
            await asyncio.sleep(1)
