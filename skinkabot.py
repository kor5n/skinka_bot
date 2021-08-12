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
client.run("ODAyNTAzOTMyMjQ1MDQ5MzU0.YAwMBw.JAWeolGKBzQHXM9Upne21UlwhF0")


