# Authors: Leonardo Matone, Nancy Ng
# Date: 3.5.21
# Title: Discord Bot interface

import discord
import os
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
from calendarInterface import getEvents, addEvent, getAssignments, addAssignment

load_dotenv()
token = os.getenv('TOKEN')

# setup the client
client = discord.Client()

@client.event # When bot establishes connection to Discord:
async def on_ready():
  print("We have logged on as {0.user}".format(client))

# inspiration gimmick
inspirational = ["inspiration", "inspirational", "inspire", "inspired"]
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  jsonData = json.loads(response.text)
  quote = '"' + jsonData[0]['q'] + '" -' + jsonData[0]['a']
  return quote

@client.event # message gimmicks:
async def on_message(message):
  print(message.author)
  # if the message author is the user, return.
  if message.author == client.user:
    return

  # actions:
  if message.content.startswith("#"):
    print("this is a function, i will prepare to do things now")

    # add new reminder
    if "add" in message.content:
      newAssignment = message.content[5:]
      assignmentName = newAssignment.split(" ")[0]
      dueDate = newAssignment.split(" ")[1]
      # optionally, we can also use addEvent() to neglect the [Assignment] designation
      addAssignment(assignmentName, dueDate)
      outputString = 'New assignment: "'+ assignmentName + '" added to calendar, due: ' + dueDate
      await message.channel.send(outputString)

    # get next 10 events in your calendar and output in discord
    elif "getEvents" in message.content:
      events = getEvents()
      await message.channel.send("Below are your upcoming events: ")
      for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        fullEvent = "\t" + event['summary'] + ": " + start
        await message.channel.send(fullEvent)

    elif "view" in message.content:
      events = getAssignments()
      await message.channel.send("Below are your upcoming assignments: ")
      for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        fullEvent = "\t" + event['summary'] + ": " + start
        await message.channel.send(fullEvent)

    else:
      await message.channel.send("Hello! You've utilized my keyword. \n\nIf you'd like to set up a reminder, feel free to do so using:\n\t#add [assignment] [month-day]\n\n You can also view upcoming assignments with:\n\t#view assignments, or\n\t#getEvents (to view all upcoming events)")

  # gimmicks:
  for word in inspirational:
    if word in message.content:
      quote = get_quote()
      await message.channel.send(quote)
      break

  if message.content.startswith("hi"):
    await message.channel.send("hi")
  if message.content.startswith("ping"):
    await message.channel.send("pong")
  if message.content.startswith("bipitty"):
    await message.channel.send("bopitty")
  if "piss cum shit fart" in message.content or "bitch" in message.content:
    await message.channel.send("No foul language please.")
  if "NICE" in message.content:
    await message.channel.send("I know, right?")

# client = MyClient()
client.run(token)