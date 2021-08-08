import random
import discord 



async def game(message,number):
    num_str = "50"
    if message.content.startswith("/угадайка"):
        channel = message.channel
        
        await channel.send(
            "загадай число от 1 до 100 напиши **/загадал** если готов"
            )
    if message.content.startswith("/загадал"):
        channel = message.channel
            


        await channel.send(
            "твое число больше " + num_str + "ответь /больше, /меньше или /угадал"
            )



    if message.content.startswith("/больше"):
            channel = message.channel
            
            number = number = number + number / 2
            num_str = str(number)
            await channel.send(
                "твое число больше " + num_str + "ответь /больше, /меньше или /угадал"
                )


    if message.content.startswith("/меньше"):
            channel = message.channel
            
            number = number / 2    
            num_str = str(number)
            await channel.send(
                "твое число больше " + num_str + "ответь /больше, /меньше или /угадал"
                )


    if message.content.startswith("/угадал"):
        channel = message.channel
        
        
        number = 50.0

        await channel.send(
            "я умный! можешь поиграть заново **/угадайка**"
            )

    return(number)



            