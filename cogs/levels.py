import discord
from discord.ext import commands
import sqlite3
import os

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('levels.db')
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS levels (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            )
        ''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Add XP
        self.cursor.execute('''
            INSERT OR IGNORE INTO levels (user_id) VALUES (?)
        ''', (message.author.id,))
        
        self.cursor.execute('''
            UPDATE levels SET xp = xp + ? WHERE user_id = ?
        ''', (random.randint(5, 15), message.author.id))
        self.conn.commit()

    @commands.command(name='rank', help='Shows your current level and XP')
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        self.cursor.execute('SELECT xp, level FROM levels WHERE user_id = ?', (member.id,))
        result = self.cursor.fetchone()
        
        if not result:
            xp, level = 0, 1
        else:
            xp, level = result
        
        embed = discord.Embed(
            title=f"📊 {member.display_name}'s Rank",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="XP", value=xp, inline=True)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))