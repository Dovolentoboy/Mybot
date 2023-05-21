import sqlite3
import db as my_db
import disnake
import asyncio
from disnake.ext import commands

db = sqlite3.connect('bot.db')
cursor = db.cursor()


class Economy_get(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        print('Способы получения готовы')
    

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot:
            return
        if message.interaction is not None:
            return
        else:
            cursor.execute("UPDATE users SET balance = balance + 2 WHERE member_id = ?",(message.author.id,))
            db.commit()
            


def setup(bot):
    bot.add_cog(Economy_get(bot))