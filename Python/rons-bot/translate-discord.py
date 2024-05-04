#!/Users/jeremyfriese/Desktop/BitBucketShared/env/bin/python3
import os
import sys
import discord
import googletrans
from googletrans import Translator
import json
from dotenv import load_dotenv


client = discord.Client()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
translator = Translator()
global last_message
last_message = "This is a placeholder"


@client.event
async def on_ready():
    print("/-- Translate -- Discord --\\")
    print("Logged in as: ")
    print(client.user.name)
    print(client.user.id)
    print("----------------------------")
    await client.change_presence(activity=discord.Game(name="The Dark Side"))
    print("--- Bot Presence Changed ---")
    print("")


@client.event
async def on_message(message):
    global last_message
    content = message.content
    #print(message)
    print(message.author.nick)
    if message.author.nick:
        name = message.author.nick
    else:
        name = message.author.name
    if content.startswith("!"):
        #print(client.get_user())
        # Makes the bot appear to be typing before sending its message
        #client.send_typing(message.channel)
        if " " in content:
            # When the user wants to call for help, or translate to more than english, this will parse their intention
            args = content.split(" ")[0].strip("!")
            print(args)
            if "-" in args:
                content = content[4:]
            else:
                content = content[2:]
            langcode = check_language(args, "language")
            #langcode = str(langcode).lower()
            if args.lower() == "help":
                help_message = "Type **.translate** to translate the message above to english.\n" \
                               " Type **.translate <language>** to translate it to that language."
                await client.send_message(message.channel, help_message)
            elif langcode != "False":
                if "-" in args:
                    content = content[4:]
                else:
                    content = content[3:]
                #langcode = str(langcode).strip()
                transText = translator.translate(content, dest = str(langcode))
                Text = transText.text
                Text = format_response(Text, content)
                await message.channel.send(Text)
                #await message.author.send(transText.text)
            else:
                print(content)
                transText = translator.translate(content, dest = "en")
                Text = transText.text
                Text = format_response(Text, content)
                print(Text)
                await message.channel.send(Text)
        else:
            print(content)
            transText = translator.translate(content, dest = "en")
            print(transText.text)
            await client.send_message(message.channel, transText.text)

    # Sets this message as the "ast message sent". Keep this at the END of the method
    last_message = content

# Takes in a string that may or may not be a language code.
# If it is a language code, it returns said code.
# If it is a language, it returns the affiliated code. If not, it returns -1
def check_language(code, target):
    with open('languages.json') as data:
        languages = json.load(data)
        for lang in languages:
            if (lang['language'].lower() == code.lower())or (lang['name'].lower() == code.lower()):
                return lang[target]
        return "False"


def format_response(response, content):
    langcode = translator.detect(content)
    item = str(langcode).split("=")[1]
    language_code = str(str(item).split(",")[0])
    print(language_code)
    language_name = check_language(language_code, "name")
    formatted_return = ("```" + "\n" + " \"" + response + "\"\n" + "```" + "\n" +
                        "**Source Language:** " + language_name + " **|** " + language_code + "\n")
    return formatted_return


client.run(TOKEN)
