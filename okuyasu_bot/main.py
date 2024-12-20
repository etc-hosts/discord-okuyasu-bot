from asyncio import run as async_run
from os import getenv
from pathlib import Path
from random import choice

from discord import Intents, ApplicationContext, option, File
from discord.ext import commands
from dotenv import load_dotenv

from .logger import setup_logger


load_dotenv(Path(__file__).parent / '.env')
logger = setup_logger('okuyasu-bot', 'DEBUG')

GUILD_IDS = [int(guild_id) for guild_id in getenv('GUILD_IDS').split(',')]

PARENT_DIR = Path(__file__).parent
fact_pics = list(PARENT_DIR.glob('images/stills/facts/*'))


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=Intents.default(),
)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.slash_command(guild_ids=GUILD_IDS, name='8ball')
@option("question", description="Enter your question")
async def _8ball(
    ctx: ApplicationContext,
    question: str,
):
    responses = {
        'Dunno...': 30,
        'Woah. I think so!': 30,
        'Probably!': 30,
        'Nani?': 30,
        'Heck yea!': 30,
        'Yeheheheeeees >:^)': 30,
        'No way!': 30,
        'Defo yes!': 30,
        'Jaboll... Or whatever they say in Germany': 30,
        'Does the bear chill in the woods? Duh-doi, yes!': 30,
        "Naaah, c'mon... Nah.": 30,
        'Well yes, but actually no.': 20,
        'Whaddya think, Josuke? Yeh? Yeh.': 30,
        'What would aniki say... "Certainly".': 30,
        'No chance on any circle of hell!': 30,
        "Oi, piss off! I'm playing Budogaoka High's "
        "custom Minecraft server! "
        "Mikitaka won't leave Creative Mode...": 20,
        'Not in the mood for this... '
        'Unless you get me a choco strawberry cone!': 20,
        'Who cares?! Oi Josuke, look! '
        'I teleported bread using Za Hando!': 20,
        "I'd ask Koichi for you, "
        "but he's doing something with Jotaro-san in Italy.": 20,
        'No way Jose! Or Josuke, if you will!': 30,
        'The more important question is, are you feeling alright, bro? '
        'Have you been eating well? '
        'I got a �500 Makunouchi bento I can share if you really need it.': 20,
        "I didn't hear what you were saying, "
        "but can you get me a black tea with milk?": 20,
    }
    responses = await sort_responses(ctx.channel, responses)
    await ctx.respond(
        f'"{question}"\n'
        f'{choice([k for k in responses for _ in range(responses[k])])}',
    )


@bot.slash_command(guild_ids=GUILD_IDS)
async def fact(ctx: ApplicationContext):
    """
    Get a random Okuyasu fact
    """
    already_posted_pics = []
    async for message in ctx.channel.history(limit=30):
        for attachment in message.attachments:
            already_posted_pics.append(attachment.filename)
    fresh_pics = [str(pic) for pic in fact_pics if pic.name not in already_posted_pics]
    chosen_file = choice(fresh_pics if fresh_pics else fact_pics)
    logger.debug(f'Chosen file: {chosen_file}')
    await ctx.respond(file=File(chosen_file))


async def sort_responses(channel, responses: dict[str, int]) -> dict[str, int]:
    if channel is None:
        return responses

    messages = await channel.history(limit=50).flatten()
    last_few_messages_by_bot = [msg for msg in messages if msg.author == bot.user]
    for message in last_few_messages_by_bot:
        if message.content in responses.keys():
            if (responses[message.content] - 30) >= 1:
                content = responses[message.content] - 30
            else:
                content = 1
            responses[message.content] = content

    return responses


async def run_bot():
    async with bot:
        await bot.start(getenv('BOT_TOKEN'))


def run() -> None:
    async_run(run_bot())
