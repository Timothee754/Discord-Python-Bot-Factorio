import subprocess
import signal
import discord
from discord import app_commands
from dotenv import load_dotenv
import os
intents = discord.Intents.default()
intents.message_content = True

factorio_process = None  # process global

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"Connecté en tant que {self.user} (slash commands prêtes)")

client = MyClient()

@client.tree.command(name="up", description="Lance le serveur Factorio")
async def up(interaction: discord.Interaction):
    global factorio_process
    if factorio_process is None:
        await interaction.response.send_message("Serveur Factorio lancé")
        factorio_process = subprocess.Popen([
            "/opt/factorio/bin/x64/factorio", 
            "--start-server", 
            "newgame.zip"
        ])
    else:
        await interaction.response.send_message("Le serveur est déjà démarré")

@client.tree.command(name="down", description="Arrête le serveur Factorio")
async def down(interaction: discord.Interaction):
    global factorio_process
    if factorio_process:
        await interaction.response.send_message("Tentative d'arrêt du serveur...")
        factorio_process.send_signal(signal.SIGINT)
        factorio_process.wait()
        await interaction.followup.send("Serveur arrêté.")
        factorio_process = None
    else:
        await interaction.response.send_message("Le serveur n'est pas en cours d'exécution.")

@client.tree.command(name="shutdown", description="Arrete la machine et en conséquence le bot et le serveur.")
async def shutdown(interaction:discord.Interaction):
    subprocess.Popen(["shutdown", "now"])


# Ton token ici
TOKEN = os.getenv('PYTHON_TOKEN_BOT')

client.run(TOKEN)