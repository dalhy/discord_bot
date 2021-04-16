from discord.ext import commands

import discord

class on_mention(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
         if self.client.user.mention == message.content:
            await message.channel.send(f" Olá {message.author.mention}, deseja saber quais são meus comandos? Você pode vê-los digitando ``{self.client.prefix}ajuda``!")

def setup(client):
    client.add_cog(on_mention(client))
