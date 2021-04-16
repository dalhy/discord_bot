import discord
import asyncio

from discord.ext import commands

class ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[OK] - {self.client.user.name} ({self.client.user.id} - Status: Online)")
        await self.client.change_presence(activity=discord.Activity(name="😊", type=1))

def setup(client):
    client.add_cog(ready(client))
