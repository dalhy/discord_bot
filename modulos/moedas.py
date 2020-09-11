import discord

from discord.ext import commands
from pymongo import MongoClient

app = MongoClient('')
db = app['Viper']
users = db['users']

class prison_moedas(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    @commands.guild_only()
    @commands.is_owner()
    async def moedas(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Use ``pex moedas dar <user> <valor>`` para adicionar Moedas a um usuário, e ``pex moedas remover <user> <valor>`` para remover Moedas de um usuário.")

    @moedas.command()
    async def dar(self, ctx, user: discord.Member=None, valor: int=None):
        try:
            if user is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"ℹ {ctx.author.mention} Você deve marcar o usuário ao qual deseja adicionar as Moedas.")
            if valor is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"ℹ {ctx.author.mention} Você deve informar a quantia de Moedas que deseja adicionar.")

            mention = users.find_one({"id": user.id})
            if mention is None:
                return await ctx.send(f"ℹ {ctx.author.mention} Você deve informar a quantia de Moedas que deseja adicionar.")

            valor_mention = int(mention['moedas'])+int(valor)
            users.update_one({'id': user.id}, {'$set': {'moedas': valor_mention}})

            await ctx.send(f"💰 Você adicionou {valor} Moedas para o usuário ``{user.name}``.")
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")

    @moedas.command()
    async def remover(self, ctx, user: discord.Member=None, valor: int=None):
        try:
            if user is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"ℹ {ctx.author.mention} Você deve marcar o usuário do qual deseja remover as Moedas.")
            if valor is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"ℹ {ctx.author.mention} Você deve informar a quantia de Moedas que deseja remover.")

            mention = users.find_one({"id": user.id})
            if mention is None:
                return await ctx.send(f"ℹ {ctx.author.mention}, {user.mention} não está registrado(a) no ``banco de dados``.")

            valor_mention = int(mention['moedas'])-int(valor)
            users.update_one({'id': ctx.author.id}, {'$set': {'moedas': valor_mention}})

            await ctx.send(f"💰 Você removeu {valor} Moedas do usuário ``{user.name}``.")
        except Exception as e:
            print(f"[ERROR]: {repr(e)}")

def setup(client):
    client.add_cog(prison_moedas(client))
