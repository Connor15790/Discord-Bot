import discord
import random
import requests
import wikipedia
import json
import aiohttp
import io
import os
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

RPS = ["rock", "paper", "scissors"]

Toss_a_Coin = ["head", "tail"]

def get_joke():
    response = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
    json_data = response.json()
    setup = json_data["setup"]
    delivery = json_data["delivery"]
    return setup, delivery

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content

    if msg.startswith("$joke"):
        setup, delivery = get_joke()
        await message.channel.send(setup)
        await message.channel.send(delivery)

    if msg.endswith("wikipedia"):
        wikipage = wikipedia.page(msg.replace("wikipedia", ""), auto_suggest = False)
        link = wikipage.images
        suffixes = (".png", ".jpg")
        links = []
        for i in link:
            if len(links)<3 and i.endswith(suffixes):
                links.append(i)
        async with aiohttp.ClientSession() as session: # creates session
            async with session.get(random.choice(links)) as resp: # gets image from url
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'cool_image.png'))
        results = wikipedia.summary(msg.replace("wikipedia", ""), sentences = 3, auto_suggest = False).encode("utf8")
        await message.channel.send(results)
        

    for i in range(len(RPS)):
        if msg == RPS[i]:
            await message.channel.send(random.choice(RPS))

    if msg == "toss":
        await message.channel.send(random.choice(Toss_a_Coin))

    await bot.process_commands(message)


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@bot.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel.")


@bot.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")

load_dotenv("C:/Users/Conno/OneDrive/Desktop/VS Code projects/Discord Bot/.env")
bot.run(os.getenv("TOKEN"))