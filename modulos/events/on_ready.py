import discord
import asyncio

from discord.ext import commands

class ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[OK] - {self.client.user.name} ({self.client.user.id} - Status: Online)")
        while True:
            await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(name="Pex Beta", type=3))
            await asyncio.sleep(15)
            await self.client.change_presence(activity=discord.Activity(name="muita diversão. 😊", type=1))
            await asyncio.sleep(15)

def setup(client):
    client.add_cog(ready(client))
