import discord
from discord.ext import commands
import os
from renderhtml import Renderer
import re
import time
import subprocess

class Kotoba(commands.Cog, name='Kotoba'):
    def __init__(self, bot):
        self.bot = bot
        self.show_wrong = False
        self.history_limit = 99999999

    @commands.command(pass_context=True)
    async def stprogress(self, ctx, keyword=None):
        """Visualizes shiritori channel history"""
        # timer_start = time.process_time()

        if keyword == "full":
            self.show_wrong = True
        
        reply = await ctx.send("Reading channel history... (1/4)")
        message_history = [message async for message in ctx.channel.history(limit=self.history_limit)]
        st_history = [] # will be reversed initially, but smaller than msg_hist so we reverse this
        for msg in message_history:
            if self.show_wrong and msg.reactions:
                if msg.reactions[0].emoji =="❓" and msg.content:
                    st_history.append((msg.author.name, msg.content[:17], "wrong"))
                    # [:17] truncates the string if longer than 17 characters (length of "n!stprogress full")
            if msg.embeds:
                for embed in msg.embeds:
                    # Put responses into (author, word, feature) tuples
                    if embed.title and embed.title == "Shiritori Ended":
                        st_history.append(("","","end"))
                    elif len(embed.fields) == 3 and embed.fields[1].name == "It means":
                        player = embed.fields[0].name
                        player = player.split(' ', 1)[0]
                        word = embed.fields[0].value
                        word = re.findall("\\[(.*?)\\]", word)[0]
                        st_history.append((player, word, "correct"))

        st_history = st_history[::-1]
        # st_history.append(("","","continuing"))
        if len(st_history) == 0:
            await reply.edit(content="No shiritori game found!")
            return
            
        await reply.edit(content="Rendering html... (2/4)")
        renderer = Renderer(st_history)
        # renderer.viewhist()
        renderer.render('./render/out.html')
        renderer.viewhist()
        
        await reply.edit(content="Rendering image... (3/4)")
        # Prints each line as a seperate pdf page per css props in @page
        subprocess.run(['weasyprint', './render/out.html', './render/out.pdf'])
        # Renders combines pdf pages and converts to a png
        subprocess.run(['magick', './render/out.pdf', '-background', 'white', '-alpha', 'Remove', '-quality', '80', '-append', './render/out.png'])

        await reply.edit(content="Sending image... (4/4)")
        image = discord.File("./render/out.png")

        # timer_elapsed = time.process_time() - timer_start
        # await ctx.send(f"done in {timer_elapsed:.03f} seconds\nhere")
        await reply.edit(content="Here")
        await ctx.send(file=image)

async def setup(bot):
    await bot.add_cog(Kotoba(bot))

