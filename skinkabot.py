# skinkabot.py
import os
import random
import discord
from dotenv import load_dotenv
from guessing_game import game

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
        self.play = False
        self.number = 50.0

    def smart_win(self):
        smart_move_row = -1
        smart_move_col = -1

        for row in range(3):
            if self.c[row][0] == "0" and self.c[row][1] == '0' and self.c[row][2] == '.' :
                smart_move_row = row + 1
                smart_move_col = 3
            
        return (smart_move_row, smart_move_col)
    
    def smart_defence_diagonal(self):
        count_dia = 0
        dia_gde_tochka = -1
        
        for dia in range(3):
            if self.c[dia][dia] == 'x':
                count_dia += 1
            if self.c[dia][dia] == ".":
                dia_gde_tochka = dia
        
        if count_dia == 2 and dia_gde_tochka != -1:
            return(dia_gde_tochka, dia_gde_tochka)
        
        dia_gde_tochka1 = -1
        count_dia = 0
        dia_gde_tochka = -1
        dia1 = 2
        for dia in range(3):
            if self.c[dia][dia1] == 'x':
                count_dia += 1
            if self.c[dia][dia1] == ".":
                dia_gde_tochka = dia
                dia_gde_tochka1 = dia1
            dia1 -= 1

        if count_dia == 2 and dia_gde_tochka != -1:
            return(dia_gde_tochka, dia_gde_tochka1)
        else:
            return(-1, -1) 

    def smart_defence(self):
        
        smart_move_row = 0
        smart_move_col = 0
        #      0
        #      |

        # 0 -> x . 0    c[0][1]
        # 1 -> x x x
        # x . .
        count0 = 0
        count1 = 0
        count2 = 0
        col = 0
        cords_real1 = -1
        cords_real2 = -1
        cords01 = 0
        cords02 = 0
        cords11 = 0
        cords22 = 0
        cords31 = 0
        cords32 = 0
        strok = 0

        for row in range(9):
            #1 - poschitatj v peremennuju count kollichetvo x v stroke 
            
            # . . x
            # x . x
            # x . x
            if self.c[strok][col] == '.':
                if strok == 0:
                    count0 += 1 
                    cords01 = 0
                    cords02 = col
                elif strok == 1:
                    count1 += 1
                    cords11 = 1
                    cords12 = col
                elif strok == 2:
                    count2 += 1
                    cords21 = 2
                    cords22 = col
            if strok == 2:
                col += 1
                strok -= 3
            strok += 1
            if col == 3 and count0 == 2 or count0 == 0 or count0 == 3:
                cords01 = 0
                cords02 = 0
            if col == 3 and count1 == 2 or count1 == 0 or count1 == 3:
                cords11 = 0
                cords12 = 0
            if col == 3 and count2 == 2 or count2 == 0 or count2 == 3:
                cords21 = 0
                cords22 = 0
            
            if col == 3 and count0 == 1:
                cords_real1 = cords01  
                cords_real2 = cords02 
            if col == 3 and count1 == 1:
                cords_real1 = cords21  
                cords_real2 = cords22   
            if col == 3 and count2 == 1:
                cords_real1 = cords21  
                cords_real2 = cords22   
        return (cords_real1, cords_real2)

    async def bot_move(self, message):
        if self.game_over == True:
            self.player_bot = False
            return
        
        smart_move = self.smart_win()

        if smart_move[0] == -1 and smart_move[1] == -1:
            smart_move = self.smart_defence()
            if smart_move[0] == -1 and smart_move[1] == -1:
                smart_move = self.smart_defence_diagonal()
                if smart_move[0] == -1 and smart_move[1] == -1:    
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


        if message.content.startswith("/x0-move"):
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
        full_count = 0
        full_strok = 0
        full_col = 0
        for full in range(9):
            if self.c[full_strok][full_col] != ".":
                full_count += 1
            if full_col == 2:
                full_col -= 3
                full_strok += 1    
            full_col += 1
            if full_count == 9:
                self.game_over = True  
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
        if message.content.startswith("/x0-start"):
            self.game_over = False
            self.player_bot = True
            channel = message.channel
            result = message.content.split()
            await channel.send("Starting new game players: Korveee and " + result[1])
            await message.channel.send("Ходит " + self.x0_turn + ".")
            await self.xprint(message)
        if message.content.startswith("/x0-start pvp"):
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

        number,play = await game(message,self.play,self.number)

        if message.content.startswith("/help"):
            channel = message.channel
            await channel.send(
                message.author + "Привет меня зовут Korvee! :grinning: \n Я бот созданый @Kor5n! \n Мои команды: \n - /x0-start @твой никнейм \n \n P. S. с ботом могут играть только двое \n \n - /x0-start pvp @твой никнейм @никнейм врага \n \n P. S. в пвп могут играть только двое \n \n - /x0-move ''кордината по х от 1-3'' ''кордината по х от 1-3'' \n \n Пример: \n      1   2   3 \n 1  ['.', '.', '.'] \n 2 ['.', '.', '.'] \n 3 ['.', '.', '.']"
            )
        if message.content.startswith("/привет"):
            channel = message.channel
            await channel.send(
                "Привет я Korvee давай дружить?"
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
