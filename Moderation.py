import sqlite3
import db as my_db
import disnake
import asyncio
from disnake.ext import commands

db = sqlite3.connect('bot.db')
cursor = db.cursor()


async def check_time(interaction, mute_role, member: disnake.Member, time, reason):
    time_formats = {'h': 3600, 'ч': 3600, 'm': 60, 'м': 60, 's': 1, 'с': 1}
    time_unit = time[-1]
    if time_unit not in time_formats:
        await interaction.send('Указан неверный формат времени. h или ч - час, m или м - минут, s или с - секунд')
        return
    duration = int(time[:-1]) * time_formats[time_unit]
    await member.add_roles(mute_role)
    await interaction.send(embed=disnake.Embed(
        title='Выдача мута',
        description=f'{interaction.author} выдал мут {member.mention} на {time} по причине {reason}'
    ))
    await asyncio.sleep(duration)
    await member.remove_roles(mute_role)
    ls_embed = disnake.Embed(
        title='Снятие мута',
        description='С вас снят мут'
    )
    await member.send(embed=ls_embed)
            

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Модерация готова')
        self.db = my_db.Database()


    @commands.slash_command(name='mute')
    async def mute(self, interaction, time, member: disnake.Member, reason='Не указана'):
        if member == interaction.author:
            embed = disnake.Embed(
                title='Ошибка применения',
                description='Вы не можете выдать наказание самому себе'
                )
            await interaction.send(embed=embed)
        else:
            await interaction.response.defer()
            mute_role = disnake.utils.get(member.guild.roles, id=1109432156037595156)
            ls_embed = disnake.Embed(
                    title='Выдача мута',
                    description=f'Вы получаете мут на {time} по причине : {reason}'
            )
            await member.send(embed=ls_embed)
            await check_time(interaction=interaction,member=member,mute_role=mute_role,time=time,reason=reason)


    @commands.slash_command(name='unmute')
    async def unmute(self,interaction,member:disnake.Member):
        if member == interaction.author:
            embed = disnake.Embed(
                title='Ошибка применения',
                description='Вы не можете выдать размут самому себе'
                )
            await interaction.send(embed=embed)
        else:
            
            mute_role = disnake.utils.get(member.guild.roles, id=1109432156037595156) #вставлять своё ID
            await member.remove_roles(mute_role)
            embed = disnake.Embed(
                title='Снятие мута',
                description=f'Пользователь {interaction.author.mention} снял мут с пользователя {member.mention}'
            )
            await interaction.send(embed=embed)
            ls_embed = disnake.Embed(
                title='Снятие мута',
                description='С вас снят мут'
            )
            await member.send(embed=ls_embed)
    


    @commands.slash_command(name='warn')
    async def warn(self, interaction, member: disnake.Member, reason='Не указана'):
        if member == interaction.author:
            embed = disnake.Embed(
                title='Ошибка применения',
                description='Вы не можете выдать наказание самому себе'
                )
            await interaction.send(embed=embed)
        else:
            warn_count = cursor.execute("SELECT warn FROM warn WHERE member_id = ?", (member.id,)).fetchone()[0]
            mute_role = disnake.utils.get(member.guild.roles, id=1109432156037595156)
            if warn_count == 3:
                cursor.execute('UPDATE warn SET warn = warn - 3 WHERE member_id = ?',(member.id,))
                db.commit()
                await interaction.send(f'{interaction.author} выдает последнее предупреждение пользователю {member.mention} по причине {reason}. Пользователю {member.mention} выдан 12 часовой мут')
                await member.add_roles(mute_role)
                await asyncio.sleep(43200)
                await member.remove_roles(mute_role)
                ls_embed = disnake.Embed(
                title='Снятие мута',
                description='С вас снят мут'
            )
                await member.send(embed=ls_embed)
            else:
                cursor.execute("UPDATE warn SET warn = warn + 1 WHERE member_id = ?", (member.id,))
                db.commit()
                await interaction.send(f'{interaction.author.mention} выдал варн пользователю {member.mention}. Это повышает его предупреждений до {warn_count}. Причина: {reason}.')
    
    @commands.slash_command(name='unwarn')
    async def unwarn(self, interaction, member: disnake.Member):
        if member == interaction.author:
            embed = disnake.Embed(
                title='Ошибка применения',
                description='Вы не можете снять варн самому себе'
                )
            await interaction.send(embed=embed)
        else:
            warn_count = cursor.execute("SELECT warn FROM warn WHERE member_id = ?", (member.id,)).fetchone()[0]
            cursor.execute('UPDATE warn SET warn = warn - 1 WHERE member_id = ?', (member.id,))
            db.commit()
            await interaction.send(f'{interaction.author.mention} снимает варн пользователю {member.mention}. Это понижает количество его предупреждений до {warn_count}')
    

    @commands.slash_command(name='ban')
    async def ban(self,interaction,member:disnake.Member,reason='Не указана'):
         if member == interaction.author:
            embed = disnake.Embed(
                title='Ошибка применения',
                description='Вы не можете выдать наказание самому себе'
                )
            await interaction.send(embed=embed)
         else:
            ls_embed = disnake.Embed(
                title='Выдача бана',
                description=f'Вам был выдан вечный бан по причине: {reason} '
            )
            embed = disnake.Embed(
                title='Выдача бана',
                description=f'Пользователь {interaction.author} выдал бан пользователю {member.mention} по причине {reason}'
            )

            await member.ban
            await member.send(embed=ls_embed)
            await interaction.send(embed=embed)
    
    @commands.slash_command(name='unban')
    async def unban(self,interaction,member:disnake.Member):
         if member == interaction.author:
            embed = disnake.Embed(
                title='Ошибка применения',
                description='Вы не можете выдать наказание самому себе'
                )
            await interaction.send(embed=embed)
         else:
            ls_embed = disnake.Embed(
                title='Снятие бана',
                description=f'С вас был снят  бан '
            )
            embed = disnake.Embed(
                title='Снятие бана',
                description=f'С пользователя {member.mention} снят бан'
            )
            await member.unban
            await member.send(embed=ls_embed)
            await interaction.send(embed=embed)
        
              
            

def setup(bot):
    bot.add_cog(Moderation(bot))
