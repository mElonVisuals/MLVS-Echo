import os
import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True,
            activity=discord.Game(name="Starting up...")
        )

        self.presence_messages = [
            discord.Activity(type=discord.ActivityType.watching, name="your commands"),
            discord.Activity(type=discord.ActivityType.listening, name="!help"),
            discord.Activity(type=discord.ActivityType.playing, name="with the API"),
            discord.Activity(type=discord.ActivityType.competing, name="in coding challenges")
        ]
        self.current_presence = 0

    async def setup_hook(self):
        await self.load_cogs()
        self.loop.create_task(self.animate_presence())
        
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"Error syncing slash commands: {e}")

    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                cog_name = f'cogs.{filename[:-3]}'
                try:
                    await self.load_extension(cog_name)
                    print(f'Loaded cog: {cog_name}')
                except Exception as e:
                    print(f'Failed to load cog {cog_name}: {e}')

    async def animate_presence(self):
        await self.wait_until_ready()
        while not self.is_closed():
            presence = self.presence_messages[self.current_presence]
            await self.change_presence(activity=presence)
            self.current_presence = (self.current_presence + 1) % len(self.presence_messages)
            await asyncio.sleep(30)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = MyBot()

@bot.command(name='help')
async def help_command(ctx, *, command: Optional[str] = None):
    """Shows help information"""
    if command:
        # Show help for specific command
        cmd = bot.get_command(command.lower())
        if not cmd:
            embed = discord.Embed(
                title="Command Not Found",
                description=f"No command named `{command}` found.",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        
        embed = discord.Embed(
            title=f"Command Help: {cmd.name}",
            description=cmd.help or "No description available",
            color=discord.Color.blue()
        )
        embed.add_field(name="Usage", value=f"`!{cmd.name} {cmd.signature}`", inline=False)
        
        if cmd.aliases:
            embed.add_field(name="Aliases", value=", ".join(f"`{a}`" for a in cmd.aliases), inline=False)
        
        embed.set_footer(text="<> = Required | [] = Optional")
        return await ctx.send(embed=embed)
    
    # Main help menu
    embed = discord.Embed(
        title="Bot Help Menu",
        description="Here are all the available command categories. Use `!help <command>` for more info.",
        color=discord.Color.blue()
    )
    
    # Add bot logo/thumbnail
    embed.set_thumbnail(url=bot.user.avatar.url)
    
    # Organize commands by cog
    for cog_name, cog in bot.cogs.items():
        commands_list = []
        for cmd in cog.get_commands():
            if not cmd.hidden:
                commands_list.append(f"• `!{cmd.name}` - {cmd.short_doc or 'No description'}")
        
        if commands_list:
            embed.add_field(
                name=f"**{cog_name}**",
                value="\n".join(commands_list),
                inline=False
            )
    
    # Add additional info
    embed.add_field(
        name="Support",
        value="Need help? Join our [support server](https://discord.gg/example)",
        inline=False
    )
    
    embed.set_footer(
        text=f"Requested by {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url
    )
    
    # Add interactive buttons
    view = View()
    
    # Button for command list
    button = Button(label="Show All Commands", style=discord.ButtonStyle.blurple)
    async def button_callback(interaction):
        all_commands = []
        for cmd in bot.commands:
            if not cmd.hidden:
                all_commands.append(f"`!{cmd.name}` - {cmd.short_doc or 'No description'}")
        
        commands_embed = discord.Embed(
            title="All Commands",
            description="\n".join(all_commands)[:2000],
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=commands_embed, ephemeral=True)
    
    button.callback = button_callback
    view.add_item(button)
    
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_command_error(ctx, error):
    """Error handler"""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Command Not Found",
            description=f"Use `!help` to see available commands.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Missing Argument",
            description=f"❌ {str(error)}",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Usage",
            value=f"`!{ctx.command.name} {ctx.command.signature}`",
            inline=False
        )
        embed.set_footer(text="<> = Required | [] = Optional")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description=f"An unexpected error occurred: ```{str(error)}```",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise error

if __name__ == "__main__":
    bot_token = os.getenv('DISCORD_TOKEN')
    if not bot_token:
        print("No DISCORD_TOKEN found in .env file")
    else:
        bot.run(bot_token)