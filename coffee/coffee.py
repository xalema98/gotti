import discord
from discord import app_commands
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

nomi = []
fatture = []
iterazioni = 0

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

class FattureModal(discord.ui.Modal, title='Nuova Fattura Officina'):
    nome = discord.ui.TextInput(
        label = 'Nome Cognome',
        placeholder = "Jeff Smith",
        required=True
    )
    ordine = discord.ui.TextInput(
        label='Servizio',
        placeholder='10x10, 5x5',
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
            nomi[iterazioni] = id_utente
            fatture[iterazioni] = int(prezzo)
            iterazioni = iterazioni + 1
        canale_ordini = client.get_channel(1466939135322361899)
        embed_ordini = discord.Embed(
        title="🔔 Fattura creata!",
        color=discord.Color.green(),
        timestamp=interaction.created_at
    )   
        embed_ordini.add_field(name="Nome", value=self.nome, inline=True)
        embed_ordini.add_field(name="Servizio", value=self.ordine, inline=False)
        embed_ordini.add_field(name="prezzo", value='$' + prezzo, inline=False)
        embed_ordini.add_field(name="Data/ora", value=self.dataora, inline=False)
        await interaction.channel.send(embed=embed_ordini)
        await interaction.response.send_message("fattura inviata!", ephemeral=True)

class ordini_bott(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Effettua ordine!", style=discord.ButtonStyle.success, emoji="📝")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OrdineModal())

class fattura_bott(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Compila fattura!", style=discord.ButtonStyle.success, emoji="📝")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FattureModal())

@client.event
async def on_ready():
    print(f'Loggato come {client.user}!')

@client.tree.command(name="ordine", description="manda embed ordini")
async def ordine(interaction: discord.Interaction):
    ordini = ordini_bott()
    channel = 1466900540100182087
    embed = discord.Embed(
        title="Benvenuto nel sistema di ordini del coffee shop di Enveart!",
        description=f"Clicca il bottone qua sotto per effettuare un'ordine.",
        color=discord.Color.green()
    )
    await interaction.response.send_message("mandato!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=ordini)

@client.tree.command(name="fattura", description="manda embed fatture")
async def fattura(interaction: discord.Interaction):
    fattura = fattura_bott()
    channel = 1466900540100182087
    embed = discord.Embed(
        title="Benvenuto nel sistema di fatture del coffee shop di Enveart!",
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
            await interaction.response.send_message(f"l'utente <@{utente}> ha fatto ${fatture[i]} in fatture", ephemeral=True)
            controllo = 1
            break
    
    if(controllo != 1):
        await interaction.response.send_message("nessun utente trovato", ephemeral=True)

client.run(TOKEN)
