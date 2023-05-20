import sqlite3
import disnake
import os
from disnake.ext import commands
import db as my_db

con = sqlite3.connect('bot.db')
cursor = con.cursor()

bot = commands.Bot(command_prefix='.',intents=disnake.Intents.all())

db = my_db.Database()

@bot.event
async def on_ready():
    print(f"{bot.user.name} вошел в сеть")
    await db.guild_write()
    for guild in bot.guilds:
        for member in guild.members:
            await db.insert_new_member(member,table='users')
            await db.insert_new_member(member,table='warn')

@bot.event
async def on_member_join(member):
    await member.send(f'Добро пожаловать на сервер! Прочтите правила.')
    await db.insert_new_member(member)

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")

bot.run('MTEwNzIwOTY5NDY0MjE5NjUyMA.G6e4Fc.n7M0MLCaOq_n8VSXZfTiduDTHj5FNMby1u2APM')
    
