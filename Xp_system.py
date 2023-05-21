import sqlite3
import db as my_db
import disnake
import asyncio
from disnake.ext import commands

db = sqlite3.connect('bot.db')
cursor = db.cursor()

class Xp_system(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        xp = cursor.execute("SELECT xp FROM users WHERE member_id = ?",(message.author.id,)).fetchone()[0]
        lvl = cursor.execute("SELECT lvl FROM users WHERE member_id = ?",(message.author.id,)).fetchone()[0]
        if message.author == self.bot:
            return
        if message.interaction is not None:
            return
        else:
            cursor.execute("UPDATE users SET xp = xp + 100 WHERE member_id = ?",(message.author.id,))
            db.commit()
            if xp >= 10 + 10 * lvl:
                cursor.execute('UPDATE users SET lvl = lvl + 1, xp = 0 WHERE member_id = ?', (message.author.id,))
                db.commit()
                embed = disnake.Embed(
                    title='Повышение уровня',
                    description=f"Поздравляем {message.author.mention} с достижением уровня {lvl + 1}!"
                )
                await message.author.send(embed=embed)
                lvl_roles = {
                    5:1109736633475014736,
                    10:1109739990654664714,
                    15:1109740016793571338,
                }
                if lvl + 1 in lvl_roles:
                    role_id = lvl_roles[lvl + 1]
                    role = message.guild.get_role(role_id)
                    await message.author.add_roles(role)

def setup(bot):
    bot.add_cog(Xp_system(bot))
