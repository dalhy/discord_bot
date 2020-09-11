import discord

from discord.ext import commands
from pymongo import MongoClient

class prison_bot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["identificadores"], description="Veja a lista de indentificadores.", usage="pex ids")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def ids(self, ctx):
        try:
            embed = discord.Embed(color=0x00FF7F, description="**:green_book: Identificadores**")
            embed.add_field(name=":pick: Picaretas", value="``×`` Picareta de Madeira = ``wooden_pickaxe``\n``×`` Picareta de Pedra = ``stone_pickaxe``\n``×`` Picareta de Ferro = ``iron_pickaxe``\n``×`` Picareta de Diamante = ``diamond_pickaxe``")
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")
        
    @commands.command(description="Veja meu tempo de respostas.", usage="pex ping")        
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx):
        try:
            await ctx.send(f"> :ping_pong: Pong. ``{self.client.latency * 1000}``ms")
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")
            
def setup(client):
    client.add_cog(prison_bot(client))
