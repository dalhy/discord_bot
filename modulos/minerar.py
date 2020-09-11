import discord
import asyncio
import random
import pymongo

from discord.ext import commands
from pymongo import MongoClient

app = MongoClient('')
db = app['Viper']
users = db['users']

class prison_minerar(commands.Cog):
    def __init__(self, client):
        self.client= client
        
    @commands.group(description="Minere minérios.", usage="p.minerar")        
    @commands.cooldown(1, 1800, commands.BucketType.user)
    @commands.guild_only()
    async def minerar(self, ctx):
        try:
            user = users.find_one({"id": ctx.author.id})
            picareta = user["picareta"]
            experiencia = random.choice(1, 1, 1, 1, 1, 1, 2, 2, 2, 3)
            
            if user is None:
                users.insert_one({"id": ctx.author.id, "moedas": 0, "ckitstarter": False, "picareta": None, "machado": None, "pedra": 0, "carvao": 0, "ferro": 0, "diamante": 0, "obsidian": 0})
                return await ctx.send("ℹ Você não estava registrado(a) em meu ``banco de dados``. Então, precisei registrá-lo. Use o comando novamente!")
            
            elif picareta is None:
                return await ctx.send("ℹ Você deve ter uma ``picareta`` para minerar. Para obter uma, colete algum kit ou compre uma na loja!")
                
            elif picareta == "wooden_pickaxe":
                pedra = random.randint(2, 7)
                pedras = user['pedra'] + pedra
                users.update_one({"id": ctx.author.id}, {'$set': {"pedra": pedras}})

                embed = discord.Embed(color=0x00FF7F, title="⛏️ Mineração", description=f"> Mineração concluída! Você minerou:\n``×`` \t{pedra}x Pedras")
                await ctx.send(embed=embed)
                
            elif picareta == "stone_pickaxe":
                pedra = random.randint(3, 9)
                carvao = random.randint(2, 6)
                ferro = random.randint(1, 4)
                pedras = user['pedra'] + pedra
                carvoes = user['carvao'] + carvao
                ferros = user['ferro'] + ferro
                users.update_one({"id": ctx.author.id}, {'$set': {"pedra": pedras, "carvao": carvoes, "ferro": ferros}})

                embed = discord.Embed(color=0x00FF7F, title="⛏️ Mineração", description=f"> Mineração concluída! Você minerou:\n``×`` \t{pedra}x Pedras\n``×`` \t{carvao}x Carvões\n``×`` \t{ferro}x Ferro(s)")
                await ctx.send(embed=embed)
                
            elif picareta == "iron_pickaxe":
                pedra = random.randint(8, 24)
                carvao = random.randint(3, 7)
                ferro = random.randint(3, 5)
                diamante = random.randint(1, 3)
                pedras = user['pedra'] + pedra
                carvoes = user['carvao'] + carvao
                ferros = user['ferro'] + ferro
                diamantes = user['diamante'] + diamante
                users.update_one({"id": ctx.author.id}, {'$set': {"pedra": pedras, "carvao": carvoes, "ferro": ferros, "diamante": diamantes}})

                embed = discord.Embed(color=0x00FF7F, title="⛏️ Mineração", description=f"> Mineração concluída! Você minerou:\n``×`` \t{pedra}x Pedras\n``×`` \t{carvao}x Carvões\n``×`` \t{ferro}x Ferros\n``×`` \t{diamante}x Diamante(s)")
                await ctx.send(embed=embed)
                
            elif picareta == "diamond_pickaxe":
                pedra = random.randint(11, 36)
                carvao = random.randint(5, 11)
                ferro = random.randint(4, 9)
                diamante = random.randint(2, 5)
                obsidian = random.randint(1, 3)
                pedras = user['pedra'] + pedra
                carvoes = user['carvao'] + carvao
                ferros = user['ferro'] + ferro
                diamantes = user['diamante'] + diamante
                obsidianas = user['obsidian'] + obsidian
                users.update_one({"id": ctx.author.id}, {'$set': {"pedra": pedras, "carvao": carvoes, "ferro": ferros, "diamante": diamantes, "obsidian": obsidianas}})

                embed = discord.Embed(color=0x00FF7F, title="⛏️ Mineração", description=f"> Mineração concluída! Você minerou:\n``×`` \t{pedra}x Pedras\n``×`` \t{carvao}x Carvões\n``×`` \t{ferro}x Ferros\n``×`` \t{diamante}x Diamantes\n``×`` \t{obsidian}x Obsidiana(s)")
                await ctx.send(embed=embed)
                
            else:
                pass         
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")                
     
def setup(client):
    client.add_cog(prison_minerar(client))
