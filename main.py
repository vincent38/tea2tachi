import os
from typing import Optional

import libs.bridge as bridge
import discord
from discord import app_commands

DISCORD_KEY = os.getenv('DISCORD_KEY')
if DISCORD_KEY is None:
    raise Exception("Fatal - Missing Discord API key")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        #self.tree.copy_global_to()
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

# Manual sync command

@client.tree.command()
async def sync(interaction: discord.Interaction):
    """Starts a manual sync for the Tea and Tachi accounts linked to your Discord user"""
    await interaction.response.send_message(f'Hello, {interaction.user.name}, your import to Tachi is on the way :)', ephemeral=True)
    reply = bridge.executeBridge(interaction.user.id)
    reply_channel = interaction.channel
    await reply_channel.send(f'{interaction.user.mention} -> Sync process has ended. Reply from Bridge: {reply}')

# Account-related commands

@client.tree.command()
@app_commands.describe(
    tea_key='Your Tea API Key',
    tachi_key='Your Tachi API Key',
)
async def account_register(interaction: discord.Interaction, tea_key: str, tachi_key: str):
    """Binds your Tea and Tachi API keys to your Discord user"""
    reply = bridge.registerUser(interaction.user.id, tea_key, tachi_key)
    await interaction.response.send_message(f'Reply from Bridge: {reply}')
    
@client.tree.command()
@app_commands.describe(
    tea_key='The new Tea API Key to bind, leave empty if no modification.',
    tachi_key='The new Tachi API Key to bind, leave empty if no modification.',
)
async def account_edit(interaction: discord.Interaction, tea_key: Optional[str] = None, tachi_key: Optional[str] = None):
    reply = bridge.editUser(interaction.user.id, tea_key, tachi_key)
    await interaction.response.send_message(f'Reply from Bridge: {reply}')
    
@client.tree.command()
async def account_remove(interaction: discord.Interaction):
    reply = bridge.removeUser(interaction.user.id)
    await interaction.response.send_message(f'Reply from Bridge: {reply}')

# Logging commands

@client.tree.command()
async def logbook(interaction: discord.Interaction):
    """Lists all logs regarding sync requests. Does not reconciliate with Tachi statuses for now."""
    reply = bridge.logbook(interaction.user.id)
    print(reply)
    
    embed = discord.Embed(title='Logbook entries')
    
    index = 1
    for r in reply:
        embed.add_field(name='', value=f'{discord.utils.format_dt(r[0])} - {r[1]}', inline=True)
        index += 1
        if index > 11:
            break

    #embed.set_footer(text='Created').timestamp = channel.created_at
    await interaction.response.send_message(embed=embed)

client.run(DISCORD_KEY)