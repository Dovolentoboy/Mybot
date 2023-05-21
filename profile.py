import sqlite3
import db as my_db
import disnake
import asyncio
from disnake.ext import commands
from DiscordLevelingCard import RankCard,Settings

db = sqlite3.connect('bot.db')
cursor = db.cursor()


class Profile(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        print('Профиля готовы')

    
    @commands.slash_command(name="rank")
    async def card(self,inter, user:disnake.Member=None):
        async def get_user_data(member):
            name = member.name
            tag = member.discriminator
            xp = cursor.execute("SELECT xp FROM users WHERE member_id = ?", (member.id,)).fetchone()[0]
            lvl = cursor.execute("SELECT lvl FROM users WHERE member_id = ?", (member.id,)).fetchone()[0]
            max_exp = 10 + 10 * lvl
            card_settings = Settings(
            background= "https://i.pinimg.com/originals/80/7c/a1/807ca16b42e5fe7dc8a5794157076559.png",
            text_color="white",
            bar_color="#5865f2"
            )
            await inter.response.defer()
            a = RankCard(
                settings=card_settings,
                avatar=user.display_avatar.url,
                level=lvl,
                current_exp=xp,
                max_exp=max_exp,
                username=f"{name}#{tag}"
            )
            image = await a.card3()
            await inter.edit_original_message(file=disnake.File(image, filename="rank.png"))
            return {'name':name,'xp':xp,'lvl':lvl,'max_exp':max_exp,'tag':tag}
        
        if user is None:
            user = inter.author
            await get_user_data(member=user)
        else:
            await get_user_data(member=user)

        
            
"""
Чтобы запустить код вам потребуется установить библиотеку - pip install discordlevelingcard

После чего код сработает)


"""        

        




def setup(bot):
    bot.add_cog(Profile(bot))
