# import discord

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

#     async def on_message(self, message):
#         print(f'Message from {message.author}: {message.content}')

# intents = discord.Intents.default()
# intents.message_content = True



# client = MyClient(intents=intents)


# @client.event
# async def on_ready():
#     print(f'{client.user.name} has connected to Discord!')


# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

# client.run('MTAxNzM0MzY0NTcwNTMyNjY5NA.GA0UwB.JXoWhFEcBXzbkNzy9P22ft_KGYAzoEGTfHcdq4')


import discord
from discord import ui, app_commands

class MyClient(discord.Client):
    def __init__(self,intents):
        super().__init__(intents=intents                )
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Logged on as {self.user}!')

class testButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="testing",style=discord.ButtonStyle.danger, custom_id="test")
    async def testing(self,interaction:discord.Interaction, button:discord.ui,Button):
        await interaction.response.send_message("deez",ephemeral=True)

class ModalTest(ui.Modal,title = "Test modal"):
    answer = ui.TextInput(label="TESTING",style= discord.TextStyle.short, placeholder="placeholder test",required=True)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title,description=f"{self.answer.label}\n{self.answer}")
        embed.set_author(name = interaction.user,icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed )

intents = discord.Intents.default()
intents.message_content = True


client = MyClient(intents=intents)

tree = app_commands.CommandTree(client)

@tree.command(name="modal",description="pull up a test modal")
async def modal(interaction:discord.Interaction):
    await interaction.response.send_modal(ModalTest)
@tree.command(name="embed_button",description="sends a message with button")
async def butoun(interaction:discord.Interaction):
    await interaction.response.send_message(view=testButton())

client.run('MTAxNzM0MzY0NTcwNTMyNjY5NA.GA0UwB.JXoWhFEcBXzbkNzy9P22ft_KGYAzoEGTfHcdq4')