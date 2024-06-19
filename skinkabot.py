# skinkabot.py
import ollama
import json
import os
import random
import discord
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
intents.members = True


class CustomClient(discord.Client):
    def __init__(self, intents, c=[["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]):
        super(CustomClient, self).__init__(intents=intents)
        self.x0_players = []
        self.c = c
        self.game_over = False
        self.x0_turn = "x"
        self.player_bot = False
        self.villains = ["Porky","Doki-Doki","stinky Peet","Super bam","miss Mil","lolik","mr J","grecnij"]
        self.shops = ["магазин щитов","магазин зелий"]
        self.adventures = ["в пещеру","на далекие острова","в арктику"]
        self.cash = []
        self.xp = []
        self.weapons = []
        self.shields = []
        self.potions = []
    def if_reg(self,nickname1):
        find_nick = None
        with open ("save_ds_game.json", "r") as file:
            nicknames = json.load(file)
            if len(nicknames) == 0:
                self.save(str(nickname1),50,0,0,0,0)
                return False
            elif nicknames['nickname'] == str(nickname1) :
                return True

            else:
                self.save(str(nickname1),50,0,0,0,0)
                return False
    def save(self,nickname1,cash1,xp1,weapons1,shields1,potions1):
        
        about = {
        'nickname': nickname1,
        'cash':cash1,
        'xp':xp1,
        'weapons': weapons1,
        'potions': potions1,
        'shields': shields1
        }
        with open ("save_ds_game.json", "a") as file:
            x = json.dump(about, file)

    
    async def bot_move(self, message):
        if self.game_over == True:
            self.player_bot = False
            return
        
        bot_stroka = random.randint(0, 2)
        bot_kolonka = random.randint(0, 2)
       
                
        if self.c[bot_stroka][bot_kolonka] == "-":
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
            self.c = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
            return
    

        else:
            if message.content.startswith("-x0-move"):
                channel = message.channel
                result = message.content.split()
                stroka = int(result[1]) - 1
                kolonka = int(result[2]) - 1
                x_or_0 = self.x0_turn
                if self.c[stroka][kolonka] == "-":
                    print(message.author.id, self.x0_players[0][2:-1], self.x0_players[1][2:-1])
                    print(self.x0_turn)
                    print(str(message.author.id) == str(self.x0_players[0][2:-1]))
                    if self.x0_turn == "x" and str(message.author.id) == str(self.x0_players[0][2:-1]) or self.x0_turn == "0" and str(message.author.id) == str(self.x0_players[1][2:-1]):
                        self.c[stroka][kolonka] = x_or_0
                        await self.x0in_row(message, x_or_0)
                        await self.x0change_turn(message)
                    else:
                        await message.channel.send(embed=discord.Embed(description="Жулик! Не жульничай!", colour=discord.Colour.red()))
                else:
                    await message.channel.send(embed=discord.Embed(description="Жулик! Не жульничай!", colour=discord.Colour.red()))
                if self.game_over==False:
                    await self.xprint(message)

                

    async def x0in_row(self, message, x_or_0):
        full_count = 0
        full_strok = 0
        full_col = 0
        for full in range(9):
            if self.c[full_strok][full_col] != "-":
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
            await self.xprint(message)
            channel = message.channel
            self.x0_turn = "x"
            if len(self.x0_players) == 2:
                if x_or_0 == "x":
                    winner = self.x0_players[0]
                else:
                    winner = self.x0_players[1]
                await channel.send(
                    embed=discord.Embed(description="Игрок " + winner+ " игравший за " + x_or_0 + " выиграл! Игра окончена.", colour=discord.Colour.orange())
                )
                self.x0_players = []
            else:
                await channel.send(
                    embed=discord.Embed(description = "Игрок игравший за " + x_or_0 + " выиграл! Игра окончена.", colour=discord.Colour.orange())
                )

    async def xprint(self, message):
        channel = message.channel
        await message.channel.send(embed=discord.Embed(title= "Ходит " + str(self.x0_turn) + "-",description=str(self.c[0]) + "\n" +str(self.c[1]) + "\n" + str(self.c[2]), colour=discord.Colour.blue()))
    async def x0start(self, message):
        if message.content.startswith("-x0-start bot"):
            self.game_over = False
            self.player_bot = True
            channel = message.channel       
            result = message.content.split()
            self.x0_players = ["<@"+ message.author.id + ">", "<@802503932245049354>"]
            await channel.send(embed=discord.Embed(description ="Starting new game players: "+ self.x0_players[0] +" and " + self.x0_players[1], colour=discord.Color.green()))
            #await message.channel.send("Ходит " + self.x0_turn + "-")
            await self.xprint(message)
        if message.content.startswith("-x0-start pvp"):
            self.game_over = False
            channel = message.channel
            result = message.content.split()
            self.x0_players.append(result[2])
            self.x0_players.append(result[3])
            print(self.x0_players[0], self.x0_players[1])
            await message.channel.send(
                embed=discord.Embed(description="starting new game players: " + result[2] + " and " + result[3], colour=discord.Colour.green())
            )
            #await message.channel.send("Ходит " + self.x0_turn + "-")
            await self.xprint(message)




        
        


    async def ShopChoose(self, message, shop,findNickname):
        channel = message.channel
        if (shop == 0):
            await channel.send(
                embed = discord.Embed(title = "выбирайте предметы:"),
                    components=[
                        discord.Button(label= "ледяной щит 50$", style = discord.ButtonStyle.blue, emoji = "🧊"),
                        discord.Button(label= "огняный щит 100$", style = discord.ButtonStyle.red, emoji = "🔥"),
                        discord.Button(label= "денежный щит 200$", style = discord.ButtonStyle.green, emoji = "💸"),
                        discord.Button(label= "щит котов 350$", style = discord.ButtonStyle.blue, emoji = "🐱"),
                        discord.Button(label= "щит древней сосиски 500$", style = discord.ButtonStyle.red, emoji = "🌭")
                    ]
                )
        elif (shop == 1):
            await channel.send(
                embed = discord.Embed(title = "выбирайте предметы:"),
                    components=[
                        discord.Button(label= "+ жизни 20$", style = discord.ButtonStyle.green, emoji = "❤"),
                        discord.Button(label= "+ атака 50$", style = discord.ButtonStyle.red, emoji = "⚔"),
                        discord.Button(label= "+ денег с врагов 200$", style = discord.ButtonStyle.blue, emoji = "💸"),
                        discord.Button(label= "+ опыта с врагов 350$", style = discord.ButtonStyle.green, emoji = "🧬")
                    ]
                )

    async def Shop(self, message,findNickname):
        channel = message.channel
        await channel.send(
            embed = discord.Embed(title = "в какой магазин отправимся?"),
                components=[
                    discord.Button(label= self.shops[0], style = discord.ButtonStyle.red, emoji = "🛡"),
                    discord.Button(label= self.shops[1], style = discord.ButtonStyle.green, emoji = "🧃")
                ]
            )
        response = await bot.wait_for("button_click")
        if response.channel == channel:
            if (response.component.label == "магазин щитов"):
                await self.ShopChoose(message,0,findNickname)
                
            elif (response.component.label == "магазин зелий"):
                await self.ShopChoose(message,1,findNickname)

        
    async def on_message(self, message):
        if message.content.startswith("-ai"):
            await self.ai(message)
        if message.content.startswith("-x0-"):

            await self.x0start(message)
            await self.x0game(message)


        

        

#"Привет меня зовут Korvee! :grinning: \n Я бот созданый @Kor5n (помогал @Fordocront)! \n Мои команды: \n - /x0-start @твой никнейм \n \n P. S. с ботом могут играть только двое \n \n - /x0-start pvp @твой никнейм @никнейм врага \n \n P. S. в пвп могут играть только двое \n \n - /x0-move ''кордината по х от 1-3'' ''кордината по х от 1-3'' \n \n Пример: \n      1   2   3 \n 1  ['-', '.', '.'] \n 2 ['.', '.', '.'] \n 3 ['.', '.', '.']"
        if message.content.startswith("-привет"):
            channel = message.channel
            await channel.send(
                "Привет я Korvee давай дружить?"
            )

        if message.content.startswith("-reg"):
            channel = message.channel
            #self.Save(str(message.author),50,0,0,0,0)
            if (self.if_reg( message.author)):
                await channel.send('вы уже зареганы!!!!!!!\n аааааа я злой!!!!1111!! 👿')
            else: 
                await channel.send(embed = discord.Embed(title = "Вы зарегестрировались", description = "Вам выдан баланс в 50 монет! \nЗагляните в магазин (-ShopChoose) чтобы их потратить 💵"))
            


        if message.content.startswith("-команды"):
            channel = message.channel
            go = False
            findNickname = "f"

            for message.author in self.nickname:
                if message.author in self.nickname:
                    findNickname = message.author
                    go = True
                    
                else:
                    go = False
                
            if (go == True):
                print(findNickname)

                await channel.send(
                    
                    embed = discord.Embed(title = "вы начали игру!"),
                    components=[
                        discord.Button(label= "Дратся", style = discord.ButtonStyle.red, emoji = "⚔"),
                        discord.Button(label= "пойти в магазин", style = discord.ButtonStyle.green, emoji = "🛍"),
                        discord.Button(label= "отправится в приключения", style = discord.ButtonStyle.blue, emoji = "🏝")

                    ]
                )
                response = await bot.wait_for("button_click")
                if response.channel == channel:
                    if (response.component.label == "Дратся"):
                        await response.respond(content = "Вы будете дратся с " + random.choice(self.villains))
                    
                    elif (response.component.label == "пойти в магазин"):
                        channel = message.channel
                        await self.Shop(message,findNickname)
                            
                        

                    
                    elif (response.component.label == "отправится в приключения"):
                        await response.respond(content = "выберите куда отправится")

                

            else:
                await channel.send(
                    
                    embed = discord.Embed(title = "вы не зарегестрированы использйте \n-reg")
                    

                    
                )



    

    #async def on_member_join(self, member):

        #await member.send(f"Hello, {member.name}!")
        #await member.send("Welcome to our server!")
    async def ai(self, message):
        print(message.content)
        print(message.content.replace("-ai", ""))
        prompt = message.content.replace("-ai", "")
        response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
        ])
        await message.reply(embed = discord.Embed(title =prompt, description = response['message']['content'], colour=discord.Colour.purple()))
        
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        #for server in self.guilds:
         #   print(server.name)
          #  for channel in server.channels:
          #      print(channel.name)
           # for member in server.members:
            #    print(member.name)
    
intents = discord.Intents.default()
intents.members = True

bot = CustomClient(intents=intents)
bot.run(os.getenv("DISCORD_TOKEN"))
