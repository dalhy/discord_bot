import discord
import asyncio
import pymongo

from discord.ext import commands
from pymongo import MongoClient

app = MongoClient('')
db = app['Viper']
users = db['users']

class prison_loja(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(description="Veja a loja com todos os itens.", usage="pex loja")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def loja(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=":shopping_cart: Loja", description="> Página principal da loja. Reaja para abrir a página da loja desejada.\n\n``×`` \t:pick: Picaretas\n``×`` \t:hammer: Machados\n``×`` \t:alarm_clock: Boosters")
            embed.set_footer(text="Use p.loja comprar (item) para comprar um item.")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("⛏️")
            await msg.add_reaction("🔨")
            await msg.add_reaction("⏰")
            try:
                while True:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=360, check=lambda reaction, user: reaction.message.id == msg.id and user.id == ctx.author.id)
                    emoji = str(reaction.emoji)
    
                    if emoji == '⛏️':
                        await msg.delete()
                        emb = discord.Embed(title=":shopping_cart: Loja", description="> Loja de picaretas.")
                        emb.add_field(name=":pick: Picaretas:", value="``×`` \tPicareta de madeira   100 Moedas (wooden_pickaxe)\n``×`` \tPicareta de pedra   500 Moedas (stone_pickaxe)\n``×`` \tPicareta de ferro   750 Moedas (iron_pickaxe)\n``×`` \tPicareta de diamante   1000 Moedas (diamond_pickaxe)")
                        emb.set_footer(text="Use p.loja comprar (item) para comprar um item.")
                        msg = await ctx.send(embed=emb)
                        await msg.add_reaction('⬅')
    
                    if emoji == '🔨':
                        await msg.delete()
                        emb = discord.Embed(title=":shopping_cart: Loja", description="> Loja de machados.")
                        emb.add_field(name=":hammer: Machados:", value="``×`` \tMachado de madeira   100 Moedas (wooden_axe)\n``×`` \tMachado de pedra   250 Moedas (stone_axe)\n``×`` \tMachado de ferro   500 Moedas (iron_axe)\n``×`` \tMachado de diamante   750 Moedas (diamond_axe)")
                        emb.set_footer(text="Use p.loja comprar (item) para comprar um item.")
                        msg = await ctx.send(embed=emb)
                        await msg.add_reaction('⬅')
    
                    if emoji == '⏰':
                        await msg.delete()
                        emb = discord.Embed(title=":shopping_cart: Loja", description="> Loja de boosters.")
                        emb.add_field(name=":alarm_clock: Boosters:", value="kkkk")
                        emb.set_footer(text="Use p.loja comprar (item) para comprar um item.")
                        msg = await ctx.send(embed=emb)
                        await msg.add_reaction('⬅')
    
                    if emoji == '⬅':
                        await msg.delete()
                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction("⛏️")
                        await msg.add_reaction("🔨")
                        await msg.add_reaction("⏰")
                        
            except asyncio.TimeoutError:
                await msg.delete()
            except Exception as e:
                await msg.delete()
                print(repr(e))

    @loja.command()
    async def comprar(self, ctx, *, args=None):
        try:
            user = users.find_one({"id": ctx.author.id})
            picareta = user["picareta"]
            
            if user is None:
                users.insert_one({"id": ctx.author.id, "moedas": 0, "ckitstarter": False, "picareta": None, "machado": None, "pedra": 0, "carvao": 0, "ferro": 0, "diamante": 0, "obsidian": 0})
                return await ctx.send("ℹ Você não estava registrado(a) em meu ``banco de dados``. Então, precisei registrá-lo. Use o comando novamente!")
                
            elif args is None:
                return await ctx.send("ℹ Você deve informar um Item válido para comprar.")
                
            elif args == "wooden_pickaxe":
                if user["moedas"] < 100:
                    return await ctx.send("ℹ Você não possui moedas suficientes para comprar este item.")
                elif picareta == "wooden_pickaxe":
                    return await ctx.send("ℹ Você já possui uma picareta de madeira.")
                else:
                    pagou = user["moedas"] - 100
                    users.update_one({'id': ctx.author.id}, {'$set': {"moedas": pagou, "picareta": "wooden_pickaxe"}})
                    await ctx.send(":shopping_cart: Você comprou uma ``Picareta de madeira`` por 100 Moedas!")
                    
            elif args == "stone_pickaxe":
                if user["moedas"] < 500:
                    return await ctx.send("ℹ Você não possui moedas suficientes para comprar este item.")
                elif picareta == "stone_pickaxe":
                    return await ctx.send("ℹ Você já possui uma picareta de pedra.")
                else:
                    pagou = user["moedas"] - 500
                    users.update_one({'id': ctx.author.id}, {'$set': {"moedas": pagou, "picareta": "stone_pickaxe"}})
                    await ctx.send(":shopping_cart: Você comprou uma ``Picareta de pedra`` por 500 Moedas!")
                    
            elif args == "iron_pickaxe":
                if user["moedas"] < 750:
                    return await ctx.send("ℹ Você não possui moedas suficientes para comprar este item.")
                elif picareta == "iron_pickaxe":
                    return await ctx.send("ℹ Você já possui uma picareta de ferro.")
                else:
                    pagou = user["moedas"] - 750
                    users.update_one({'id': ctx.author.id}, {'$set': {"moedas": pagou, "picareta": "iron_pickaxe"}})
                    await ctx.send(":shopping_cart: Você comprou uma ``Picareta de ferro`` por 750 Moedas!")
                    
            elif args == "diamond_pickaxe":
                if user["moedas"] < 1000:
                    return await ctx.send("ℹ Você não possui moedas suficientes para comprar este item.")
                elif picareta == "diamond_pickaxe":
                    return await ctx.send("ℹ Você já possui uma picareta de diamante.")
                else:
                    pagou = user["moedas"] - 1000
                    users.update_one({'id': ctx.author.id}, {'$set': {"moedas": pagou, "picareta": "diamond_pickaxe"}})
                    await ctx.send(":shopping_cart: Você comprou uma ``Picareta de diamante`` por 1000 Moedas!")
                    
            else:
                return await ctx.send("ℹ Você deve informar um Item válido para comprar. Use ``pex loja`` para ver os Items disponíveis.")
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")
        
def setup(client):
    client.add_cog(prison_loja(client))
