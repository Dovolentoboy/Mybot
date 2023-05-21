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



"""

Для непонимающих. В этом ивенте бот читает сообщения и исходя из них делает определенные дейсвтия. Узнать вы можете об этом в документации или же через вопросы к нейросети
Хочу также отметить,что вы можете использовать формулу для уровня какую хотите. Например мой товарищ предложил сделать систему опыта через длину сообщений
Также можете сделать свою систему лвлов. Здесь предложен мой вараинт(взял я его у Fsoky)
Если что-то будет не работать обращайтесь в Dovolen toboy#6686

Удачного кодинга , поменьше ошибок и багов. Верю в вас)

P.S Ниже код для длины сообщений

@commands.Cog.listener()
    async def on_message(self,message):
        xp_count = len(message.content) * 0.3
        xp = cursor.execute("SELECT xp FROM users WHERE member_id = ?",(message.author.id,)).fetchone()[0]
        lvl = cursor.execute("SELECT lvl FROM users WHERE member_id = ?",(message.author.id,)).fetchone()[0]
        if message.author == self.bot:
            return
        if message.interaction is not None:
            return
        else:
             cursor.execute(f"UPDATE users SET xp = xp + {xp_count} WHERE member_id = ?",(message.author.id,))
             db.commit()
             

Остальное можете оставить неизменным, т.е тупо взять всё с кода выше)
"""



def setup(bot):
    bot.add_cog(Xp_system(bot))
