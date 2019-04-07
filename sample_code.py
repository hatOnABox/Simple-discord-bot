import discord
import os
import random
import time
import sqlite3
import threading


client = discord.Client()
down = False
runningSleep = False


def backgroundSleep():
    global down
    global runningSleep

    time.sleep(10)
    down = False
    runningSleep = False

@client.event # event desorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    global down
    global runningSleep


    if down == True and message.author.server_permissions.administrator == False:
        if runningSleep == False:
            t = threading.Thread(target=backgroundSleep)
            t.start()
            runningSleep = True
        pass
    else:

        if message.content.lower() == "!source":
            await client.send_file(message.channel, f"{os.getcwd()}/sample_code.txt")
            if message.author.server_permissions.administrator == False:
                down = True

        if message.content.lower() == "!quote":
            conn = sqlite3.connect('quotes.db')
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS quote (text, author)''')
            conn.commit()
            quotes = list(c.execute('''SELECT * FROM quote'''))
            thingy = random.choice(quotes)

            await client.send_message(message.channel, f"{thingy[0] + ' ' + thingy[1]}")


            conn.close()
            if message.author.server_permissions.administrator == False:
                down = True


        if len(message.content) > 150 and message.author.bot == False:
            await client.delete_message(message)
            await client.send_message(message.channel, str(message.author) + " that message was way too long!")


        if message.content.lower() == "!commands":
            await client.send_message(message.channel, """!quote - Prints a funny quote\n!commands - pulls this list up again\n!source - prints a txt file with this bot's source code\n!add quote (quote) (author) - adds quote (NOTE: only works if admins use it)\n!off - turns bot off (NOTE: only works if admins use it)\n!clear - clears full char (only admins can use)\n!slowclap - makes the bot slow clap five times\n!love (put someones name here) - Spread the love to people""")

            if message.author.server_permissions.administrator == False:
                down = True

        if message.content.lower()[0:10] == "!add quote" and message.author.server_permissions.administrator == True:

            if len(message.content.split("\"")) != 5:
                await client.send_message(message.channel, "Error: Incorrect quote syntax")
            else:
                quote = message.content.split("\"")[1]
                author = message.content.split("\"")[3]

            conn = sqlite3.connect('quotes.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS quote (text, author)''')
            conn.commit()
            c.execute(f'INSERT INTO quote (text, author) VALUES (?, ?)', (quote, author))
            conn.commit()
            conn.close()

            await client.send_message(message.channel, "Add quote: " + quote + ' ' + author)


        if message.content.lower() == "!slowclap":
            for i in range(0, 5):
                await client.send_message(message.channel, "*Clap*")
                time.sleep(2)


            if message.author.server_permissions.administrator == False:
                down = True


        if message.content.isupper() == True and message.author.server_permissions.administrator == False:
            await client.delete_message(message)
            await client.send_message(message.channel, str(message.author) + " Thou shall not spam caps!!!")


        if message.content.lower() == "!off" and message.author.server_permissions.administrator == True:
            await client.send_message(message.channel, "Bot is shuting down...")
            await client.close()


        if message.content.lower() == "!clear" and message.author.server_permissions.administrator == True:
            msgs = []
            async for x in client.logs_from(message.channel):
                msgs.append(x)
            await client.delete_messages(msgs)


        if str(message.content.lower())[0:5] == "!love":
            if len(message.content.split(" ")) > 2:
                await client.send_message(message.channel, "Love syntax incorrect!")
            else:
                await client.send_message(message.channel, "Spread some love to " + message.content.split(" ")[1] + "!")


client.run("ENTER YOUR TOKEN HERE")
