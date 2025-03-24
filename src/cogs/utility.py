import discord
from discord.ext import commands
import random

class Utility(commands.Cog, name='Utility'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def test(self, ctx):
        """Test command"""
        await ctx.send("test")

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong"""
        await ctx.send(f"Pong :ping_pong: `{int(self.bot.latency*1000)} ms`")

    @commands.command(pass_context=True)
    async def add(self, ctx, left: int, right: int):
        """Addition calculator"""
        await ctx.send(left + right)
    @add.error
    async def add_error(self, ctx, error):
        await ctx.send('error...')

    @commands.command(pass_context=True)
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined"""
        await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')    

    @commands.command(pass_context=True)
    async def echo(self, ctx, arg):
        """Echo"""
        await ctx.send(arg)    

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """Flip coin..."""
        num = random.randint(0,1)
        res = ""
        if (num == 1):
            res = "heads :)"
        else:
            res = "tails :("
        await ctx.send(res)

async def setup(bot):
    await bot.add_cog(Utility(bot))
