import discord
from discord import app_commands
from discord.ext import commands, tasks
import requests
import json
import random
import os
import itertools
from dotenv import load_dotenv

load_dotenv("bot.env")
token = os.getenv("BOT_TOKEN")

hunter = 485957450009149451
CHANNEL_ID = 1350541876167573686  # Rules channel
ROLE_ID = 1282826246488850495     # verified role
EMOJI = "✅"
ITEMS_PER_PAGE = 25
MSG_ID_FILE = "rules_msg_id.txt"

MEMES_FOLDERS = ["D:/Hrobe/Downloads/Memes", "/home/hdr/Desktop/memes"]
PEPE_FOLDERS = ["D:/Hrobe/Downloads/Memes/pepe", "/home/hdr/Desktop/memes/pepe"]
VIDEO_FOLDERS_1 = ["D:/Hrobe/Downloads/Memes", "/home/hdr/Desktop/memes"]
VIDEO_FOLDERS_2 = ["D:/Hrobe/Videos", "C:/Users/Hrobe/Videos"]

activities = [
    discord.Activity(type=discord.ActivityType.watching, name="veggie burger mukbang"),
    discord.Activity(type=discord.ActivityType.listening, name="fortniteballer100 - h.ntrr"),
    discord.Streaming(name="absolutely nothing", url="https://twitch.tv/charmanita"),
    discord.Game(name="guh buh ugh"),
]
class FileIndexView(discord.ui.View):
    def __init__(self, images, videos):
        super().__init__(timeout=60)
        self.images = images
        self.videos = videos
        self.page = 0
        self.all_files = (
            [f"🖼️ {f}" for f in images] +
            [f"🎬 {f}" for f in videos]
        )
        self.total_pages = max(1, (len(self.all_files) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    def build_embed(self):
        start = self.page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        chunk = self.all_files[start:end]
        embed = discord.Embed(
            title="📁 Memes Folder Index",
            description="\n".join(chunk) if chunk else "*Empty folder*",
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Page {self.page + 1}/{self.total_pages} | {len(self.images)} images, {len(self.videos)} videos")
        return embed

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.total_pages - 1:
            self.page += 1
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

# Definition of the function to grab memes from the Meme API. 

def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = json.loads(response.text)
    return json_data['url']

# Definition of function using CatAAS to grab random pictures of cats. 

def get_cat():
    response = requests.get('https://cataas.com/cat?json=true')
    json_data = response.json()
    return json_data['url']

# Function for getting random images from the folder paths from the MEME_FOLDERS

def get_random_image(*folder_paths, max_mb=25):
    images = []
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue
        images += [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))
            and os.path.getsize(os.path.join(folder_path, f)) <= max_mb * 1024 * 1024
        ]
    if not images:
        return None
    return random.choice(images)

# Function for getting random pictures from the Pepe Folders

def get_random_pepe(*folder_paths, max_mb=25):
    images = []
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue
        images += [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))
            and os.path.getsize(os.path.join(folder_path, f)) <= max_mb * 1024 * 1024
        ]
    if not images:
        return None
    return random.choice(images)

# Function for getting random videos from the VIDEO_FOLDERS_1
def get_random_video(*folder_paths, max_mb=25):
    videos = []
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue
        videos += [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(('mp4', 'mov', 'avi', 'mkv', 'webm'))
            and os.path.getsize(os.path.join(folder_path, f)) <= max_mb * 1024 * 1024
        ]
    if not videos:
        return None
    return random.choice(videos)

# Grabs random clips from my Windows PC to send (doesn't work on Pi due to storage constraints.)
def get_random_clip(*folder_paths, max_mb=25):
    videos = []
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue
        videos += [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(('mp4', 'mov', 'avi', 'mkv', 'webm'))
            and os.path.getsize(os.path.join(folder_path, f)) <= max_mb * 1024 * 1024
        ]
    if not videos:
        return None
    return random.choice(videos)

# Gets specific image that user chooses.
def get_specific_image(filename, *folder_paths):
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue
        full_path = os.path.join(folder_path, filename)
        if os.path.exists(full_path):
            return full_path
    return None
@tasks.loop(seconds=30)
async def rotate_status():
    await bot.change_presence(activity=next(activity_cycle))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Bot setup
class HunterBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync once here so slash commands register on startup.
        await self.tree.sync()
    # Rules embed for server
    def build_rules_embed(self):
        embed = discord.Embed(
            title="Welcome to hunter's gang! Please read the rules and click the checkmark to gain access to the server!",
            color=0x00ff95
        )
        embed.set_image(url="attachment://huntersgangembed.jpg")
        embed.add_field(name="1. No slurs", value="\u200b", inline=False)
        embed.add_field(name="2. No Racism", value="\u200b", inline=False)
        embed.add_field(name="3. No NSFW", value="\u200b", inline=False)
        embed.add_field(name="4. No spamming", value="\u200b", inline=False)
        embed.add_field(name="5. Be nice to everybody (no exceptions)", value="\u200b", inline=False)
        embed.add_field(name="6. Follow Discord TOS", value="All users need to strictly follow Discord [Terms of Service](https://www.discord.com/terms).", inline=False)
        embed.set_footer(text=f"React with {EMOJI} below to accept the rules and enjoy the server!")
        return embed
    # Setup for when bot initially starts up. 
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        # This is the way the bot checks what system it's on.
        global activity_cycle
        activity_cycle = itertools.cycle(activities)
        rotate_status.start()

        target_user = await self.fetch_user(hunter)
        await target_user.send("👍🏻")

        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print("Channel not found...")
            return

        embed = self.build_rules_embed()

        if os.path.exists(MSG_ID_FILE):
            msg_id = None
            with open(MSG_ID_FILE) as f:
                content = f.read().strip()
            if content:
                try:
                    msg_id = int(content)
                except ValueError:
                    print(f"Invalid content in {MSG_ID_FILE}, ignoring.")

            if msg_id is not None:
                try:
                    existing = await channel.fetch_message(msg_id)
                    await existing.edit(embed=embed)
                    print("Rules embed updated.")
                except discord.NotFound:
                    msg_id = None

            if msg_id is None:
                print("Previous message not found or file empty, resending...")
                my_file = discord.File("/home/hdr/Desktop/img/huntersgangembed.jpg", filename="huntersgangembed.jpg")
                message = await channel.send(file=my_file, embed=embed)
                await message.add_reaction(EMOJI)
                with open(MSG_ID_FILE, "w") as f:
                    f.write(str(message.id))
        else:
            my_file = discord.File("/home/hdr/Desktop/img/huntersgangembed.jpg", filename="huntersgangembed.jpg")
            message = await channel.send(file=my_file, embed=embed)
            await message.add_reaction(EMOJI)
            with open(MSG_ID_FILE, "w") as f:
                f.write(str(message.id))
            print("Rules embed sent.")

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return
        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return
        role = guild.get_role(ROLE_ID)
        member = guild.get_member(payload.user_id)
        if role and member:
            try:
                await member.add_roles(role)
                print(f"Successfully gave {role.name} role to {member.name}.")
            except discord.Forbidden:
                print("Error: Missing 'Manage Roles' permissions, or role is lower in hierarchy.")
            except discord.HTTPException:
                print("Failed to add role due to a network or Discord API error.")

    # Message triggers
    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.strip().lower()

        if content == 'meow':
            await message.channel.send("woof", file=discord.File("/home/hdr/Desktop/memes/puphunter.png"))

        if "clanker" in content:
            await message.channel.send(f'WHAT DID YOU CALL ME?! <@{message.author.id}>')


bot = HunterBot()


@bot.tree.command(name="help", description="List commands!")
async def help_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Commands:\n/meme - Get a random meme\n/whoami - See if I know you...\n/roll - Roll a number between 1 and 100\n"
        "/random - Get a random meme from <@485957450009149451>'s computer!\n/randompepe - Get a random Pepe the Frog meme!\n"
        "/randvid - Get a random meme video from <@485957450009149451>'s computer!\n/randclip - Get a random clip from <@485957450009149451>'s computer!\n"
        "/shutdown - Shutdown the bot (<@485957450009149451> only!)\n/ls - lists all images indexed with the bot (<@485957450009149451> only.)\n"
        "/image - pick an image from the list by filename."
    )


@bot.tree.command(name="meme", description="Grabs a random meme from the Meme API.")
async def meme(interaction: discord.Interaction):
    await interaction.response.send_message(get_meme())


@bot.tree.command(name="randocat", description="Send a random cat picture using CatAAS!")
async def randocat(interaction: discord.Interaction):
    await interaction.response.send_message(get_cat())


@bot.tree.command(name="whoami", description="See if I know you...")
async def whoami(interaction: discord.Interaction):
    await interaction.response.send_message(f"<@{interaction.user.id}>")


@bot.tree.command(name="roll", description="Roll a number between 1 and 100")
async def roll(interaction: discord.Interaction):
    await interaction.response.send_message(str(random.randint(1, 100)))


@bot.tree.command(name="random", description="Get a random meme from hunter's computer")
async def random_image_cmd(interaction: discord.Interaction):
    image_path = get_random_image(*MEMES_FOLDERS)
    if image_path:
        await interaction.response.send_message(file=discord.File(image_path))
    else:
        await interaction.response.send_message("No images found in the folder.")


@bot.tree.command(name="randompepe", description="Get a random Pepe the Frog meme")
async def randompepe(interaction: discord.Interaction):
    path = get_random_pepe(*PEPE_FOLDERS)
    if path:
        await interaction.response.send_message(file=discord.File(path))
    else:
        await interaction.response.send_message("No images found in the folder.")


@bot.tree.command(name="randvid", description="Get a random meme video from hunter's computer")
async def randvid(interaction: discord.Interaction):
    video_path = get_random_video(*VIDEO_FOLDERS_1)
    if video_path:
        await interaction.response.send_message(file=discord.File(video_path))
    else:
        await interaction.response.send_message("No videos found in this folder.")


@bot.tree.command(name="randclip", description="Get a random clip from hunter's computer")
async def randclip(interaction: discord.Interaction):
    video = get_random_clip(*VIDEO_FOLDERS_2)
    if video:
        try:
            await interaction.response.send_message(file=discord.File(video))
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Failed to send clip: {e}")
    else:
        await interaction.response.send_message("No videos found.")


@bot.tree.command(name="image", description="Send a specific image by filename")
@app_commands.describe(filename="The exact filename to look up")
async def image_cmd(interaction: discord.Interaction, filename: str):
    image_path = get_specific_image(filename.strip().lower(), *MEMES_FOLDERS)
    if image_path:
        await interaction.response.send_message(file=discord.File(image_path))
    else:
        await interaction.response.send_message("Image not found.")


@bot.tree.command(name="ls", description="List all indexed images/videos (owner only)")
async def ls_cmd(interaction: discord.Interaction):
    if interaction.user.id != hunter:
        await interaction.response.send_message("You are not sigma owner admin 💯🔥", ephemeral=True)
        return

    memes_folder = next((p for p in MEMES_FOLDERS if os.path.exists(p)), None)
    if memes_folder:
        files = os.listdir(memes_folder)
        images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        videos = [f for f in files if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]
        view = FileIndexView(images, videos)
        await interaction.response.send_message(embed=view.build_embed(), view=view)
    else:
        await interaction.response.send_message("Folder not found.")


@bot.tree.command(name="shutdown", description="Shut down the bot (owner only)")
async def shutdown_cmd(interaction: discord.Interaction):
    if interaction.user.id == hunter:
        await interaction.response.send_message('Shutting down...')
        await bot.close()
    else:
        await interaction.response.send_message("You are not sigma owner admin 💯🔥", ephemeral=True)


bot.run(token)