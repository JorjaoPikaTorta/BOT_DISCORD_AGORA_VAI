import discord
from discord.ext import commands
import os 

# Token vem da variável de ambiente (Render usa isso)
TOKEN = os.getenv("TOKEN")


# Usuário que o bot deve manter o nick
NICK_TARGET_ID = 765711397371379732  # Substitua pelo ID correto
NICK_TARGET_NAME = "MANCER GAMES"

# Usuário que o bot deve monitorar e mandar mensagem ao ficar online
MSG_TARGET_ID = 455011986267176972  # Substitua pelo ID correto
CHANNEL_ID = 1239254305131856025    # Canal onde a mensagem será enviada

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.presences = True  # Necessário para monitorar status online/offline

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    # Ajusta o nick na inicialização (se precisar)
    for guild in bot.guilds:
        member = guild.get_member(NICK_TARGET_ID)
        if member and member.nick != NICK_TARGET_NAME:
            try:
                await member.edit(nick=NICK_TARGET_NAME, reason="MANCER GAMES (startup fix)")
                print(f"✅ Nick ajustado no servidor: {guild.name}")
            except Exception as e:
                print(f"❌ Erro ao ajustar no servidor {guild.name}: {e}")

@bot.event
async def on_member_update(before, after):
    # Restaurar nick do usuário alvo (NICK_TARGET_ID)
    if after.id == NICK_TARGET_ID and after.nick != NICK_TARGET_NAME:
        try:
            await after.edit(nick=NICK_TARGET_NAME, reason="MANCER GAMES (prevenção de troca)")
            print(f"✅ Nick restaurado para '{NICK_TARGET_NAME}'")
        except Exception as e:
            print(f"❌ Erro ao tentar restaurar o nick: {e}")

@bot.event
async def on_presence_update(before, after):
    # Verifica se é o usuário que deve receber mensagem (MSG_TARGET_ID)
    if after.id == MSG_TARGET_ID:
        # Checa se o usuário acabou de ficar online
        if after.status == discord.Status.online and before.status != discord.Status.online:
            print(f"✅ {after.name} acabou de ficar online!")
            
            for guild in bot.guilds:
                member = guild.get_member(MSG_TARGET_ID)
                if member:
                    channel = guild.get_channel(CHANNEL_ID)
                    if channel:
                        try:
                            await channel.send(f"VAI SE FUDER <@{MSG_TARGET_ID}>! Bem-vindo de volta sua bixinha! 🎉")
                            print("✅ Mensagem enviada com sucesso!")
                        except Exception as e:
                            print(f"❌ Erro ao enviar mensagem: {e}")

bot.run(TOKEN)
