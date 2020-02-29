import discord
import logging
from discord.ext import commands

class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def setup(client):
    client.add_cog(Logging(client))
