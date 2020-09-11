import discord

from pymongo import MongoClient
from discord.ext import commands

app = MongoClient("") # Url do MongoDB
db = app.Viper
guilds = db['guilds']

client = commands.Bot(command_prefix="pex ", case_insensitive=True)
sharded = discord.AutoShardedClient(shard_count=2, shard_ids=(1, 2))
client.remove_command('help')

for extension in __import__("pathlib").Path('./modulos').glob('**/*.py'):
    ext_file = str(extension).replace('/','.').replace('\\','.')[:-3]
    ext_name = '.'.join(ext_file.split('.')[1:])
    try:
        client.load_extension(ext_file)
        print(f"Módulo [{ext_name}] carregado!")
    except commands.NoEntryPointError:
        if not str(extension).startswith("_"):
            print(f'Módulo [{ext_name}] ignorado! "def setup" não encontrado!!')
    except:
        print(f"\n\n{'='*10} [{ext_name}] Falhou! {'='*70}\n\n{__import__('traceback').format_exc()}\n{'-' * 100}")
 
 
try:
    client.run("") # Token
    print(f'[OK] - Conectado ao Discord(Bot)')
except Exception as e:
    print(f'[Erro] - Não foi possível conectar ao discord(Bot)\n[Erro] - {e}')