import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import re
import time

async def raiseError(ctx, msg):
    await ctx.send(msg)
    return
