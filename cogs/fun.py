import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball', help='Ask the magic 8-ball a question')
    async def eight_ball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."
        ]
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {random.choice(responses)}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name='meme', help='Generates a random meme')
    async def meme(self, ctx):
        memes = [
            "https://i.imgur.com/xyz123.jpg",
            "https://i.imgur.com/abc456.png"
        ]
        embed = discord.Embed(title="😂 Random Meme", color=discord.Color.gold())
        embed.set_image(url=random.choice(memes))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))