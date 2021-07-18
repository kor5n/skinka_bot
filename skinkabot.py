# skinkabot.py
import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents()
intents.members = True


class CustomClient(discord.Client):
    def __init__(self, intents, c=[[".", ".", "."], [".", ".", "."], [".", ".", "."]]):
        super(CustomClient, self).__init__(intents=intents)
        self.c = c
        self.game_over = False
        self.x0_turn = "x"
        self.player_bot = False

    def smart_win(self):
        smart_move_row = 0
        smart_move_col = 0

        for row in range(3):
            if self.c[row][0] == "0" and self.c[row][1] == '0' and self.c[row][2] == '.' :
                smart_move_row = row + 1
                smart_move_col = 3
            
        return (smart_move_row, smart_move_col)

    def smart_defence(self):
        smart_move_row = 0
        smart_move_col = 0
        for row in range(3):
            if self.c[row][0] == "x" and self.c[row][1] == 'x' and self.c[row][2] == '.' :
                smart_move_row = row + 1
                smart_move_col = 3
        
        return (smart_move_row, smart_move_col)

    async def bot_move(self, message):
        if self.game_over == True:
            self.player_bot = False
            return
        
        smart_move = self.smart_win()

        if smart_move[0] == 0 and smart_move[1] == 0:
            smart_move = self.smart_defence()
            if smart_move[0] == 0 and smart_move[1] == 0:   
                bot_stroka = random.randint(0, 2)
                bot_kolonka = random.randint(0, 2)
            else:
                bot_stroka = smart_move[0] -1 
                bot_kolonka = smart_move[1] -1
        else:
            bot_stroka = smart_move[0] -1
            bot_kolonka = smart_move[1] -1
                
        if self.c[bot_stroka][bot_kolonka] == ".":
            self.c[bot_stroka][bot_kolonka] = "0"
            await self.x0in_row(message, "0")
            await self.x0change_turn(message)
        elif self.c[bot_stroka][bot_kolonka] == "x" or "0":
            await self.bot_move(message)
        await self.xprint(message)

    async def x0change_turn(self, message):
        if self.x0_turn == "x":
            self.x0_turn = "0"
        else:
            self.x0_turn = "x"
        if self.player_bot == True:
            if self.x0_turn == "0":
                await self.bot_move(message)

    async def x0game(self, message):

        if self.game_over == True:
            return

        if message.content.startswith("!x0-move"):
            channel = message.channel
            result = message.content.split()
            stroka = int(result[1]) - 1
            kolonka = int(result[2]) - 1
            x_or_0 = self.x0_turn
            if self.c[stroka][kolonka] == ".":
                self.c[stroka][kolonka] = x_or_0
                await self.x0in_row(message, x_or_0)
                await self.x0change_turn(message)
                if not self.game_over:
                    await message.channel.send("Ходит " + self.x0_turn + ".")
            else:
                await channel.send("Жулик! Не жульничай!")
            await self.xprint(message)

    async def x0in_row(self, message, x_or_0):
        for row in range(3):
            if (
                self.c[row][0] == x_or_0
                and self.c[row][1] == x_or_0
                and self.c[row][2] == x_or_0
            ):
                self.game_over = True
        for collon in range(3):
            if (
                self.c[0][collon] == x_or_0
                and self.c[1][collon] == x_or_0
                and self.c[2][collon] == x_or_0
            ):
                self.game_over = True
        if self.c[0][0] == x_or_0 and self.c[1][1] == x_or_0 and self.c[2][2] == x_or_0:
            self.game_over = True
        if self.c[0][2] == x_or_0 and self.c[1][1] == x_or_0 and self.c[2][0] == x_or_0:
            self.game_over = True
        if self.game_over == True:
            channel = message.channel
            await channel.send(
                "Игрок игравший за " + x_or_0 + " выиграл! Игра окончена."
            )

    async def xprint(self, message):
        channel = message.channel
        await channel.send(self.c[0])
        await channel.send(self.c[1])
        await channel.send(self.c[2])

    async def x0start(self, message):
        if message.content.startswith("!x0-start"):
            self.game_over = False
            self.player_bot = True
            channel = message.channel
            result = message.content.split()
            await channel.send("Starting new game players: Korv and " + result[1])
            await message.channel.send("Ходит " + self.x0_turn + ".")
            await self.xprint(message)
        if message.content.startswith("!x0-start pvp"):
            self.game_over = False
            channel = message.channel
            result = message.content.split()
            await channel.send(
                "starting new game players: " + result[1] + " and " + result[2]
            )
            await message.channel.send("Ходит " + self.x0_turn + ".")
            await self.xprint(message)

    async def on_message(self, message):
        if self.user == message.author:
            return

        await self.x0start(message)
        await self.x0game(message)

        if message.content.startswith("!python"):
            channel = message.channel
            await channel.send(
                "Python is the most popular programming language in the world."
            )

    async def on_member_join(self, member):
        await member.send(f"Hello, {member.name}!")
        await member.send("Welcome to our programming server!")

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
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
