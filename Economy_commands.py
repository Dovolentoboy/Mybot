import sqlite3
import db as my_db
import disnake
import asyncio
from disnake.ext import commands

db = sqlite3.connect('bot.db')
cursor = db.cursor()


class Economy(commands.Cog):
    
    def __init__(self,bot):
        print('Экономика готова')
        self.bot = bot
        
    
    @commands.slash_command(name='balance')
    async def balance(self,interaction,member:disnake.Member):
        

        balance = cursor.execute("SELECT balance FROM users WHERE member_id = ?",(member.id,)).fetchone()[0]
        embed = disnake.Embed(
            title=f'Баланс пользователя {member}',
            description=f'Деньги 💵\n```{balance}```'
        )
        await interaction.send(embed=embed)

       
    
    @commands.slash_command(name='pay')
    async def pay(self,interaction,member:disnake.Member,amount:int):
        
        balance = cursor.execute("SELECT balance FROM users WHERE member_id = ?",(member.id,)).fetchone()[0] #берем эту переменную из прошлой команды
        if int(balance) < int(amount):
            await interaction.send('Ваш баланс меньше. Незя так')
        else:
            member_transfer = cursor.execute(f'UPDATE users SET balance = balance + {amount} WHERE member_id = ?',(member.id,))
            author_transfer = cursor.execute(f'UPDATE users SET balance = balance - {amount} WHERE member_id = ?',(member.id,))
            await interaction.send(f'Пользователь {interaction.author.mention} перевел пользовател {member.mention} {amount} денег💵')
            await member.send(f'Вам подарок от {interaction.author} в виде {amount} денег💵')
    
    @commands.slash_command(name='setBalance')
    async def set_balance(self,interaction,member:disnake.Member,count:int):
        cursor.execute(f"UPDATE users SET balance = {count}")
        await interaction.send(f'Значение баланса пользователя {member} = {count}')
    

    @commands.slash_command(name='give',description='Причина по дефолту подарок')
    async def give(self,interaction,member:disnake.Member,amount:int,reason='Подарок'):
        member_transfer = cursor.execute(f'UPDATE users SET balance = balance + {amount} WHERE member_id = ?',(member.id,))
        await interaction.send(f'Пользователь {interaction.author.mention} выдал пользователю {member.mention} {amount} денег💵')
        await member.send(f'{interaction.author} прислал вам денег в количестве {amount} по причине {reason}')
    
    
def setup(bot):
    bot.add_cog(Economy(bot))
