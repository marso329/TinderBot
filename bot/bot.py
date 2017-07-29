import pynder
import time
import os
import sys
import unicodedata
import time
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

sys.path.insert(0,os.getcwd()+"/cleverwrap.py/cleverwrap")
from cleverwrap import CleverWrap

class bot:
    def __init__(self,_token,_facebook_id,cleverbot_key):
        self._token=_token
        self._facebook_id=_facebook_id
        self._session = pynder.Session( facebook_token=self._token,facebook_id=self._facebook_id)
        self._matches={}
        self._cleverbot_key=cleverbot_key
        matches=self._session.matches()
        for element in matches:
            cw = CleverWrap(self._cleverbot_key)
            self._matches[element.user.name]=BotMatch(element,cw)
    def print_matches(self):
        print("You have liked:")
        matches=self._session.matches()
        for element in matches:
            print(element)
    def talk(self,nr=1):
        counter=0
        for element in self._matches:
            self._matches[element].talk()
            counter+=1
            if counter==nr:
                return
    def match(self,nr=1):
        counter=0
        while True:
            try:
                users = self._session.nearby_users()
                for element in users:
                    time.sleep(1)
                    element.like()
                    print("liked "+ element.name)
                    if self._session.likes_remaining==0:
                        print("No more likes, more likes in"+str(self._session.can_like_in())+"seconds")
                        return
                    counter+=1
                    if counter==nr:
                        return
            except KeyError:
                if self._session.likes_remaining==0:
                    print("No more likes, more likes in"+str(self._session.can_like_in())+"seconds")
                    return
                
class BotMatch:
    def __init__(self,match,cleverbot):
        self._match=match
        self._cleverbot=cleverbot
        messages=self._match.messages
        for element in messages:
            if type(element.sender)!=pynder.models.me.Profile:
                self._cleverbot.say(element.body)
    def send_message(self,message):
        temp=unicodedata.normalize('NFKD', message).encode('ascii','ignore').decode()
        print("Sending: "+temp+" to:"+self._match.user.name)
        self._match.message(temp);
    def talk(self):
        messages=self._match.messages
        #init conversation
        if len(messages)==0:
            self.send_message(self._cleverbot.say(""))
            return
        #if the last message was from a match
        if type(messages[-1])!=pynder.models.me.Profile:
            temp=[]
            counter=-1
            #the match could have sent multiple messages
            while abs(counter)<=len(messages) and type(messages[counter])!=pynder.models.me.Profile:
                temp.append(messages[counter])
                counter-=1
            for i in range(len(temp)):
                mes=temp.pop()
                self.send_message(self._cleverbot.say(mes.body))
            return
        #handle if the match has not responded in a day
        time_now=datetime.now()
        time_now= pytz.UTC.localize(time_now)
        rdelta = relativedelta(time_now,messages[-1].sent)
        if rdelta.hours>1:
            self.send_message(self._cleverbot.say(""))
            return
            
        
            
        