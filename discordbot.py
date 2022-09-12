from dis import disco
from re import I, S
from tkinter.ttk import Style
import discord
from discord import ui, app_commands
import functions.scrapefunc
import json
class MyClient(discord.Client):
    def __init__(self,intents):
        super().__init__(intents=intents)
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
    async def testing(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message("deez",ephemeral=True)

class ModalTest(ui.Modal,title = "Test modal"):
    answer = ui.TextInput(label="TESTING",style= discord.TextStyle.short, placeholder="placeholder test",required=True)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title,description=f"{self.answer.label}\n{self.answer}")
        embed.set_author(name = interaction.user,icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)


class SetupModal(ui.Modal,title = "Setup"):
    userNameAnswer = ui.TextInput(label="e-klase username",style=discord.TextStyle.short, placeholder="e-klases username",required=True)
    userPassAnswer = ui.TextInput(label="e-klase password",style=discord.TextStyle.short, placeholder="e-klases password",required=True)
    async def on_submit(self, interaction: discord.Interaction):
        checkResponse = functions.scrapefunc.checkLoginData(self.userNameAnswer, self.userPassAnswer)
        if checkResponse == 0x1:
            errEm = discord.Embed(title="Error",description="Username or password is incorrect\nPlease try again by using ***/start_setup***")
            await interaction.response.send_message(embed=errEm, ephemeral=True)

        if checkResponse == 0x21:
            errEm = discord.Embed(title="Error",description="E-klase.lv server problem\nPlease try again later by using ***/start_setup***")
            await interaction.response.send_message(embed=errEm,ephemeral=True)
        if checkResponse == 0x200:
            await interaction.response.send_message(f"Valid",ephemeral=True)
            with open("details.json", "r") as f:
                data = json.loads(f.read())
                data['payload1']['UserName'],data['payload1']['Password'] = str(self.userNameAnswer),str(self.userPassAnswer)
            with open("details.json","w") as f:
                f.write(json.dumps(data,indent=4))

        


class InitButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
    @discord.ui.button(label="Start", style=discord.ButtonStyle.blurple, custom_id="start")
    async def initB(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_modal(SetupModal())

    


intents = discord.Intents.default()
intents.message_content = True


client = MyClient(intents=intents)

tree = app_commands.CommandTree(client)

@tree.command(name="modal",description="pull up a test modal")
async def modal(interaction:discord.Interaction):
    await interaction.response.send_modal(ModalTest())
@tree.command(name="embed_button",description="sends a message with button")
async def butoun(interaction:discord.Interaction):
    await interaction.response.send_message(view=testButton())


@tree.command(name="start_setup",description="Starts setup sequence for e-scrape")
async def setupSeq(interaction:discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        embed = discord.Embed(title="Setup for E-scrape",description="Start the setup sequence for E-scrape by pressing the start button bellow.")
        embed.set_author(name="E-scrape",url="https://github.com/sodiumts/E-scrape",icon_url="https://cdn.discordapp.com/attachments/1017501822342144256/1018860380178612244/icon.jpg")
        await interaction.response.send_message(embed=embed,view=InitButton(),ephemeral=True)
    else:
        await interaction.response.send_message("You don't have the required permissions (administrator) to use the start_setup command",ephemeral=True)




client.run('MTAxNzM0MzY0NTcwNTMyNjY5NA.GG-Jd-.vAu6yBtv2VIksOslC9FZfCwpERjzauhupON0NU')