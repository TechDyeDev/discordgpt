from pathlib import Path

import discord

import ai

# Vars
CUR_DIR = Path(__file__).parent
KEY_FILE = CUR_DIR / "keys" / "discord.key"


# Discord
class MyClient(discord.Client):
	def __init__(self, intents):
		super().__init__(intents=intents)

	async def on_ready(self):
		print(f'Logged on as {self.user}!')

	async def on_message(self, message):
		if message.channel.id == 1235250952685224005 and self.user.id != message.author.id:
			answer = ai.generate_message(f"{message.content}")
			
			await message.channel.typing()
			await message.reply(answer, mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(KEY_FILE.read_text())