TOKEN = "" #Paste your discord bot token here


import discord
from discord import ui, app_commands
from functions.scrapefunc import Scraper, DBManager
import json
import asyncio
from os.path import exists
from os import linesep
#initiate the discord client class
scrape = Scraper()
dbstuff = DBManager()
# lists = scrape.scrape_all(2)
# print(lists)
with open("functions/details.json", "r") as f:
    firstCheck = json.load(f)
if firstCheck["creds"]["UserName"] == "":
    print("################################################################################################")
    print("PLEASE START THE SETUP SEQUENCE BY TYPING THE /start_setup IN ANY CHANNEL!")
    print("################################################################################################\n")
class MyClient(discord.Client):
    def __init__(self,intents):
        super().__init__(intents=intents)
        self.synced = False 
    
    
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync() #sync the commands to the server
            self.synced = True
        print(f'Logged on as {self.user}!')
        self.bg_task = self.loop.create_task(self.scraping())
        # printer.start()
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    # async def setup_hook(self) -> None:
    #     self.bg_task = self.loop.create_task(self.scraping())
    async def scraping(self):
        # self.scr = self.loop.create_task(scrape.scrape_all(2))
        await self.wait_until_ready()
        boundid = None
        if exists("channelid.txt"):
            with open("channelid.txt") as f:
                boundid = f.readline()
        while not self.is_closed():
            if boundid != None:
                channel = self.get_channel(int(boundid))

            if boundid != None:
                response = scrape.scrape_all(2)
                message = ""
                # print(response)
                # if response["NewDescriptions"] != None:
                #     # for id in response["NewDescriptions"]:
                #     #     descStuff = dbstuff.get_info(id,"Descriptions")
                #     #     messageDesc = f"{descStuff[5]},{str(descStuff[2])}. {descStuff[4]}  {descStuff[3]}, {descStuff[3]}"
                #     #     print(messageDesc)
                #     message += f"New uniqueID in Descriptions: {response['NewDescriptions']}\n"
                if response["NewHomework"] != None:
                    message += f"New uniqueID in Homework: {response['NewHomework']}\n"
                    finalHWmsg = ""
                    for id in response["NewHomework"]:
                        homeworkStuff = dbstuff.get_info(id,"Lessons")
                        homeworkFormatted = homeworkStuff[3]
                        homeworkFormatted = linesep.join([s for s in homeworkFormatted.splitlines() if s])
                        messageHW = f"{homeworkStuff[5]} {str(homeworkStuff[2])}. {homeworkStuff[4]}  ***{homeworkStuff[1]}:*** *{homeworkFormatted.strip()}*\n"
                        finalHWmsg += messageHW
                    await channel.send(finalHWmsg)
                if response["NewTests"] != None:
                    message += f"New uniqueID in Tests: {response['NewTests']}\n"
                    finalTestMsg = ""
                    for id in response["NewTest"]:
                        testStuff = dbstuff.get_info(id,"Lessons")
                        messageTest = f"{testStuff[4]} {str(testStuff[2])}. {testStuff[3]}  ***{testStuff[1]}:*** **Plānots kontroldarbs!**\n"
                        finalTestMsg +=messageTest
                    await channel.send(finalTestMsg)
                
                await asyncio.sleep(600)
            else:
                if exists("channelid.txt"):
                    with open("channelid.txt") as f:
                        boundid = f.readline()
                # print("none")
                await asyncio.sleep(5)


##################################### TESTING CLASSES ####################################
# class testButton(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#     @discord.ui.button(label="testing",style=discord.ButtonStyle.danger)
#     async def testing(self,interaction:discord.Interaction, button:discord.ui.Button):
#         await interaction.response.send_message("deez",ephemeral=True)

# class ModalTest(ui.Modal,title = "Test modal"):
#     answer = ui.TextInput(label="TESTING",style= discord.TextStyle.short, placeholder="placeholder test",required=True)
#     async def on_submit(self, interaction: discord.Interaction):
#         embed = discord.Embed(title=self.title,description=f"{self.answer.label}\n{self.answer}")
#         embed.set_author(name = interaction.user,icon_url=interaction.user.avatar)
#         await interaction.response.send_message(embed=embed)
##################################### TESTING CLASSES ####################################

#defining the modal for the setup sequence
class SetupModal(ui.Modal,title = "Setup"):
    #define the 2 text inputs
    userNameAnswer = ui.TextInput(label="e-klase username",style=discord.TextStyle.short, placeholder="e-klases username",required=True)
    userPassAnswer = ui.TextInput(label="e-klase password",style=discord.TextStyle.short, placeholder="e-klases password",required=True)
    
    async def on_submit(self, interaction: discord.Interaction):
        #send the input data to scrapefunc.py to verify if its valid
        checkResponse = scrape.checkLoginData(self.userNameAnswer, self.userPassAnswer)
        
        #error for invalid creds
        if checkResponse == 0x1:
            errEm = discord.Embed(title="Error",description="Username or password is incorrect\nPlease try again by using ***/start_setup***")
            await interaction.response.send_message(embed=errEm, ephemeral=True)
        #error for E-klase.lv server issue
        if checkResponse == 0x21:
            errEm = discord.Embed(title="Error",description="E-klase.lv server problem\nPlease try again later by using ***/start_setup***")
            await interaction.response.send_message(embed=errEm,ephemeral=True)
        # valid credentials
        if checkResponse == 0x200:
            await interaction.response.send_message(f"Please select a channel to send alerts about new Homework and lessons by running ***/bind*** in the desired channel",ephemeral=True)
            #write the valid credentials to details.json
            with open("functions/details.json", "r") as f:
                data = json.loads(f.read())
                data['creds']['UserName'],data['creds']['Password'] = str(self.userNameAnswer),str(self.userPassAnswer)
            with open("functions/details.json","w") as f:
                f.write(json.dumps(data,indent=4))
            
            

#define buttton class for setup
class InitButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
    #button definition
    @discord.ui.button(label="Start", style=discord.ButtonStyle.blurple)
    async def initB(self, interaction:discord.Interaction, button:discord.ui.Button):
        #call SetupModal on button press
        await interaction.response.send_modal(SetupModal())

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
# context = app_commands.ContextMenu(client)

tree = app_commands.CommandTree(client)

###################### TESTING COMMANDS ##########################
# @tree.command(name="modal",description="pull up a test modal")
# async def modal(interaction:discord.Interaction):
#     await interaction.response.send_modal(ModalTest())
# @tree.command(name="embed_button",description="sends a message with button")
# async def butoun(interaction:discord.Interaction):
#     await interaction.response.send_message(view=testButton())
###################### TESTING COMMANDS ##########################

#define the command for the setup sequence
@tree.command(name="start_setup",description="Starts setup sequence for e-scrape")
#define the command to run when the command is called
async def setupSeq(interaction:discord.Interaction):
    #check if command caller has administrator permissions in the guild
    if interaction.user.guild_permissions.administrator:
        #define an embed for setup sequence
        embed = discord.Embed(title="Setup for E-scrape",description="Start the setup sequence for E-scrape by pressing the start button bellow.")
        embed.set_author(name="E-scrape",url="https://github.com/sodiumts/E-scrape")
        
        #send an embed with the InitButton 
        await interaction.response.send_message(embed=embed,view=InitButton(),ephemeral=True)
    else:
        await interaction.response.send_message("You don't have the required permissions (administrator) to use the start_setup command",ephemeral=True)

@tree.command(name="bind",description="Binds the printing of new tasks and tests to the current channel.")
async def bindCha(interaction:discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        boundid = interaction.channel_id
        with open("channelid.txt","w")as f:
            f.write(str(boundid))
        print(f"New bound channel at: {interaction.channel_id}")
        await interaction.response.send_message(f"Bound channel <#{interaction.channel_id}> as the channel for new entries from tests and lessons.",ephemeral=True)
@tree.command(name="less-descr",description="Makes a table with all the days in the week")
async def imgGen(interaction:discord.Interaction, weeks_ammount:int):
    await interaction.response.defer(ephemeral=True)
    count = scrape.imageGen(weeks=2)
    # await asyncio.sleep(5)
    for each in count:
        
        await interaction.channel.send(file=discord.File(f"functions/{each}.png"))
    await interaction.edit_original_response(content="done")
# @tree.command()
# @app_commands.describe(credentials="Credentials to change/input")
# async def credential(interaction:discord.Interaction,credentials:typing.Literal["Username","Password"],input_credentials:str):
#     await interaction.response.send_message(f'Your choice{credentials} and {input_credentials}')


#enter bot key in this field
client.run(TOKEN)