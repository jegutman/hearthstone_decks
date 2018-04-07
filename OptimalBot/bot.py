#!/usr/bin/env python3

import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

import argparse
import json
import subprocess

import discord
from handlers.message_handler import MessageHandler


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to configuration file")
    args = p.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    client = discord.Client()
    message_handler = MessageHandler(config, client)

    @client.event
    async def on_ready():
        print("Logged in as", client.user.name)

    @client.event
    async def on_message(message):
        await message_handler.handle(message)

    client.run(config["token"])


if __name__ == "__main__":
    main()
