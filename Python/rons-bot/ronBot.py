#!/Users/jeremyfriese/Desktop/BitBucketShared/env/bin/python3
import os
import random
import discord
from discord.ext import commands
import cv2
"""from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger"""
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("DISCORD_TOKEN "))
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
#GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='')

client = discord.Client()

async def func():
    c = bot.get_channel(channel_id)
    await c.send("Timer Test")

@bot.command(name='dice', help='Simulates rolling dice.')
async def roll(ctx):
    filePath = "dice/"
    number_of_dice = 2
    number_of_sides = 6
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]

    item1 = str(random.choice(range(1, number_of_sides + 1)))
    item2 = str(random.choice(range(1, number_of_sides + 1)))
    if item1 == "1":
        file1 = filePath + "1.png"
    elif item1 == "2":
        file1 = filePath + "2.png"
    elif item1 == "3":
        file1 = filePath + "3.png"
    elif item1 == "4":
        file1 = filePath + "4.png"
    elif item1 == "5":
        file1 = filePath + "5.png"
    if item2 == "1":
        file2 = filePath + "1.png"
    elif item2 == "2":
        file2 = filePath + "2.png"
    elif item2 == "3":
        file2 = filePath + "3.png"
    elif item2 == "4":
        file2 = filePath + "4.png"
    elif item2 == "5":
        file2 = filePath + "5.png"
    elif item2 == "6":
        file2 = filePath + "6.png"
    #await ctx.send(', '.join(dice))
    img1 = cv2.imread(file1)
    img2 = cv2.imread(file2)
    image = cv2.hconcat([img1, img2])
    cv2.imwrite("tmp.png", image)
    await ctx.send(file=discord.File("tmp.png"))

@bot.command(name='flip', help='Simulates flipping a coin.')
async def flip(ctx):
    filepath = "ht"
    coin = os.listdir(filepath)
    pic = random.choice(coin)
    if "ds" in pic.lower():
        print("Done")
        pic = random.choice(coin)
    pic = filepath + "/" + pic
    await ctx.send(file=discord.File(pic))


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    #initializing scheduler
    """scheduler = AsyncIOScheduler()

    #sends "s!t" to the channel when time hits 10/20/30/40/50/60 seconds, like 12:04:20 PM
    scheduler.add_job(func, CronTrigger(second="0, 10, 20, 30, 40, 50"))

    #starting the scheduler
    scheduler.start()"""

@bot.event
async def on_member_join(member):
    #guild = discord.utils.get(client.guilds, name=GUILD)
    ron_quotes = [
        "You have an absolutely breathtaking hiney.",
        "I'm kind of a big deal....",
        "I'm kind of a big deal. People know me.",
    ]
    response = random.choice(ron_quotes)
    await message.channel.send(f"Hi {client.user}, " + response)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@bot.command(name='Sith', help='Responds with a random quote from Ron Burgundy')
async def AnchorMan(ctx):
    #guild = discord.utils.get(client.guilds, name=GUILD)
    guild = ctx.message.guild.name
    channel = bot.get_channel
    ron_quotes = [
        "You underestamate the power of the dark side.",
        "Be careful not to choke on your aspirations.",
        "I am altering the deal. ...",
        "You don't know the power of the dark side!",
        "He’s as clumsy as he is stupid.",
        f"{guild} knows the true power of the dark side",
        "I am altering the deal. Pray I don’t alter it any further.s",
        "When I left you, I was but the learner. Now I am the master.",
        f"I find your lack of faith in {guild} disturbing.",
        "This will be a day long remembered.",
        "When I left you, I was but the learner. Now I am the master.",
        "Don’t fail me again",
        "You are unwise to lower your defenses!",



    ]
    tmpList = []
    meme = os.listdir("memes")
    for m in meme:
        if "ds" in m.lower():
            pass
        else:
            tmpList.append(m)
    r = random.choice((tmpList, ron_quotes))
    response = random.choice(r)

    if "jpeg" in response or "gif" in response:
        await ctx.send(file=discord.File("memes/" + response))
    else:
        await ctx.send(response)




@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@bot.command(name='Vader', help='Responds with a random quote from Ron Burgundy')
async def AnchorMan(ctx):
    #guild = discord.utils.get(client.guilds, name=GUILD)
    guild = ctx.message.guild.name
    channel = bot.get_channel
    ron_quotes = [
        "You underestamate the power of the dark side.",
        "Be careful not to choke on your aspirations.",
        "I am altering the deal. ...",
        "You don't know the power of the dark side!",
        "He’s as clumsy as he is stupid.",
        f"{guild} knows the true power of the dark side",
        "I am altering the deal. Pray I don’t alter it any further.s",
        "When I left you, I was but the learner. Now I am the master.",
        f"I find your lack of faith in {guild} disturbing.",
        "This will be a day long remembered.",
        "When I left you, I was but the learner. Now I am the master.",
        "Don’t fail me again",
        "You are unwise to lower your defenses!",
        


    ]
    tmpList = []
    meme = os.listdir("memes")
    for m in meme:
        if "ds" in m.lower():
            pass
        else:
            tmpList.append(m)
    r = random.choice((tmpList, ron_quotes))
    response = random.choice(r)

    if "jpeg" in response or "gif" in response:
        await ctx.send(file=discord.File("memes/" + response))
    else:
        await ctx.send(response)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@bot.command(name='Ron', help='Responds with a random quote from Ron Burgundy')
async def AnchorMan(ctx):
    #guild = discord.utils.get(client.guilds, name=GUILD)
    guild = ctx.message.guild.name
    channel = bot.get_channel
    ron_quotes = [
        "You underestamate the power of the dark side.",
        "Be careful not to choke on your aspirations.",
        "I am altering the deal. ...",
        "You don't know the power of the dark side!",
        "He’s as clumsy as he is stupid.",
        f"{guild} knows the true power of the dark side",
        "I am altering the deal. Pray I don’t alter it any further.s",
        "When I left you, I was but the learner. Now I am the master.",
        f"I find your lack of faith in {guild} disturbing.",
        "This will be a day long remembered.",
        "When I left you, I was but the learner. Now I am the master.",
        "Don’t fail me again",
        "You are unwise to lower your defenses!",
        


    ]
    tmpList = []
    meme = os.listdir("memes")
    for m in meme:
        if "ds" in m.lower():
            pass
        else:
            tmpList.append(m)
    r = random.choice((tmpList, ron_quotes))
    response = random.choice(r)

    if "jpeg" in response or "gif" in response:
        await ctx.send(file=discord.File("memes/" + response))
    else:
        await ctx.send(response)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@bot.command(name='Darth', help='Responds with a random quote from Ron Burgundy')
async def AnchorMan(ctx):
    #guild = discord.utils.get(client.guilds, name=GUILD)
    guild = ctx.message.guild.name
    channel = bot.get_channel
    ron_quotes = [
        "You underestamate the power of the dark side.",
        "Be careful not to choke on your aspirations.",
        "I am altering the deal. ...",
        "You don't know the power of the dark side!",
        "He’s as clumsy as he is stupid.",
        f"{guild} knows the true power of the dark side",
        "I am altering the deal. Pray I don’t alter it any further.s",
        "When I left you, I was but the learner. Now I am the master.",
        f"I find your lack of faith in {guild} disturbing.",
        "This will be a day long remembered.",
        "When I left you, I was but the learner. Now I am the master.",
        "Don’t fail me again",
        "You are unwise to lower your defenses!",
        


    ]
    tmpList = []
    meme = os.listdir("memes")
    for m in meme:
        if "ds" in m.lower():
            pass
        else:
            tmpList.append(m)
    r = random.choice((tmpList, ron_quotes))
    response = random.choice(r)

    if "jpeg" in response or "gif" in response:
        await ctx.send(file=discord.File("memes/" + response))
    else:
        await ctx.send(response)


bot.run(TOKEN)
