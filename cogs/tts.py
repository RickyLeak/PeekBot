from discord.ext import commands
from random import choice
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import box
from collections import Counter, defaultdict, namedtuple
import discord
import time
import os
import asyncio
import chardet

class TextToSpeech:
    """General commands."""
    def __init__(self, bot):
        self.bot = bot
        self.ttsEnabled = False

    @commands.group(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def tts(self, ctx):
        """Gives the current status of TextToSpeech"""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            if self.ttsEnabled:
                msg = box("TextToSpeech is currently enabled")
            else:
                msg = box("TextToSpeech is currently disabled")
            await self.bot.say(msg)

    @tts.command(pass_context=True)
    async def off(self, ctx):
        """Turn off TextToSpeech"""
        server = ctx.message.server
        msg = box("TextToSpeech Disabled")
        self.ttsEnabled = False
        await self.bot.say(msg)
        
    @tts.command(pass_context=True)
    async def on(self, ctx):
        """Turn on TextToSpeech"""
        server = ctx.message.server
        
        if self.is_playing(server):
            await ctx.invoke(self._queue, url=url)
            return  # Default to queue
        
                # Checking already connected, will join if not

        try:
            self.has_connect_perm(author, server)
        except AuthorNotConnected:
            await self.bot.say("You must join a voice channel before I can"
                               " play anything.")
            return
        except UnauthorizedConnect:
            await self.bot.say("I don't have permissions to join your"
                               " voice channel.")
            return
        except UnauthorizedSpeak:
            await self.bot.say("I don't have permissions to speak in your"
                               " voice channel.")
            return
        except ChannelUserLimit:
            await self.bot.say("Your voice channel is full.")
            return

        if not self.voice_connected(server):
            await self._join_voice_channel(voice_channel)
        else:  # We are connected but not to the right channel
            if self.voice_client(server).channel != voice_channel:
                await self._stop_and_disconnect(server)
                await self._join_voice_channel(voice_channel)
        
        msg = box("TextToSpeech Enabled")
        self.ttsEnabled = True
        await self.bot.say(msg)
        
#    @commands.command(pass_context=True, no_pm=True)
#    async def connect(self, ctx, *, url_or_search_terms):

    
    def is_playing(self, server):
        if not self.voice_connected(server):
            return False
        if self.voice_client(server) is None:
            return False
        if not hasattr(self.voice_client(server), 'audio_player'):
            return False
        if self.voice_client(server).audio_player.is_done():
            return False
        return True
        
    def voice_connected(self, server):
        if self.bot.is_voice_connected(server):
            return True
        return False
        
    
def setup(bot):
    bot.add_cog(TextToSpeech(bot))
