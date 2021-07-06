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
        self.game_over = False
        self.x0_turn = "x"
    def x0change_turn(self):
        if self.x0_turn == "x":
            self.x0_turn = "0"
        else:
            self.x0_turn = "x"
    async def x0game(self,message):
        if self.game_over == True:
            return
        await message.channel.send("Ходит " + self.x0_turn + ".") 
        if message.content.startswith('!x0-move'):
            channel = message.channel
            result = message.content.split()
            stroka = int(result[1]) - 1 
            kolonka = int(result[2]) - 1
            x_or_0 = self.x0_turn
            if self.c[stroka][kolonka] == '.':
                self.c[stroka][kolonka] = x_or_0
                await self.x0in_row(message, x_or_0)
                self.x0change_turn()
            else:
                await channel.send("Жулик! Не жульничай!")
            await self.xprint(message)
        

    async def x0in_row(self, message, x_or_0):
        for row in range(3): 
            if self.c[row][0] == x_or_0 and self.c[row][1] == x_or_0 and self.c[row][2] == x_or_0:
                self.game_over = True
        for collon in range(3):
            if self.c[0][collon] == x_or_0 and self.c[1][collon] == x_or_0 and self.c[2][collon] == x_or_0:
                self.game_over = True
        if self.c[0][0] == x_or_0 and self.c[1][1] == x_or_0 and self.c[2][2] == x_or_0:
            self.game_over = True
        if self.c[0][2] == x_or_0 and self.c[1][1] == x_or_0 and self.c[2][0] == x_or_0:
            self.game_over = True
        if self.game_over == True:
            channel = message.channel
            await channel.send("Игрок игравший за " + x_or_0 + " выиграл! Игра окончена.")
            
            
    async def xprint (self,message):
        channel = message.channel 
        await channel.send(self.c[0])
        await channel.send(self.c[1])
        await channel.send(self.c[2])

    async def x0start (self,message):
        if message.content.startswith("!x0-start") :
            self.game_over = False
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
