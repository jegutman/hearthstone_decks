from shared_utils import *
import asyncio
import re
import sys
from datetime import datetime
from deck_db import DeckDBHandler
from bot_logger import BotLogger

from .sim_handler import SimHandler
from .deck_handler import DeckHandler



CMD_DECK = "!deck "
CMD_UPDATE = "!update "
CMD_DATA = "!data"
CMD_SIM = "!sim "
CMD_SIM_LHS = "!simlhs "
CMD_HELP = "!help"
#CMD_CHANNEL = "!channel"
#CMD_OWNER = "!owner"

USAGE = """
OptimalBot v0.1

Pro tip: Typo'd your search? Edit it and I will edit my response. :)
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

    async def handle(self, message):
        ALLOWED_CHANNELS_BASIC = ["decklists", "spooky"]
        if str(message.channel.name) not in ALLOWED_CHANNELS_BASIC:
            if not message.channel.is_private:
                return True
        if message.author.id == self.client.user.id:
            return
        if await self.handle_cmd(message):
            return

    async def handle_cmd(self, message, my_message=None):
        ALLOWED_CHANNELS = ["decklists", "spooky"]
    
        if message.content.startswith(CMD_UPDATE):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck_update(message, CMD_UPDATE, my_message)
            return True

        if message.content.startswith(CMD_DECK):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck(message, CMD_DECK, my_message)
            return True
        else:
            deckstring_matches = self.deckstring_re.findall(message.content)
            for deck_code in deckstring_matches:
                self.logger.info_log('\n    %s\n    %s\n    MATCH: %s' % (message.author, message.content, deck_code))
                self.deck_db_handler.process_deck(message, deck_code)

        if message.content.startswith(CMD_DATA):
            await self.data_check(message, CMD_DATA, my_message)
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

    async def respond(self, message, response, my_message=None):
        log_message(message)
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

        async def handle_sim(self, message, cmd, my_message):
            response = self.sim_handler.handle(message.content[len(cmd):], is_conquest)
            await self.respond(message, response, my_message)

    async def data_check(self, message, cmd, my_message):
        response = self.sim_handler.data_check()
        await self.respond(message, response, my_message)

        async def data_check(self, message, cmd, my_message):
            response = self.sim_handler.data_check()
            await self.respond(message, response, my_message)

    async def handle_deck(self, message, cmd, my_message, collectible=None):
        response = self.deck_handler.handle(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

        async def handle_deck(self, message, cmd, my_message):
            response = self.deck_handler.handle(message.content[len(cmd):], message, self.deck_db_handler)
            await self.respond(message, response, my_message)

    async def handle_deck_update(self, message, cmd, my_message, collectible=None):
        response = self.deck_handler.handle_update(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

        async def handle_deck_update(self, message, cmd, my_message):
            response = self.deck_handler.handle_update(message.content[len(cmd):], message, self.deck_db_handler)
            await self.respond(message, response, my_message)

    async def check_edit(self, message, sent):
        original_content = message.content
        for _ in range(0, 30):
            if message.content != original_content:
                await self.handle_cmd(message, sent)
                return
            await asyncio.sleep(1)
