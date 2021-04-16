import discord
import traceback, sys, re

from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        cmd_name = ctx.message.content.split()[0]

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f":information_source: {ctx.author.mention}, o comando ``{cmd_name}`` que você digitou, **não existe**!")

        if isinstance(error, commands.CommandOnCooldown):
            if int(error.retry_after) < 60:
                return await ctx.send(f':clock1: Você deve aguardar **{int(error.retry_after) % 60} segundo(s)** para utilizar este comando novamente!')
            elif int(error.retry_after) < 3600: 
                return await ctx.send(f':clock1: Você deve aguardar **{int(int(error.retry_after) / 60)} minuto(s) e {int(error.retry_after) % 60} segundo(s)** para utilizar este comando novamente!')
            elif int(error.retry_after) < 86400:
                return await ctx.send(f':clock1: Você deve aguardar **{int(int(error.retry_after) / 60 / 60)} hora(s) e {int(int(error.retry_after) / 60 % 60)} minuto(s)** para utilizar este comando novamente!')
            elif int(error.retry_after) >= 86400:
                return await ctx.send(f':clock1: Você deve aguardar **{int(int(error.retry_after) / 60 / 60 / 24)} dia(s) e {int(int(error.retry_after) / 60 / 60 % 24)} hora(s)** para utilizar este comando novamente!')

        if isinstance(error, commands.MissingPermissions):
            perms = "\n".join(error.missing_perms)
            return await ctx.send(f':information_source: {ctx.author.mention}, para executar o comando ``{cmd_name}`` você deve ter as seguintes permissões: ``{perms}``')

        if isinstance(error, commands.BotMissingPermissions):
            perms = "\n".join(error.missing_perms)
            return await ctx.send(f':information_source: {ctx.author.mention}, para executar o comando ``{cmd_name}`` eu preciso ter as seguintes permissões: ``{perms}``')
            
        if isinstance(error, commands.NotOwner):
            return await ctx.send(f':information_source: {ctx.author.mention}, apenas meus desenvolvedores podem usar este comando!')
            
        if isinstance(error, commands.UserInputError):
            try:
                usage = ctx.command.usage.replace('<command>', cmd_name) 
            except:
                pass
        
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(Errors(client))
