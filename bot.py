import modules
import os
import re
import requests
from flask import Flask, request


app = Flask(__name__)
GROUPS = {
    46649296: {"name": "Main Yale chat", "bot_id": "1520c98b3da635c8c6383951a6"},
    48071223: {"name": "Active chat", "bot_id": "d0bb06c46660d9bf5c5cb4fcff"},
    47894954: {"name": "Yalebot testing server", "bot_id": "d4e61d0ecd65cbabc8a7ad36e3"},
}
simple_responses = {
    "ping": "Pong!",
    "about": "Yalebot is maintained by Erik Bøsen, whom you should follow on Instagram @erikboesen. The bot's source code can be viewed and contributed to on GitHub: https://github.com/ErikBoesen/Yalebot",
    "flex": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "essays": "Submit your essays here, or read your classmates'! https://drive.google.com/open?id=1IUG1cNxmxBHhv1sSemi92fYO6y5lG6of",
    "spreadsheet": "https://docs.google.com/spreadsheets/d/10m_0glWVUncKCxERsNf6uOJhfeYU96mOK0KvgNURIBk/edit?fbclid=IwAR35OaPO6czQxZv26A6DEgEH-Qef0kCSe4nXxl8wcIfDml-BfLx4ksVtp6Y#gid=0",
}
commands = {
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "countdown": modules.Countdown(),
    "vet": modules.Vet(),
    "bulldog": modules.Bulldog(),
    "groups": modules.Groups(),
    "chat": modules.Chat(),
    "weather": modules.Weather(),
    "kelly": modules.Kelly(),
    "sad": modules.Sad(),
    "eightball": modules.EightBall(),
    "analytics": modules.Analytics(),
    "pick": modules.Pick(),
    "thatswhyichoseyale": modules.Chose(),
    "love": modules.Love(),
}
meme_commands = {
    "drake": modules.Drake(),
    "yaledrake": modules.YaleDrake(),
    "juice": modules.Juice(),
    "changemymind": modules.ChangeMyMind(),
}

F_PATTERN = re.compile('can i get an? (.+) in the chat', flags=re.IGNORECASE | re.MULTILINE)
H_PATTERN = re.compile('(harvard)', flags=re.IGNORECASE)
@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    group_id = int(message["group_id"])
    text = message["text"]
    name = message["name"]
    forename = name.split(" ", 1)[0]
    print("Message received: %s" % message)
    matches = F_PATTERN.search(text)
    if matches is not None and len(matches.groups()):
        reply(matches.groups()[0] + ' ❤', group_id)
    if message["sender_type"] != "bot":
        if text.startswith("!"):
            instructions = text[1:].split(" ", 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else None
            query = query.strip()
            # Check if there's an automatic response for this command
            if command in simple_responses:
                reply(simple_responses[command], group_id)
            elif command in commands:
                # If not, query appropriate module for a response
                response = commands[command].response(query, message)
                if response is not None:
                    reply(response, group_id)
            elif command in meme_commands:
                #reply("@" + message["name"], group_id, image=meme_commands[command].response(query))
                reply(meme_commands[command].response(query), group_id)
            elif command == "help":
                help_string = ">--- Yalebot Help ---\n\n"
                help_string += "Simple commands: " + ", ".join(["!" + title for title in simple_responses])
                help_string += "\n\n"
                help_string += "Tools:\n"
                for title in commands:
                    help_string += "- !" + title + ": " + commands[title].DESCRIPTION + "\n"
                help_string += "\nMemes: " + ", ".join(["!" + title for title in meme_commands])
                reply(help_string, group_id)
            else:
                reply("Command not found. Use !help to view a list of commands.", group_id)

        if text.startswith("@Yalebot "):
            reply(commands["chat"].response(text.split(" ", 1)[1], message), group_id)
        if H_PATTERN.search(text) is not None:
            reply(forename + ", did you mean \"" + H_PATTERN.sub("H******", text) + "\"? Perhaps you meant to say \"" + H_PATTERN.sub("The H Place", text) + "\" instead?", group_id)
        if "thank" in text.lower() and "yalebot" in text.lower():
            reply("You're welcome, " + forename + "! :)", group_id)
        if "dad" in text.lower():
            new_text = text.strip().replace("dad", "dyd").replace("Dad", "Dyd").replace("DAD", "DYD")
            reply("Hey " + forename + ", did you mean \"" + new_text + "\"?", group_id)
    if message["system"]:
        if not text.startswith("Poll '") and text.contains("the group") and not text.contains("changed name"):
            name = text.replace(" has rejoined the group", "").replace(" has joined the group", "")
            reply(commands["vet"].check_user(name), group_id)
    return "ok", 200

def reply(text, group_id, image: str = None):
    """
    Reply in chat.
    :param text: text of message to send.
    :param group_id: ID of group in which to send message.
    :param image: URL of image to attach.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": GROUPS[group_id]["bot_id"],
        "text": text,
    }
    if image is not None:
        print('Attaching image %s' % image)
        data["attachments"] = [
            {
                "type": "image",
                "url": image,
            }
        ]
    print(data)
    response = requests.post(url, data=data)

if __name__ == "__main__":
    pass
