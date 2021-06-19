#skinkabot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents()
intents.members = True

class CustomClient(discord.Client):
    def __init__(self, intents,  c = [['.', '.', '.'],['.', '.', '.'], ['.', '.', '.']]):
        super(CustomClient, self).__init__(intents=intents)
        self.c = c
        
    async def x0game(self,message):
        if message.content.startswith('!x0-move'):
            channel = message.channel
            result = message.content.split()
            stroka = int(result[2]) - 1 
            kolonka = int(result[3]) - 1
            x_or_0 = result[1]
            if self.c[stroka][kolonka] == '.':
                self.c[stroka][kolonka] = x_or_0 
            else:
                await channel.send("Жулик! Не жульничай!")
            await self.xprint(message)
        
    async def xprint (self,message):
        channel = message.channel 
        await channel.send(self.c[0])
        await channel.send(self.c[1])
        await channel.send(self.c[2])

    async def x0start (self,message):
        if message.content.startswith("!x0-start") :
            channel = message.channel
            result = message.content.split()
            await channel.send("starting new game players: " + result[1] + " and " +result[2])
            
            await self.xprint(message)

    async def on_message(self,message):
        if (self.user == message.author):
            return

        await self.x0start(message)
        await self.x0game (message)

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

bot = CustomClient(intents=intents)
bot.run(TOKEN)
