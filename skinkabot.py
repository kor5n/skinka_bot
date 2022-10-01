#starer bot

import os

import discord



intents = discord.Intents()
intents.members = True

class CustomClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        
intents = discord.Intents.default()
intents.members = True

client = CustomClient(intents=intents)
client.run("TOKEN")#your discord bot's token has to be here


