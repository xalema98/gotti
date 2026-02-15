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
GUILD_ID = 1467145084653932546
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

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

class FattureModal(discord.ui.Modal, title='Nuova Fattura Motel'):
    nome_tel = discord.ui.TextInput(
        label = 'Nome Cognome Affittuario e Telefono (RP)',
        placeholder = "Jeff Smith - (555)123 4567",
        required=True
    )
    camera = discord.ui.TextInput(
        label='Camera',
        placeholder='300, 200, 100',
        required=True
    )
    prezzo = discord.ui.TextInput(
        label='Prezzo',
        placeholder='6000, 90000',
        required=True
    )
    prenota = discord.ui.TextInput(
        label='Fino al:',
        placeholder='01/01/2026',
        required=True
    )
    async def on_submit(self, interaction: discord.Interaction):
        controllo = 0
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
        embed_ordini.add_field(name="Operatore", value=interaction.user.display_name) 
        embed_ordini.add_field(name="Nome affittuario e Numero", value=self.nome_tel, inline=False)
        embed_ordini.add_field(name="Camera", value=self.camera, inline=False)
        embed_ordini.add_field(name="Prezzo", value='$' + prezzo, inline=False)
        embed_ordini.add_field(name="Fino al", value=self.prenota)
        await interaction.response.defer(ephemeral=True)
        count = -1
        while controllo != 1 and count < 3:
            if count != -1:
                    await interaction.channel.purge(limit=2)
            for channel in client.get_all_channels():
                if str(self.camera) in channel.name:
                    nome_pulito = channel.name.replace("🟢", "").strip()
                    nuovo_nome = f"{nome_pulito}🔴"
                    controllo = 1
                    await channel.edit(name=nuovo_nome)
                    await interaction.channel.send(embed=embed_ordini)

            if controllo != 1:
                await interaction.followup.send("Camera non trovata, rispondi a questo messaggio con il corretto numero di camera, hai 1 minuto di tempo")
                ins = await client.wait_for("message", timeout=60.0)
                self.camera = ins.content
                count += 1
        if count == 3:
            await interaction.response.send_message("troppi tentativi", ephemeral=True)

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
    for i in range(iterazioni):
        nomi.pop(i)
        fatture.pop(i)
    await interaction.channel.purge(limit= iterazioni + 1)
    embed = discord.Embed(
        title="Benvenuto nel sistema di fatture del Manfredi's Motel di Enveart!",
        description=f"Clicca il bottone qua sotto per creare una fattura",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=fattura)

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

@client.tree.command(name="stato_camere", description="cambia lo stato delle camere del motel una volta fatto il checkout")
async def stato_camere(interaction: discord.Interaction, camera: str):
    controllo = 0
    for channel in client.get_all_channels():
            if camera in channel.name:
                nome_pulito = channel.name.replace("🔴", "").strip()
                nuovo_nome = f"{nome_pulito}🟢"
                controllo = 1
                if channel != nuovo_nome:
                    await channel.edit(name=nuovo_nome)
                    await interaction.response.send_message(f"L'affittuario della camera {camera} ha fatto il checkout!", ephemeral=True)
                else:
                    await interaction.response.send_message("La camera è già vacante", ephemeral=True)
    if controllo != 1:
        await interaction.response.send_message("Camera non trovata", ephemeral=True)

client.run(TOKEN)