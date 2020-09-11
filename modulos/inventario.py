import discord
import asyncio
import random
import pymongo

from discord.ext import commands
from pymongo import MongoClient

app = MongoClient('')
db = app['Viper']
users = db['users']

class prison_inventario(commands.Cog):
    def __init__(self, client):
        self.client= client
        
    @commands.group(description="Veja seu inventário.", usage="p.inventario")        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def inventario(self, ctx):
        try:
            user = users.find_one({"id": ctx.author.id})
            
            if user is None:
                users.insert_one({"id": ctx.author.id, "moedas": 0, "ckitstarter": False, "picareta": None, "machado": None, "pedra": 0, "carvao": 0, "ferro": 0, "diamante": 0, "obsidian": 0})
                return await ctx.send("ℹ Você não estava registrado(a) em meu ``banco de dados``. Então, precisei registrá-lo. Use o comando novamente!")
                
            else:
                moeda = user["moedas"]
                pedra = user["pedra"]           
                carvao = user["carvao"]
                ferro = user["ferro"]
                diamante = user["diamante"]
                obsidian = user["obsidian"]     
                
                embed = discord.Embed(color=0x00FF7F, title="🎒 Inventário", description=f"> Este é o seu inventário:")
                embed.add_field(name=":credit_card: Moedas:", value=f"``×`` \tMoedas: {moeda}")
                embed.add_field(name=":alarm_clock: Boosters:", value=f"``×`` \tBooster x2 experiência:")
                embed.add_field(name=":mountain_snow: Minérios:", value=f"``×`` \tPedras: {pedra}\n``×`` \tCarvões: {carvao}\n``×`` \tFerros: {ferro}\n``×`` \tDiamantes: {diamante}\n``×`` \tObsidianas: {obsidian}")               
                await ctx.send(embed=embed)
                     
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")                
     
def setup(client):
    client.add_cog(prison_inventario(client))
