
import discord
from discord.client import Client
from discord.embeds import EmptyEmbed
from discord.ext import commands
import time
import datetime
import random
import asyncio
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import tzfe

client = commands.Bot(command_prefix = "~", help_command=None)

@client.event
async def on_ready():
    print(f"\n[{datetime.datetime.now()}] The bot, {client.user}, is ready\n")

@client.command()
async def hello(ctx):
    await ctx.send("Hello")

@client.command()
async def r(ctx, numMsgs):
    messages = await ctx.history(limit = int(numMsgs), before = ctx.message.created_at).flatten()    
    messages.reverse()
    filename = "record-" + str(ctx.message.created_at) + ".csv"
    namedfile = open(filename, "w")
    namedfile.write("Username, Server Nickname, Profile Picture, Time Sent, Message\n")
    for currentmsg in messages:
        nickname = ""
        if currentmsg.author.nick == None:
            nickname += currentmsg.author.name
        else:
            nickname += currentmsg.author.nick
        
        namedfile.write(f"{currentmsg.author},{nickname},{currentmsg.author.avatar_url},{currentmsg.created_at},{currentmsg.content}\n")
    namedfile.close()

    await ctx.send("Would you like to receive the file with the recorded messages? (yes/no)")

    def check(message):
        return ctx.author == message.author

    try:
        message = await client.wait_for("message", timeout=30, check=check)
    except asyncio.TimeoutError:
        await ctx.send("The file is no longer available for sending.")
        return None
    
    if message.content.lower() == "yes":
        await ctx.send("Here is the file.")
        recordFile = open(filename, "rb")
        await ctx.send(file = discord.File(fp = recordFile))
        recordFile.close()
    elif message.content.lower() == "no":
        await ctx.send("Okay, the record file won't be sent.")
    else:
        await ctx.send("I'll assume that that's a no.")

@client.command()
async def documentation(ctx):
    await ctx.send("https://discordpy.readthedocs.io/en/latest/api.html")

@client.command()
async def profile(ctx):
    mentioned = ctx.message.mentions
    if len(mentioned) == 0:
        mentioned.append(ctx.message.author)

    for user in mentioned:
        embed = discord.Embed(title = f"User Profile for {user.name}", colour = user.colour)
        embed.add_field(name = "Account Name", value = str(user), inline = False)
        created = user.created_at
        created_date = f"{created.strftime('%A')}, {created.strftime('%B')} {created.day}, {created.year}"
        embed.add_field(name = "Account Created On:", value = created_date, inline = False)
        embed.set_image(url = user.avatar_url)

        await ctx.send(embed = embed)

@client.command()
async def pfp(ctx):
    mentioned = ctx.message.mentions
    if len(mentioned) == 0:
        await ctx.send(ctx.message.author.avatar_url)
    elif len(mentioned) > 1:
        await ctx.send("You specified too many people for the command. Only mention one user,"
        + " or none if you want your own profile picture.")
    else:
        await ctx.send(mentioned[0].avatar_url)

@client.command()
async def flipcoin(ctx):
    await ctx.send("Flipping a coin...")
    await asyncio.sleep(3)
    choice = random.choice(range(1))
    if choice == 0:
        await ctx.send("It landed on heads.")
    else:
        await ctx.send("It landed on tails.")

@client.command()
async def rolldice(ctx, numDice):
    try:
        dice = int(numDice)
    except ValueError:
        await ctx.send("You have to specify a valid number of dice.")
        return None

    if dice == 1:
        await ctx.send("Rolling a die...")
    elif dice == 0:
        await ctx.send("You can't roll 0 dice.")
        return None
    else:
        await ctx.send(f"Rolling {dice} dice...")

    await asyncio.sleep(3)
    
    if dice == 1:
        await ctx.send(f"The die landed on {random.choice(range(1, 7))}.")
    else:
        message = ""
        for die in range(1, dice + 1):
            message += f"Die #{die} landed on {random.choice(range(1, 7))}.\n"
        await ctx.send(message)

@client.command()
async def google(ctx, *, search_term):
    if(ctx.author.id != 301087023744417792):
        no = await ctx.send("Only this bot's creator is allowed to use this command")
        
        def not_me_check(reaction, user):
            print("checking")
            return (user.id == 301087023744417792) and (reaction.message == ctx.message) and (reaction.emoji == "👍")

        try:
            reaction, user = await client.wait_for("reaction_add", timeout=30, check=not_me_check)
            await no.delete()
        except asyncio.TimeoutError:
            return None

    await ctx.trigger_typing()
    original_embed = discord.Embed(title="BudgetGoogle Inc.", colour=0xffffff, description=f"Your search term: \"{search_term}\"")
    original_embed.set_footer(text="Please wait; your search is loading.", icon_url="https://i0.wp.com/emoji.gg/assets/emoji/3859_Loading.gif")
    original_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/368px-Google_2015_logo.svg.png")
    embed_message = await ctx.send(embed=original_embed)
    path = "/Users/Sri/Desktop/chromedriver 2"
    driver = webdriver.Chrome(path)
    driver.get("https://google.com")
    search_bar = driver.find_element_by_name("q")
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)

    async def print_page(ctx, driver, embed_message):
        main_element = WebDriverWait(driver, 0.1).until(ec.presence_of_element_located((By.ID, "search")))
        search_results = main_element.find_elements_by_class_name("g")

        current_result = 0
        embed = discord.Embed(title="Google Search Results", colour=0xffffff)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/368px-Google_2015_logo.svg.png")
        embed.add_field(name="Search Term", value=f"\"{search_term}\"", inline=False)
        working_search_results = []
        for result in search_results:
            title = ""
            the_link = ""
            description = ""
            try:
                title += result.find_element_by_class_name("yuRUbf").find_element_by_tag_name("h3").text
                the_link += result.find_element_by_class_name("yuRUbf").find_element_by_tag_name("a").get_attribute("href")
                description += result.find_element_by_class_name("IsZvec").find_element_by_tag_name("div").text
                current_result += 1
                embed.add_field(name=f"({current_result}) {title}", value=f"{description}", inline=False)
                working_search_results.append(result)
            except selenium.common.exceptions.NoSuchElementException:
                pass
        navigation_field = ""
        for table_element in driver.find_element_by_id("xjs").find_elements_by_tag_name("td"):
            if table_element.get_attribute("class") == "YyVfkd":
                navigation_field += f".          ***{table_element.text}***          "
            else:
                navigation_field += f".          {table_element.text}          "
        navigation_field += "."
        embed.add_field(name="Page Navigation", value=navigation_field, inline=False)
        embed.description = "React to this message with the number of the chosen search result to get its hyperlink. \
            React with a forward arrow to go to the next page, or a backward arrow to go to the previous page."

        await embed_message.edit(embed=embed)
        await embed_message.clear_reactions()
        return [working_search_results, embed_message]
    
    no_page_changes = False
    while(no_page_changes == False):
        no_page_changes = True
        embed_return = await print_page(ctx, driver, embed_message)
        embed_message = embed_return[1]
        wsr = embed_return[0]
        action = ""
        # old_page_changers = ["▶️", "⏯", "⏭", "⏩", "➡️", "⏮", "⏪", "◀️", "⬅️"]
        page_changers = ["⬅️", "➡️"]
        number_reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        while len(number_reactions) > (len(embed_message.embeds[0].fields) - 2):
            number_reactions.pop()
        
        for option_reaction in number_reactions: await embed_message.add_reaction(option_reaction)
        for option_reaction in page_changers: await embed_message.add_reaction(option_reaction)
        
        def check(reaction, user):
            return (user == ctx.author) and (reaction.message == embed_message) and ((reaction.emoji in number_reactions) or (reaction.emoji in page_changers))
        
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
            await embed_message.reply("This Google search has timed out.")
            break
        if reaction.emoji in page_changers:
            no_page_changes = False

        if reaction == None: break

        if reaction.emoji in number_reactions:
            number_search = number_reactions.index(reaction.emoji)
            chosen_result = wsr[number_search]
            current_page = driver.find_element_by_id("xjs").find_element_by_class_name("YyVfkd").text
            embed_description = f"Here is the link for search result #{number_search + 1} on page {current_page}:\n"
            embed_description += chosen_result.find_element_by_class_name("yuRUbf").find_element_by_tag_name("a").get_attribute("href")
            embed = discord.Embed(title="Google Search Result", colour=0xffffff, description=embed_description)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/368px-Google_2015_logo.svg.png")
            await ctx.send(embed=embed)

        elif reaction.emoji == "➡️":
            if driver.find_element_by_id("xjs").find_elements_by_class_name("d6cvqb")[1].text == "":
                await ctx.send("You are at the last page of the search results, so there is no next page to go to. Please try again.")
            else:
                new_page_link = driver.find_element_by_id("xjs").find_elements_by_class_name("d6cvqb")[1].find_element_by_tag_name("a").get_attribute("href")
                driver.get(new_page_link)
        elif reaction.emoji == "⬅️":
            if driver.find_element_by_id("xjs").find_elements_by_class_name("d6cvqb")[0].text == "":
                await ctx.send("You are at the first page of the search results, so there is no previous page to go to. Please try again.")
            else:
                new_page_link = driver.find_element_by_id("xjs").find_elements_by_class_name("d6cvqb")[0].find_element_by_tag_name("a").get_attribute("href")
                driver.get(new_page_link)

    driver.close()

@client.command()
async def a(ctx):
    # await ctx.message.add_reaction("2️⃣")
    # await asyncio.sleep(5)
    # print(ctx.message.reactions)
    # print(await ctx.message.reactions[0].users().flatten())

    # print(await ctx.message.reactions[1].users().flatten())
    
    def check(channel, user, when):
        return False
    
    try:
        channel, user, when = await client.wait_for("typing", timeout=10, check=check)
        await ctx.send(channel)
        await ctx.send(type(channel))
        await ctx.send(user)
        await ctx.send(type(user))
        await ctx.send(when)
        await ctx.send(type(when))
    except asyncio.TimeoutError:
        await ctx.send("timed out. 10 seconds have passed.")

@client.command()
async def help(ctx):
    await ctx.send("Access denied.")

@client.command()
async def defaultavatar(ctx):
    mentioned = ctx.message.mentions
    if len(mentioned) == 0:
        mentioned.append(ctx.message.author)

    for user in mentioned:
        await ctx.send(user.default_avatar_url)

@client.command()
async def play2048(ctx):

    # def rectangular_string(matrix):
    #     string = ""
    #     max_digits = 1
    #     for i in range(len(matrix)):
    #         for j in range(len(matrix[0])):
    #             if len(str(matrix[i][j])) > max_digits:
    #                 max_digits = len(str(matrix[i][j]))
    #     new_matrix = [["-" for j in range((4 * len(matrix)) + 1)] for i in range((3 * len(matrix[0])) + 1)]
    #     #constructs the matrix
    #     for i in range(len(new_matrix)):
    #         for j in range(len(new_matrix[0])):
    #             if i == 0:
    #                 new_matrix[i][j] = "_"
    #             elif j % 4 == 0:
    #                 new_matrix[i][j] = "|"
    #             elif j % 2 == 0:
    #                 if (i - 1) % 3 == 0:
    #                     new_matrix[i][j] = " ".center(max_digits, "-")
    #                 elif (i - 2) % 3 == 0:
    #                     new_matrix[i][j] = (str(matrix[int((i-2)/3)][int((j-2)/4)])).center(max_digits)
    #                 elif i % 3 == 0:
    #                     new_matrix[i][j] = "_".center(max_digits, "-")
    #             elif i % 3 == 0:
    #                 new_matrix[i][j] = "_"
        
    #     #converts the matrix into a string
    #     for i in range(len(new_matrix)):
    #         for j in range(len(new_matrix[0])):
    #             string += new_matrix[i][j]
    #         string += "\n"

    #     return string
    def rectangular_string(matrix):
        string = ""

        max_digits = 1
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if len(str(matrix[i][j])) > max_digits:
                    max_digits = len(str(matrix[i][j]))

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if j == len(matrix[0]) - 1:
                    emoji_string = num2emoji(matrix[i][j])
                    string += emoji_string.center(max_digits + len(emoji_string) - len(str(matrix[i][j])), "🟦")
                elif j != len(matrix[0]) - 1:
                    emoji_string = num2emoji(matrix[i][j])
                    string += emoji_string.center(max_digits + len(emoji_string) - len(str(matrix[i][j])), "🟦") + "🟨"
            string += "\n"
            if i != len(matrix) - 1:
                for j in range((len(matrix[0]) * (max_digits + 1)) - 1):
                    string += "🟨"
                string += "\n"
        
        return string

    def num2emoji(number):
        numstring = str(number)
        emoji_string = ""
        for digit in numstring:
            if digit == "0":
                emoji_string += "🟦"
            elif digit == "1":
                emoji_string += "1️⃣"
            elif digit == "2":
                emoji_string += "2️⃣"
            elif digit == "3":
                emoji_string += "3️⃣"
            elif digit == "4":
                emoji_string += "4️⃣"
            elif digit == "5":
                emoji_string += "5️⃣"
            elif digit == "6":
                emoji_string += "6️⃣"
            elif digit == "7":
                emoji_string += "7️⃣"
            elif digit == "8":
                emoji_string += "8️⃣"
            elif digit == "9":
                emoji_string += "9️⃣"
        return emoji_string

    embed = discord.Embed(title="2048", colour=0xedc53f, description="Play a game of 2048!")
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/8/8a/2048_logo.png")
    key = "⬅️ - Move left\n" + \
        "➡️ - Move right\n" + \
        "⬆️ - Move up\n" + \
        "⬇️ - Move down\n" + \
        "❌ - End game"
    the_board = tzfe.Board(4, 4)
    embed.add_field(name="Key", value=key, inline=False)
    embed.add_field(name="Game Board", value=rectangular_string(the_board.board), inline=False)
    embed_message = await ctx.send(embed=embed)
    for r in ["⬅️", "⬆️", "⬇️", "➡️", "❌"]: await embed_message.add_reaction(r)

    def check(reaction, user):
        choices = ["⬅️", "➡️", "⬆️", "⬇️", "❌"]
        return (reaction.message == embed_message) and (user == ctx.author) and (reaction.emoji in choices)
    reason_for_end = ""
    while True:
    
        try:
            move, user = await client.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
            reason_for_end = "The game has timed out, and has therefore ended."
            break

        if move.emoji == "❌":
            reason_for_end = "You have exited the game."
            break
        
        footer = EmptyEmbed
        if move.emoji == "⬅️":
            if the_board.move_legal("left") == False:
                footer = "You are not able to move the tiles in that direction."
            else:
                the_board.move("left")
        elif move.emoji == "➡️":
            if the_board.move_legal("right") == False:
                footer = "You are not able to move the tiles in that direction."
            else:
                the_board.move("right")
        elif move.emoji == "⬆️":
            if the_board.move_legal("up") == False:
                footer = "You are not able to move the tiles in that direction."
            else:
                the_board.move("up")
        else:
            if the_board.move_legal("down") == False:
                footer = "You are not able to move the tiles in that direction."
            else:
                the_board.move("down")

        new_embed = discord.Embed(title="2048", colour=0xedc53f, description="Play a game of 2048!")
        new_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/8/8a/2048_logo.png")
        new_embed.add_field(name="Key", value=key, inline=False)
        new_embed.add_field(name="Game Board", value=rectangular_string(the_board.board), inline=False)
        new_embed.set_footer(text=footer)
        await embed_message.edit(embed=new_embed)

        if the_board.has_legal_move() == False:
            reason_for_end = "You lost the game."
            break

        await embed_message.remove_reaction(move, user)


    recap_embed = discord.Embed(title="Game Over", colour=0xedc53f, description=reason_for_end)
    recap_embed.add_field(name="Score", value=str(the_board.score), inline=True)
    recap_embed.add_field(name="Highest Tile", value=str(the_board.highest_tile()), inline=True)
    await embed_message.reply(embed=recap_embed)

@client.command()
async def ripbozo(ctx):
    mentioned = ctx.message.mentions
    if len(mentioned) == 0:
        mentioned.append(ctx.message.author)

    if len(mentioned) > 1:
        await ctx.send("You specified too many people for the command.")
    else:
        await ctx.message.delete()
        channel = client.get_channel(798013975266590743)
        audit_log_history = await channel.history(limit = 10).flatten()
        
        for message in audit_log_history:
            embed_description = message.embeds[0].description
            if embed_description.find("~ripbozo") != -1:
                await message.delete()
                break

        content = ""
        addendum = "#ripbozo " + mentioned[0].mention + " "
        while len(content) <= (2000 - len(addendum)):
            content += addendum

        await ctx.send(content)

@client.event
async def on_message(message):
    if(message.author == client.user):
        return None

    if "kys" in message.content and message.author.id == 355123587385917440:
        await message.channel.send("classic michael. still a yikes tho")
    elif "kys" in message.content and message.author.id != 355123587385917440:
        await message.channel.send("\"kys\" lmao michael moment")
    
    try:
        await client.process_commands(message)
    except discord.ext.commands.errors.MissingRequiredArgument:
        await message.channel.send("You have to send another argument to the command."
        + " For more information, try ~help. (btw the help command isn't done yet)")

client.run("ODY3MDk5NDYwNjIxOTU5MjA4.GO9TK8.pL9hr5NSu9iqzgQuaiWpDq0j6JvbRZUMSsIe2Q")