import discord
import pymongo

from discord.ext import commands
from pymongo import MongoClient

app = MongoClient('')
db = app['Viper']
users = db['users']

class prison_kits(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.group(description="Veja a lista com todos os kits.", usage="pex kits")        
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def kits(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                user = users.find_one({"id": ctx.author.id})
            
                if user is None:
                    users.insert_one({"id": ctx.author.id, "moedas": 0, "ckitstarter": False, "picareta": None, "machado": None, "pedra": 0, "carvao": 0, "ferro": 0, "diamante": 0, "obsidian": 0})
                    return await ctx.send("ℹ Você não estava registrado(a) em meu ``banco de dados``. Então, precisei registrá-lo. Use o comando novamente!")
                    
                else:
                    embed = discord.Embed(color=0x00FF7F, title="📦 Kits", description="> Seja bem-vindo ao menu de kits, todos os kits disponíveis estão listados abaixo.")
                    embed.add_field(name=":hammer_pick: Kit Inicial (kit_starter)", value="``×`` \t1x Picareta de Madeira\n``×`` \t1x Machado de Madeira\n``×`` \t100 Moedas")
                    embed.set_footer(text="Use p.kits coletar (kit) para obter um kit.")
                    await ctx.send(embed=embed)
            except Exception as e:
                print(f"[ERROR]: {repr(e)}")         

    @kits.command()
    async def coletar(self, ctx, *, args=None):
        try:
            user = users.find_one({"id": ctx.author.id})
            
            if user is None:
                users.insert_one({"id": ctx.author.id, "moedas": 0, "ckitstarter": False, "picareta": None, "machado": None, "pedra": 0, "carvao": 0, "ferro": 0, "diamante": 0, "obsidian": 0})
                return await ctx.send("ℹ Você não estava registrado(a) em meu ``banco de dados``. Então, precisei registrá-lo. Use o comando novamente!")
                
            elif args is None:
                return await ctx.send("ℹ Você deve informar um Kit válido para coletar.")
            elif args == "kit_starter":
                ckitstarter = user["ckitstarter"]
                if ckitstarter == True:
                    return await ctx.send("ℹ Você já coletou este kit anteriormente e não pode coletá-lo novamente.")
                else:
                    embed = discord.Embed(color=0x00FF7F, description="> 📦 ``Kit Inicial`` coletado com sucesso. Em seu inventário foi adicionado um ``Machado`` e uma ``Picareta`` de madeira, e 100 Moedas!")
                    await ctx.send(embed=embed)
                    moeda = user["moedas"] + 100
                    users.update_one({'id': ctx.author.id}, {'$set': {"moedas": moeda, "ckitstarter": True, "picareta": "wooden_pickaxe", "machado": "wooden_axe"}})
            else:
                return await ctx.send("ℹ Você deve informar um Kit válido para coletar. Opções disponíveis: ``kit_starter``")
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")
            
def setup(client):
    client.add_cog(prison_kits(client))
