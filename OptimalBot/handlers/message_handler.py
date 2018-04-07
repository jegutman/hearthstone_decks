import asyncio
import re
import sys
from datetime import datetime

from .sim_handler import SimHandler
from .deck_handler import DeckHandler
from .card_handler import CardHandler
from .issue_handler import IssueHandler


__version__ = "1.0.1"


CMD_CARD = "!card "
CMD_DECK = "!deck "
CMD_DATA = "!data"
CMD_TARGET = "!target "
CMD_SIM = "!sim "
CMD_SIM_LHS = "!simlhs "
CMD_HELP = "!help"
CMD_TAG = "!tag "
CMD_ENUM = "!enum "
CMD_CHANNEL = "!channel"

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
        self.issue_handler = IssueHandler(config["repos"])
        self.card_handler = CardHandler()
        self.deck_handler = DeckHandler()
        self.sim_handler = SimHandler()
        self.invite_url = config.get("invite_url", "")

    async def handle(self, message):
        ALLOWED_CHANNELS_BASIC = ["decklists"]
        if str(message.channel.name) not in ALLOWED_CHANNELS_BASIC:
            if not message.channel.is_private:
                return True
        if message.author.id == self.client.user.id:
            return
        if await self.handle_cmd(message):
            return

        matches = re.findall(r"(?<!<)(\w+)?#(\d+)($|\s|[^\w])", message.content)
        for match in matches:
            prefix = match[0]
            issue = match[1]
            response = self.issue_handler.handle(message.channel.name, prefix, issue)
            if response is not None:
                await self.client.send_message(message.channel, response)

    async def handle_cmd(self, message, my_message=None):
        ALLOWED_CHANNELS = ["decklists"]

        if message.content.startswith(CMD_CARD):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_card(message, CMD_CARD, my_message)
            return True

        if message.content.startswith(CMD_DECK):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck(message, CMD_DECK, my_message)
            return True

        if message.content.startswith(CMD_DATA):
            await self.data_check(message, CMD_DATA, my_message)
            return True

        if message.content.startswith(CMD_SIM):
            if not message.channel.is_private:
                return True
            await self.handle_sim(message, CMD_SIM, my_message)
            return True

        if message.content.startswith(CMD_TARGET):
            if not message.channel.is_private:
                return True
            await self.handle_sim(message, CMD_TARGET, my_message)
            return True

        if message.content.startswith(CMD_SIM_LHS):
            if not message.channel.is_private:
                return True
            await self.handle_sim(message, CMD_SIM_LHS, my_message, is_conquest=False)
            return True

        #if message.content.startswith(CMD_HELP):
        #    if message.channel.is_private:
        #        await self.respond(message, USAGE)
        #    else:
        #        await self.respond(message, "PM me !help for available commands. <3")
        #    return True
        
        if message.content.startswith(CMD_CHANNEL):
            await self.respond(message, str(message.channel.name))
        
        return False

    async def respond(self, message, response, my_message=None):
        log_message(message)
        if my_message is None:
            my_message = await self.client.send_message(message.channel, response)
        else:
            await self.client.edit_message(my_message, response)
        await self.check_edit(message, my_message)

    async def handle_sim(self, message, cmd, my_message, is_conquest=True):
        #if cmd == CMD_TARGET:
        #    response = self.sim_handler.handle_target(
        #        message.content[len(cmd):], is_conquest
        #    )
        #    await self.respond(message, response, my_message)
        #
        #    async def handle_sim(self, message, cmd, my_message):
        #        response = self.sim_handler.handle_target(message.content[len(cmd):], is_conquest)
        #        await self.respond(message, response, my_message)
        #else:
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
        response = self.deck_handler.handle(
            message.content[len(cmd):]
        )
        await self.respond(message, response, my_message)

        async def handle_deck(self, message, cmd, my_message):
            response = self.deck_handler.handle(message.content[len(cmd):], self.max_resposne(message))
            await self.respond(message, response, my_message)

    async def handle_card(self, message, cmd, my_message, collectible=None):
        response = self.card_handler.handle(
            message.content[len(cmd):], self.max_response(message), collectible
        )
        await self.respond(message, response, my_message)

        async def handle_card(self, message, cmd, my_message):
            response = self.card_handler.handle(message.content[len(cmd):], self.max_resposne(message))
            await self.respond(message, response, my_message)

    async def check_edit(self, message, sent):
        original_content = message.content
        for _ in range(0, 30):
            if message.content != original_content:
                await self.handle_cmd(message, sent)
                return
            await asyncio.sleep(1)

    def max_response(self, message):
        return self.max_cards_private if message.channel.is_private else self.max_cards_public
