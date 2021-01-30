#skinkabot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents()
intents.members = True

class CustomClient(discord.Client):
    async def on_message(self,message):
        if (self.user == message.author):
            return

        if message.content.startswith('!python'):
            channel = message.channel
            await channel.send('Python is the most popular programming language in the world.')
    
    async def on_member_join(self,member):
        await member.send (f"Hello, {member.name}!")
        await member.send ("Welcome to our programming server!")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for server in self.guilds:
            print(server.name)
            for channel in server.channels:
                print(channel.name)
            for member in server.members:
                print(member.name)

intents = discord.Intents.default()
intents.members = True

client = CustomClient(intents=intents)
client.run(TOKEN)


