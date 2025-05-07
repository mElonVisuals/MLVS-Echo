import discord
from discord.ext import commands
from datetime import datetime

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command(name='hello', help='Greets the user with a friendly message')
    async def hello(self, ctx):
        embed = discord.Embed(
            title="👋 Hello!",
            description=f"Hi {ctx.author.mention}, I'm {self.bot.user.name}!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="Bot Info",
            value=f"• **Uptime:** {self.get_uptime()}\n• **Server Count:** {len(self.bot.guilds)}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', help='Displays information about the server')
    async def server_info(self, ctx):
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"🛠️ {guild.name} Server Info",
            color=discord.Color.blue()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
        
        if guild.description:
            embed.description = guild.description
        
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        
        embed.set_footer(
            text=f"Server ID: {guild.id} • Requested by {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url
        )
        
        await ctx.send(embed=embed)

    def get_uptime(self):
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        if days:
            return f"{days}d {hours}h {minutes}m"
        elif hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m {seconds}s"

async def setup(bot):
    await bot.add_cog(General(bot))