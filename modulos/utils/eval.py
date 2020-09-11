import ast
import discord
import inspect
import asyncio
import traceback
import pymongo

from pymongo import MongoClient
from discord.ext import commands
from pprint import pformat

app = MongoClient('')
db = app['Viper']
users = db['users']

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def attr(func):
    lst = {'1: type': type(func).__name__, '3: methods': [], '2: attributes': []}
    for attr in [f for f in dir(func) if not f.endswith('_')]:
        try:
            attr_method = inspect.ismethod(getattr(func, attr))
            if not attr_method:
                lst['2: attributes'].append(f"{attr}")
            else:
                lst['3: methods'].append(f"{attr}")
        except:
            pass
    if len(lst['3: methods']):
        lst['3: methods'] = ", ".join(lst['3: methods'])
    else:
        del lst['3: methods']
    if len(lst['2: attributes']):
        lst['2: attributes'] = ", ".join(lst['2: attributes'])
    else:
        del lst['2: attributes']
    return lst

class eval_(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bot = client

    @commands.command(name="eval", aliases=['ev'])
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'client': ctx.bot,
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            'self': self,
            'channel': ctx.channel,
            'author': ctx.author,
            'message': ctx.message,
            'guild': ctx.guild,
            'getcmd': ctx.bot.get_command,
            'getcog': ctx.bot.get_cog,
            'source': inspect.getsource,
            'attr': attr,
            'users': users,
            '_get': discord.utils.get,
            '_find': discord.utils.find,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        try:
            result = (await eval(f"{fn_name}()", env))
            if inspect.isawaitable(result):
                result = await result
            if inspect.iscoroutine(result):
                result = await result
            result_type = str(type(result).__name__)
            if result_type != "str":
                result = pformat((result), width=80)
            result = result.replace('```py','').replace('```python','').replace('**','').replace('`','')
            text = f"Eval: Executado ✅ -> Tipo: {result_type}"
        except Exception as e:
            result = repr(e)
            text = "**Eval: Erro** ❌"

        ###############################################################################

        pages = commands.Paginator(prefix="```py", suffix='```', max_size=1900)
        for line in result.splitlines():

            # algumas linhas podem exceder o limite de carateres, então será necessário dividi-las
            if len(line) >= pages.max_size - 3:
                line2 = [(line[i:i + pages.max_size - 3]) for i in range(0, len(line), pages.max_size - 3)]
                for line3 in line2:
                    pages.add_line(line3)
            else:
                pages.add_line(line)

        pages = pages.pages
        max_pages = len(pages)-1

        page_count = f"**Página: 1/{max_pages+1}**" if max_pages else ""

        msg = await ctx.send(f"{text}{pages[0]}{page_count}")

        if max_pages:
            await msg.add_reaction('⬅')
            await msg.add_reaction('➡')
            try:
                def check(reaction, user):
                    return user == ctx.author and reaction.message.id == msg.id

                index = 0

                while True:

                    done, pending = await asyncio.wait([
                        ctx.bot.wait_for('reaction_remove', check=check),
                        ctx.bot.wait_for('reaction_add', check=check)], timeout=500,
                        return_when=asyncio.FIRST_COMPLETED)

                    [p.cancel() for p in pending]

                    if not done:
                        if ctx.channel.permissions_for(ctx.guild.me).manage_messages:
                            await msg.clear_reactions()
                        return await msg.add_reaction('🔒')

                    reaction, user = done.pop().result()

                    emoji = str(reaction.emoji)

                    if emoji == "➡":
                        if not index == max_pages:
                            index += 1
                        else:
                            index -= index
                        await msg.edit(content=f"{text}{pages[index]}**Página: {index + 1}/{max_pages+1}**")

                    elif emoji == "⬅":
                        if not index == 0:
                            index -= 1
                        else:
                            index += max_pages
                        await msg.edit(content=f"{text}{pages[index]}**Página: {index + 1}/{max_pages+1}**")

            except Exception:
                print(traceback.format_exc())

        ###############################################################################

    @eval_fn.error
    async def eval_error(self, ctx, error):

        if isinstance(error, commands.NotOwner): return
        await ctx.send(f"> Eval: Erro ❌\n```py\n{repr(error)}```")


def setup(client):
    client.add_cog(eval_(client))
