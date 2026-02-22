import discord
from discord import app_commands
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

global nomi
global fatture
global iterazioni
nomi = []
fatture = []
iterazioni = 0


TOKEN = os.getenv("TOKEN")
GUILD_ID = 1466760040424935478
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

class FattureModal(discord.ui.Modal, title='Nuova Fattura Officina'):
    ordine = discord.ui.TextInput(
        label='Servizio',
        placeholder='kit riparazione, modifiche (elenco)',
        required=True
    )
    prezzo = discord.ui.TextInput(
        label='prezzo',
        placeholder='6000, 90000',
        required=True
    )
    dataora = discord.ui.TextInput(
        label='data e ora',
        placeholder='01/01/2026 22:30',
        required=True
    )
    async def on_submit(self, interaction: discord.Interaction):
        prezzo = str(self.prezzo)
        global nomi
        global fatture
        global iterazioni
        controllo = 0
        id_utente = interaction.user.id
        for i in range(iterazioni):
            if(id_utente == nomi[i]):
                fatture[i] = fatture[i] + int(prezzo)
                controllo = 1
                break
        if controllo != 1:
            nomi.append(id_utente)
            fatture.append(int(prezzo))
            iterazioni = iterazioni + 1
        canale_ordini = client.get_channel(1466939135322361899)
        embed_ordini = discord.Embed(
        title="🔔 Fattura creata!",
        color=discord.Color.green(),
        timestamp=interaction.created_at
    )   
        embed_ordini.add_field(name="Nome", value=interaction.user.display_name, inline=True)
        embed_ordini.add_field(name="Servizio", value=self.ordine, inline=False)
        embed_ordini.add_field(name="prezzo", value='$' + prezzo, inline=False)
        embed_ordini.add_field(name="Data/ora", value=self.dataora, inline=False)
        await interaction.channel.send(embed=embed_ordini)
        await interaction.response.send_message("fattura inviata!", ephemeral=True)

class fattura_bott(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Compila fattura!", style=discord.ButtonStyle.success, emoji="📝")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FattureModal())

@client.event
async def on_ready():
    print(f'Loggato come {client.user}!')

@client.tree.command(name="fattura", description="manda embed fatture")
async def fattura(interaction: discord.Interaction):
    fattura = fattura_bott()
    channel = 1466900540100182087
    embed = discord.Embed(
        title="Benvenuto nel sistema di fatture dell'officina Black Wolf di Enveart!",
        description=f"Clicca il bottone qua sotto per creare una fattura",
        color=discord.Color.green()
    )
    await interaction.response.send_message("mandato!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=fattura)

@client.tree.command(name="conto_settimanale", description="manda il resoconto settimanale dell'utente selezionato")
@app_commands.describe(tag="Inserisci il tag del dipendente selezionato")
async def conto_settimanale(interaction: discord.Interaction, tag: discord.Member):
    global nomi
    global fatture
    global iterazioni
    controllo = 0
    utente = tag.id
    for i in range(iterazioni):
        if(utente == nomi[i]):
            await interaction.response.send_message(f"Il dipendentee <@{utente}> ha fatto ${fatture[i]} in fatture", ephemeral=True)
            controllo = 1
            break
    
    if(controllo != 1):
        await interaction.response.send_message("nessun utente trovato", ephemeral=True)

client.run(TOKEN)
