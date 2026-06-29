import discord
import requests
import json
import random
import os
from dotenv import load_dotenv

load_dotenv("bot.env")
token = os.getenv("BOT_TOKEN")

hunter = 485957450009149451
CHANNEL_ID = 1520923759987523684  # Rules channel
ROLE_ID = 1520925875917295696     # verified role
EMOJI = "✅"
ITEMS_PER_PAGE = 25
MSG_ID_FILE = "rules_msg_id.txt"


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


def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = json.loads(response.text)
    return json_data['url']


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


def get_specific_image(filename, *folder_paths):
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue
        full_path = os.path.join(folder_path, filename)
        if os.path.exists(full_path):
            return full_path
    return None


class MyClient(discord.Client):
    def build_rules_embed(self):
        embed = discord.Embed(
            title="Welcome to charmanita.dev's server! Please read the rules and click the checkmark to gain access to the server!",
            color=0x00ff95
        )
        embed.set_image(url="attachment://charmanitadevembed.jpg")
        embed.add_field(name="1. Be respectful", value="Treat everybody with respect. Do not be disrespectful in any way, shape, or form just because you disagree on things or you think it's in a joking manner.", inline=False)
        embed.add_field(name="2. No Spamming", value="Do not spam in the server, keep it nice and tidy. Do not post links without asking the owner first.", inline=False)
        embed.add_field(name="3. Follow Discord TOS", value="All users need to strictly follow Discord [Terms of Service](https://www.discord.com/terms).", inline=False)
        embed.set_footer(text=f"React with {EMOJI} below to accept the rules and enjoy the server!")
        return embed

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        if os.path.exists("/home/hdr/Desktop/memes"):
            status = "Running on Raspberry Pi"
        else:
            status = "Running on Windows"

        target_user = await self.fetch_user(hunter)
        await target_user.send("I'm online master 😍")
        await self.change_presence(activity=discord.Game(name=status))

        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print("Channel not found...")
            return

        embed = self.build_rules_embed()

        if os.path.exists(MSG_ID_FILE):
            with open(MSG_ID_FILE) as f:
                msg_id = int(f.read().strip())
            try:
                existing = await channel.fetch_message(msg_id)
                await existing.edit(embed=embed)
                print("Rules embed updated.")
            except discord.NotFound:
                print("Previous message not found, resending...")
                my_file = discord.File("/home/hdr/Desktop/img/charmanitadevembed.jpg", filename="charmanitadevembed.jpg")
                message = await channel.send(file=my_file, embed=embed)
                await message.add_reaction(EMOJI)
                with open(MSG_ID_FILE, "w") as f:
                    f.write(str(message.id))
        else:
            my_file = discord.File("/home/hdr/Desktop/img/charmanitadevembed.jpg", filename="charmanitadevembed.jpg")
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

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.strip().lower()

        if content == 'h!help':
            await message.channel.send(
                "Commands:\n$meme - Get a random meme\nwhoami - See if I know you...\nroll - Roll a number between 1 and 100\nrandom - Get a random meme from <@485957450009149451>'s computer!\nrandompepe - Get a random Pepe the Frog meme!\nrandvid - Get a random meme video from <@485957450009149451>'s computer!\nrandclip - Get a random clip from <@485957450009149451>'s computer!\n!shutdown - Shutdown the bot (<@485957450009149451> only!)\nls - lists all images indexed with the bot (<@485957450009149451> only.)\nimage - start your message with image and type in any image in the list."
            )

        if content == 'meow':
            await message.channel.send("woof", file=discord.File("/home/hdr/Desktop/memes/puphunter.png"))

        if content == '$meme':
            await message.channel.send(get_meme())

        if content == 'whoami':
            await message.channel.send(f"<@{message.author.id}>")

        if "clanker" in content:
            await message.channel.send(f'WHAT DID YOU CALL ME?! <@{message.author.id}>')

        if content == 'roll':
            await message.channel.send(str(random.randint(1, 100)))

        if content == 'random':
            image_path = get_random_image("D:/Hrobe/Downloads/Memes", "/home/hdr/Desktop/memes")
            if image_path:
                await message.channel.send(file=discord.File(image_path))
            else:
                await message.channel.send("No images found in the folder.")

        if content == '!shutdown' and message.author.id == hunter:
            await message.channel.send('Shutting down...')
            await self.close()
        elif content == '!shutdown' and message.author.id != hunter:
            await message.channel.send("You are not sigma owner admin 💯🔥")

        if content == 'randvid':
            video_path = get_random_video("D:/Hrobe/Downloads/Memes", "/home/hdr/Desktop/memes")
            if video_path:
                await message.channel.send(file=discord.File(video_path))
            else:
                await message.channel.send("No videos found in this folder.")

        if content == 'randclip':
            video = get_random_clip("D:/Hrobe/Videos", "C:/Users/Hrobe/Videos")
            if video:
                try:
                    await message.channel.send(file=discord.File(video))
                except discord.HTTPException as e:
                    await message.channel.send(f"Failed to send clip: {e}")
            else:
                await message.channel.send("No videos found.")

        if content == 'randompepe':
            randompepe = get_random_pepe("D:/Hrobe/Downloads/Memes/pepe", "/home/hdr/Desktop/memes/pepe")
            if randompepe:
                await message.channel.send(file=discord.File(randompepe))
            else:
                await message.channel.send("No images found in the folder.")

        if content.startswith('image '):
            filename = content[6:].strip()
            image_path = get_specific_image(filename, "D:/Hrobe/Downloads/Memes", "/home/hdr/Desktop/memes")
            if image_path:
                await message.channel.send(file=discord.File(image_path))
            else:
                await message.channel.send("Image not found.")

        if content == 'ls' and message.author.id == hunter:
            memes_folder = next((p for p in ["D:/Hrobe/Downloads/Memes", "/home/hdr/Desktop/memes"] if os.path.exists(p)), None)
            if memes_folder:
                files = os.listdir(memes_folder)
                images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                videos = [f for f in files if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]
                view = FileIndexView(images, videos)
                await message.channel.send(embed=view.build_embed(), view=view)
            else:
                await message.channel.send("Folder not found.")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = MyClient(intents=intents)
client.run(token)