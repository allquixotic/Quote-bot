import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import hashlib
import sqlite3
import os

#prefix
bot = commands.Bot(command_prefix='%')

#check if database is made and load it
db = sqlite3.connect('quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user TEXT, message TEXT, date_added TEXT)')
print("Loaded database")

db.commit()

@bot.event
async def on_ready():
    print ("Connected to discord")

#######commands##########

#test commmand
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("pong: quotebot.")
    print ("ping sent")

#help menu
@bot.command()
async def qhelp(ctx):
    embed = discord.Embed(name="qhelp")
    embed.set_author(name="Quotebot commands:")
    embed.add_field(name="To quote:", value="%qsave [user] [message]", inline=False)
    embed.add_field(name="To display", value="%qget [user]", inline=False)
    embed.add_field(name="Random quote from a random user", value="%qrand", inline=False)
    await ctx.send(embed=embed)

#print random quote
@bot.command()
async def qrand(ctx):

    cursor.execute("SELECT user,message,date_added FROM quotes ORDER BY RANDOM() LIMIT 1")
    query = cursor.fetchone()

    #log
    print(query[0]+": \""+query[1]+"\" printed to the screen "+str(query[2]))

    #embeds the output
    #processed = query[0].replace("<", "").replace(">", "").replace("!","").replace("@","")
    #print("raw " + processed)
    #dn = await bot.get_user(processed).name
    style = discord.Embed(name="responding quote", description="- " + query[0] + " "+str(query[2]))
    style.set_author(name=str(query[1]))
    await ctx.send(embed=style)


@bot.command()
async def qsave(ctx, username: str, *, message: str):
    
    if '@' in username:
        await ctx.send("Please don't use `@` to ping a person when using this bot. It wakes people up. Not nice!")
        return

    uniqueID = hash(username+message)

    #date and time of the message
    time = datetime.datetime.now()
    formatted_time = str(time.strftime("%d-%m-%Y %H:%M"))

    #find if message is in the db already
    cursor.execute("SELECT count(*) FROM quotes WHERE hash = ?",(uniqueID,))
    find = cursor.fetchone()[0]

    if find>0:
        return

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?,?,?)",(uniqueID,username,message,formatted_time))
    await ctx.send("Quote successfully added")

    db.commit()

    #number of words in the database
    rows = cursor.execute("SELECT * from quotes")

    #log to terminal
    print(str(len(rows.fetchall()))+". added - "+ username +": \"" + message + "\" to database at "+formatted_time)


@bot.command()
async def qget(ctx, user: str):

    try:
        #query random quote from user
        print("Looking for message from " + user)
        cursor.execute("SELECT message,date_added,user FROM quotes WHERE lower(trim(user)) = lower(trim(?)) ORDER BY RANDOM() LIMIT 1", (user,))
        query = cursor.fetchone()

        #adds quotes to message
        output = "\""+str(query[0])+"\""

        #log
        print(user+": \""+output+"\" printed to the screen "+str(query[1]))

        #embeds the output to make it pretty
        style = discord.Embed(name="responding quote", description="- "+ query[2] +" "+str(query[1]))
        style.set_author(name=output)
        await ctx.send(embed=style)

    except Exception as excrement:
        print(excrement)
        await ctx.send("No quotes of that user found")

    db.commit()    

sekrit = os.environ['DISCORD_SECRET']
if sekrit:
    bot.run(os.environ['DISCORD_SECRET'])
else:
    print("Need to specify environment variable DISCORD_SECRET")
