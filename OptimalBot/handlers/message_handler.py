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
from deck_db import DeckDBHandler
from bot_logger import BotLogger

from .sim_handler import SimHandler
from .deck_handler import DeckHandler



CMD_DECK = "!deck "
CMD_SEARCH = "!search "
CMD_SEARCH_PLAYOFF = "!searchplayoff "
CMD_LINEUP = "!lineup "
CMD_COMPARE = "!compare "
CMD_COMPARE_ALL = "!compareall "
CMD_SIMILAR = "!similar "
CMD_UPDATE = "!update "
CMD_DATA = "!data"
CMD_RANDOM = "!random "
CMD_SIM = "!sim "
CMD_BANS = "!bans "
CMD_BANS_LHS = "!banslhs "
CMD_SIM_LHS = "!simlhs "
CMD_LEAD_LHS = "!leadlhs "
CMD_NASH_LHS = "!nashlhs "
CMD_NASH_CQ_BANS = "!nashcqbans "
CMD_NASH_LHS_BANS = "!nashlhsbans "
CMD_HELP = "!help"
CMD_COUNTDOWN = "!countdown"
CMD_UPTIME = "!uptime"
CMD_OWNER = "!owner"
CMD_MECHATHUN = "!mechathun"
CMD_NEXTCARD = "!nextcard"

#USAGE = """`
USAGE = """
OptimalBot:
Commands:
!deck
!compare
!similar
!update
!data
!search

!help
""".strip()
#`
#""".strip()



class MessageHandler:
    def __init__(self, config, client):
        self.client = client
        self.deck_handler = DeckHandler()
        self.sim_handler = SimHandler()
        self.logger = BotLogger()
        self.deck_db_handler = DeckDBHandler(self.logger)
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

    def check_power_user(self, user):
        if user.lower() in POWER_USERS:
            return True
        else:
            return False

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

        if message.content.startswith(CMD_SEARCH_PLAYOFF):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck_search(message, CMD_SEARCH_PLAYOFF, my_message)
            return True

        if message.content.startswith(CMD_NEXTCARD):
            if str(message.channel.name) not in ['new-cards']:
                if not message.channel.is_private:
                    return True
                
            reveal_times = [ 
                # Times in PDT 
                "2018_11_20 02:00:00", 
                "2018_11_20 04:00:00", 
                "2018_11_20 05:00:00", 
                "2018_11_20 07:00:00", 
                "2018_11_20 08:00:00", 
                "2018_11_20 09:00:00", 
                "2018_11_20 11:00:00", 
                "2018_11_20 20:00:00", 
                "2018_11_21 02:00:00", 
                "2018_11_21 04:00:00", 
                "2018_11_21 07:00:00", 
                "2018_11_21 11:00:00", 
                "2018_11_21 13:00:00", 
                "2018_11_21 18:00:00", 
                "2018_11_21 23:00:00", 
                "2018_11_22 01:00:00", 
                "2018_11_22 04:00:00", 
                "2018_11_22 07:00:00", 
                "2018_11_22 10:00:00", 
                "2018_11_22 23:00:00", 
                "2018_11_23 04:00:00", 
                "2018_11_23 06:00:00", 
                "2018_11_23 07:00:00", 
                "2018_11_23 11:00:00", 
                "2018_11_23 14:00:00", 
                "2018_11_23 22:00:00", 
                "2018_11_23 23:00:00", 
                "2018_11_24 01:00:00", 
                "2018_11_24 07:00:00", 
                "2018_11_24 11:00:00", 
                "2018_11_24 13:00:00", 
                "2018_11_24 23:00:00", 
                "2018_11_25 04:00:00", 
                "2018_11_25 07:00:00", 
                "2018_11_25 11:00:00", 
                "2018_11_25 19:00:00", 
                "2018_11_26 02:00:00", 
                "2018_11_26 04:00:00", 
                "2018_11_26 07:00:00", 
                "2018_11_26 08:00:00", 
                "2018_11_26 11:00:00", 
                "2018_11_26 21:00:00", 
                "2018_11_26 23:00:00", 
                "2018_11_27 01:00:00", 
                "2018_11_27 04:00:00", 
                "2018_11_27 07:00:00", 
                "2018_11_27 11:00:00", 
                "2018_11_27 18:00:00", 
                "2018_11_27 23:00:00", 
            ]
            na_tz = pytz.timezone('America/Los_Angeles')
            local_tz = pytz.timezone('America/Chicago')
            current_time = datetime.now(tz=local_tz)
            card_times = []
            for timestamp in reveal_times:
                card_time = na_tz.localize(datetime.strptime(timestamp, "%Y_%m_%d %H:%M:%S"))
                if card_time > current_time:
                    break
            res = "Next Card Reveal in " + str(card_time - current_time).split('.')[0] + ' at ' + '%s PDT' % (card_time.strftime("%H:%M:%S"))
            await self.respond(message, res)
            return True


        if message.content.startswith(CMD_LINEUP):
            if str(message.channel.name) not in ALLOWED_CHANNELS:
                if not message.channel.is_private:
                    return True
            await self.handle_deck_search(message, CMD_LINEUP, my_message)
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

        if message.content.startswith(CMD_RANDOM):
            await self.get_random(message, CMD_RANDOM, my_message)
            return True

        if message.content.startswith(CMD_HELP):
            await self.respond(message, USAGE)
            return True

        if message.content.startswith(CMD_COUNTDOWN):
            #season_end = "08-01-2018 02:00:00"
            #season_end_asia = "07-31-2018 11:00:00"
            #season_end_eu = "07-31-2018 17:00:00"
            #tmp = message.content.split(' ')
            
            na_tz = pytz.timezone('America/Los_Angeles')
            eu_tz = pytz.timezone('CET')
            asia_tz = pytz.timezone('Hongkong')
            season_end = "12-01-2018 00:00:00"
            na_end = na_tz.localize(datetime.strptime(season_end, "%m-%d-%Y %H:%M:%S"))
            eu_end = eu_tz.localize(datetime.strptime(season_end, "%m-%d-%Y %H:%M:%S"))
            asia_end = asia_tz.localize(datetime.strptime(season_end, "%m-%d-%Y %H:%M:%S"))
            local_tz = pytz.timezone('America/Chicago')
            #current_time = local_tz.localize(datetime.now())
            current_time = datetime.now(tz=local_tz)
            t1 = str(na_end - current_time).split('.')[0] + ' left in season'
            t2 = str(eu_end - current_time).split('.')[0] + ' left in season'
            t3 = str(asia_end - current_time).split('.')[0] + ' left in season'
            res = ''
            res += 'NA:   ' + t1 + '\n'
            res += 'EU:   ' + t2 + '\n'
            res += 'APAC: ' + t3 + '\n'
            await self.respond(message, res)
            return True

            #await self.respond(message, '`' + str(end_time - datetime.now()).split('.')[0] + ' left in season`')

        if message.content.startswith(CMD_UPTIME):
            await self.respond(message, str(datetime.now() - self.start_time).split('.')[0])
            return True

        if message.content.startswith(CMD_BANS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of DMs to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_bans(message, CMD_BANS, my_message)
            return True

        if message.content.startswith(CMD_BANS_LHS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of DMs to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_bans(message, CMD_BANS_LHS, my_message, is_conquest=False)
            return True

        if message.content.startswith(CMD_LEAD_LHS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of DMs to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_lead(message, CMD_LEAD_LHS, my_message, is_conquest=False)
            return True

        if message.content.startswith(CMD_NASH_LHS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_power_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of this command to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_nash_lead(message, CMD_NASH_LHS, my_message, is_conquest=False)
            return True

        if message.content.startswith(CMD_NASH_CQ_BANS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_power_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of this command to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_nash_cq_bans(message, CMD_NASH_CQ_BANS, my_message, is_conquest=False)
            return True

        if message.content.startswith(CMD_NASH_LHS_BANS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_power_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of this command to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_nash_lhs_bans(message, CMD_NASH_LHS_BANS, my_message, is_conquest=False)
            return True

        if message.content.startswith(CMD_SIM):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of DMs to optimal bot" % str(message.author).split('#')[0])
                        return True
                
            await self.handle_sim(message, CMD_SIM, my_message)
            return True

        if message.content.startswith(CMD_SIM_LHS):
            if str(message.channel.name).lower() not in ['sims']:
                if not message.channel.is_private:
                    return True
                else:
                    if not self.check_user(str(message.author)):
                        await self.respond(message, "Sorry %s, you are not an authorized user of DMs to optimal bot" % str(message.author).split('#')[0])
                        return True
            await self.handle_sim(message, CMD_SIM_LHS, my_message, is_conquest=False)
            return True
            
        if message.content.startswith(CMD_OWNER):
            await self.respond_image(message, basedir + 'drlight.jpeg')

        if message.content.startswith(CMD_MECHATHUN):
            await self.respond_image(message, basedir + 'OptimalBot/Assets/mechathun.png')
        
        return False

    async def respond(self, message, response, my_message=None):
        self.log_message(message)
        if len(response) > 2000:
            sys.stdout.write('response is very long: ' + str(len(response)) + '\n')
            sys.stdout.flush()
            response = 'Unfortunately response is too long'
        if my_message is None:
            if isinstance(response, list):
                for tmp_response in response:
                    my_message = await self.client.send_message(message.channel, '```\n' + tmp_response + '```')
            else:
                my_message = await self.client.send_message(message.channel, '```\n' + response + '```')
        else:
            await self.client.edit_message(my_message, '```\n' + response + '```')
        await self.check_edit(message, my_message)

    async def respond_image(self, message, response, my_message=None):
        self.log_message(message)
        my_message = await self.client.send_file(message.channel, response)

    async def handle_sim(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def handle_bans(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle_bans(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def handle_lead(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle_lead(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def handle_nash_lead(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle_nash_lead(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def handle_nash_lhs_bans(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle_nash_lhs_bans(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def handle_nash_cq_bans(self, message, cmd, my_message, is_conquest=True):
        response = self.sim_handler.handle_nash_cq_bans(
            message.content[len(cmd):], is_conquest
        )
        await self.respond(message, response, my_message)

    async def data_check(self, message, cmd, my_message):
        response = self.sim_handler.data_check()
        await self.respond(message, response, my_message)

    async def get_random(self, message, cmd, my_message):
        response = self.sim_handler.get_random(message.content[len(cmd):])
        await self.respond(message, response, my_message)

    async def handle_deck(self, message, cmd, my_message, collectible=None):
        response = self.deck_handler.handle(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_deck_update(self, message, cmd, my_message):
        response = self.deck_handler.handle_update(message.content[len(cmd):], message, self.deck_db_handler)
        await self.respond(message, response, my_message)

    async def handle_deck_search(self, message, cmd, my_message):
        use_playoffs = False
        if cmd == CMD_LINEUP:
            response = self.deck_handler.handle_lineup(message.content[len(cmd):], message, self.deck_db_handler)
            await self.respond(message, response, my_message)
        else:
            if cmd == CMD_SEARCH_PLAYOFF:
                use_playoffs = True
            response = self.deck_handler.handle_search(message.content[len(cmd):], message, self.deck_db_handler, use_playoffs=use_playoffs)
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
