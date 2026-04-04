import discord
import requests
import json
import random
import os
from dotenv import load_dotenv
load_dotenv("bot.env")
token = os.getenv("BOT_TOKEN")

hunter = 485957450009149451
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

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        if os.path.exists("/home/hdr/Desktop/memes"):
            status = "Running on Raspberry Pi"
        else:
            status = "Running on Windows"
        target_user = await self.fetch_user(485957450009149451)
        await target_user.send("I'm online master 😍")
        await self.change_presence(activity=discord.Game(name=status))

    async def on_message(self, message):
        if message.author == self.user:
            return

        # for specific person sending messages in channel 
        if message.author.id == 673341883577270313:
            gif_url = "https://cdn.discordapp.com/attachments/716426554380386354/1452761928366817311/bouncingpoof.gif?ex=69d1767a&is=69d024fa&hm=fc147bf4137cadbbd96a1588bd99a3b8e8caf6421c9e9d09bde00ab4bd4538c0&"
            embed = discord.Embed()
            embed.set_image(url=gif_url)
            await message.channel.send(random.choice(['shut up poof', 'you like femboys, right?', 'are u sped?' ]),
            embed=embed
            )
            return

        content = message.content.strip().lower()

        if content == 'help':
            await message.channel.send(
                "Commands:\n$meme - Get a random meme\nwhoami - See if I know you...\nroll - Roll a number between 1 and 100\nrandom - Get a random meme from <@485957450009149451>'s computer!\nrandompepe - Get a random Pepe the Frog meme!\nrandvid - Get a random meme video from <@485957450009149451>'s computer!\nrandclip - Get a random clip from <@485957450009149451>'s computer!\n!shutdown - Shutdown the bot (<@485957450009149451> only!)"
            )

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

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)