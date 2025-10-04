import discord
from discord.ext import commands
import os 

# Token vem da variável de ambiente
TOKEN = os.getenv("TOKEN")


# Usuário que o bot deve manter o nick
NICK_TARGET_ID = 765711397371379732  
NICK_TARGET_NAME = "MANCER GAMES"

# Usuário que o bot deve monitorar e mandar mensagem ao ficar online (texto)
MSG_TARGET_ID = 455011986267176972  
CHANNEL_ID = 1239254305131856025    

# Usuário que deve receber mensagem + imagem
IMG_TARGET_ID = 638377524635893780  # <<< Substituir pelo ID do usuário

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.presences = True  # Necessário para monitorar status online/offline

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    # Ajusta o nick na inicialização
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
    # ---- Target 2: Mensagem de texto ----
    if after.id == MSG_TARGET_ID:

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

   # ---- Target 3: Mensagem + Imagem ----
if after.id == IMG_TARGET_ID:
    if after.status == discord.Status.online and before.status != discord.Status.online:
        print(f"✅ {after.name} acabou de ficar online (com imagem)!")

        for guild in bot.guilds:
            member = guild.get_member(IMG_TARGET_ID)
            if member:
                channel = guild.get_channel(CHANNEL_ID)
                if channel:
                    try:
                        file = discord.File("image.png", filename="image.png")  # Imagem local
                        await channel.send(
                            content=f"Você <@{IMG_TARGET_ID}>",
                            file=file
                        )
                        print("✅ Mensagem + imagem enviada com sucesso!")
                    except Exception as e:
                        print(f"❌ Erro ao enviar mensagem com imagem: {e}")
bot.run(TOKEN)
