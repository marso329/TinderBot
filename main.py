from bot import bot
from facebooktoken import facebooktoken

print("Starting TinderBot")
credentials={}
f=open("credentials.txt")
for element in f:
    credentials[element.split(":")[0]]=element.split(":")[1].rstrip('\n')

token=facebooktoken.get_access_token(credentials["login"], credentials["pass"])
print("Facebook token fetched")
print("Starting bot")
tinderbot=bot.bot(token,credentials["facebook_id"],credentials["cleverbot_key"])
tinderbot.print_matches()
tinderbot.match()
tinderbot.talk(10)