import discord
from discord import app_commands
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
GUILD_ID = 1466759785805516918
intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"Comandi sincronizzati per il server: {GUILD_ID}")

client = MyClient()

class OrdineModal(discord.ui.Modal, title='Nuovo Ordine Coffee Shop'):
    nome = discord.ui.TextInput(
        label = 'Nome Cognome',
        placeholder = "Jeff Smith",
        required=True
    )
    ordine = discord.ui.TextInput(
        label='Ordine',
        placeholder='10x10, 5x5',
        required=True
    )
    civ = discord.ui.TextInput(
        label='Civico',
        placeholder='100, 3030',
        required=False
    )
    num = discord.ui.TextInput(
        label = 'Numero di Telefono',
        placeholder = '(555) 123 4567',
        required=True
    )
    identificatore = discord.ui.TextInput(
        label = 'Mail Applicativo',
        placeholder = "(L'id scritto in piccolo nel profilo)",
        required=True
    )
    async def on_submit(self, interaction: discord.Interaction):
        canale_ordini = client.get_channel(1466939135322361899)
        embed_ordini = discord.Embed(
            title="🔔 Nuovo Ordine Ricevuto!",
            color=discord.Color.green(),
            timestamp=interaction.created_at
        )
        embed_ordini.add_field(name="Cliente", value=self.nome, inline=True)
        embed_ordini.add_field(name="Prodotto", value=self.ordine, inline=False)
        embed_ordini.add_field(name="civ", value=self.civ or "In sede", inline=False)
        embed_ordini.add_field(name="Num", value=self.num, inline=False)
        embed_ordini.add_field(name="id", value=self.identificatore, inline=False)
        await interaction.response.send_message(
            f'Grazie {interaction.user.mention}! Il tuo ordine è stato inviato allo staff. ☕', ephemeral=True)
        await canale_ordini.send(content="<@&1466774237099331651> <@&1466773674144174140> <@&1466773435530346641> <@&1466773824484933834>")
        await canale_ordini.send(embed=embed_ordini)

class MyView(discord.ui.View):
    @discord.ui.button(label="Effettua ordine!", style=discord.ButtonStyle.success, emoji="📝")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OrdineModal())

@client.event
async def on_ready():
    print(f'Loggato come {client.user}!')

@client.tree.command(name="ordine", description="manda embed ordini")
async def fattura(interaction: discord.Interaction):
    view = MyView()
    channel = 1466900540100182087
    embed = discord.Embed(
        title="Benvenuto nel sistema di ordini del coffee shop di Enveart!",
        description=f"Clicca il bottone qua sotto per effettuare un'ordine.",
        color=discord.Color.green()
    )
    await interaction.response.send_message("mandato!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)
client.run(TOKEN)
