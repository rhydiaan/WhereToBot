import random
import asyncio
import discord
from discord.ext import commands
from environ import TOKEN
import json

# Instantiate a discord client
client = commands.Bot(command_prefix = '>', help_command=None)


def load_from_json(filename): # Function to load the information from the JSON files
    with open(filename, 'r', encoding="utf8") as json_file:
        info = json.load(json_file)
    return info


country_info = load_from_json('Countries.json')
region_info = load_from_json('Regions.json')


async def help_embed(ctx, type): # Starts the embed to show the user how to use the functionality of the bot
    if type == "whereto": # If the type matches "whereto" then send the help embed for the whereto commands
        title = "Where to? Command Help"
    embed = discord.Embed( # Creating the help embed
        title=f'{title}',
        colour=discord.Colour.green()
    )

    if type == "whereto":
        embed.add_field(name='>whereto random', value='Throw a dart at the map and pick a random country'
        ' in the world to travel to!', inline=False)
        embed.add_field(name='>whereto region [region choice]', value='Throw a dart at the map and pick a random country'
        ' within the region chosen to travel to!', inline=False)
        embed.add_field(name='All regions to choose from', value='Africa, Asia, Europe, North America, Oceania, South America',
                        inline=False)

    await ctx.send(embed=embed) # Sending the help embed


async def whereto_embed(ctx, picked_country): # Starts the embed to show the information of the picked country
    embed = discord.Embed( # Creating the embed
        title=f'Pack your bags, you\'re going to {picked_country["name"]}!',
        description='-------',
        colour=discord.Colour.green()
    )
    embed.add_field(name=f'Here\'s information about the country!',
                    value=f'It\'s capital is {picked_country["capital"]}\n'
                    f'The native language is {picked_country["language"]["name"]}\n'
                    f'The country\'s currency is {picked_country["currency"]["name"]}'
                    f'. Symbol: {picked_country["currency"]["symbol"]}\n'
                    f'The country\'s region is: {picked_country["region"]}', inline=True)
    await ctx.send(embed=embed) # Sends the embed with all the information


async def whereto_region_picked(ctx, region): # If a region is picked by the user
    region_code = ""
    region_list = []
    for n in region_info: # To get the region Code of the specified region
        if region == n["name"]:
            region_code = n["code"]
    for i in country_info:
        # To check that the region code in the picked region and appends all countries within that region to a list
        if i["region"] == region_code:
            region_list.append(i)
    picked_country = random.choice(region_list) # Picks a random country from the list ("throwing the dart")
    await whereto_embed(ctx, picked_country) # Starts the embed function


async def whereto_random(ctx): # If the user wants a completely random country to be picked from the list
    picked_country = random.choice(country_info) # Picks a random country from the list and assigns to picked_country
    await whereto_embed(ctx, picked_country) # Starts the embed function




@client.command()
async def whereto(ctx, arg, arg2= None): # The whereto discord command
    if arg != None and arg.lower() == 'random': # If arg1 is random then start the random function
        await whereto_random(ctx)
    elif arg != None and arg.lower() == 'region' and arg2 != None: # If arg1 is region
        correct_region = False
        for i in region_info: # Ensuring arg2 is a region that is an option in the region list
            if arg2.lower() == i['name']: # If the region the user picked matches a region in the list
                await whereto_region_picked(ctx, arg2) # then start the region picked function
                correct_region = True
                break
        if correct_region == False: # Ensuring that if arg2 is not a region then send and error message to the user
            await ctx.send('That is not a usable region, please pick from: '
            'Africa, Asia, Europe, North America, Oceania, South America')

    elif arg != None and arg.lower() == 'help': # If arg1 is help then start the help embed_function
        await help_embed(ctx, 'whereto')
    else: # If none of the arguments are correct then send this error message to the user
        await ctx.message.add_reaction('❌')
        await ctx.send(f'">whereto [arg] [arg2]" Use ">whereto help" for help!')

# On ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">whereto help"))
    print('You have logged in as {0.user}'.format(client))

client.run(TOKEN)