#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CookieTipBot by Steve Richey

import tweepy, time, sys, json, random, re, os

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

conf_strings = ["Okay", "Alright", "Hey", "Yep", "Sure", "Mmhmm", "Yup", "You betcha", "Yeah", "Aight", "Of course", "Absolutely", "No problem", "Not a problem", "No problemo", "You know it", "100%", "Affirmative", "Roger that", "I'm on it", "Uh huh", "Alrighty", "Indeed"]
fail_strings = ["Darn", "Shoot", "Shucks", "Dang", "Uh oh", "Nope", "Sorry", "No", "Oops", "Oh no", "About that"]
nice_strings = ["nice", "friendly", "fine", "fancy", "pleasant", "neat", "rad", "generous", "cool", "sweet", "incredible"]
hi_strings =   ["Hi", "Yo", "Hello", "Hey there", "Greetings"]

def is_printable(s, coded='utf-8'):
    try: s.decode(coded)
    except UnicodeDecodeError: return False
    else: return True

def is_int(x):
    try: return int(x) == x
    except ValueError: return False

def account_add(name, amount):
    try:
        writefile = open('db.txt', 'a+b')
        writefile.write(name + ", " + str(amount) + "\n")
        writefile.close()
        
        print "added " + name
        
        return True
    except:
        return False

def account_close(name):
    try:
        file = open('db.txt', 'r')
        data = file.readlines()
        
        for account in data:
            if name in account:
                print "removing " + name
                data.remove(account)
        
        file.close()
        file = open('db.txt', 'w')
        
        for account in data:
            file.write(account + "\n")
        
        file.close()
        
        return True
    except:
        return False

def account_exists(name):
    filename = open('db.txt','r')
    filedata = filename.readlines()
    filename.close()
    
    for account in filedata:
        if name in account:
            return True
    
    return False

def account_balance(name):
    if account_exists(name):
        filename = open('db.txt','r')
        filedata = filename.readlines()
        filename.close()
        
        for account in filedata:
            if name in account:
                commaindex = account.find(",")
                balanceindex = commaindex + 1
                stringbal = account[balanceindex:]
                return int(stringbal)
    else:
        return 0

def account_change(name, amount):
    if account_exists(name):
        balance = account_balance(name)
        account_close(name)
        account_add(name, balance + amount)
        return True
    else:
        return False

def tweet_to(name, message, id):
    if id is not None:
        if not is_int(id):
            print "Reply_to malformed, was " + id
            return False
    
    if not is_printable(message):
        print "Content not printable, " + message
        return False
    
    if len(message) > 140:
            print "Content was too long, " + message
            return False
    
    tosend = "@" + name + " " + message
    
    try:
        if id == 0:
            api.update_status(tosend)
        else:
            api.update_status(tosend, id)
        print "Replied: " + tosend
    except tweepy.TweepError, e:
        print "Tried to tweet but failed, tried ", tosend, "error: ", e

def clean_db():
    try:
        filename = open('db.txt','r')
        filedata = filename.readlines()
        
        for line in filedata:
            if line.strip() == '':
                filedata.remove(line)
        
        filename.close()
        filename = open('db.txt', 'w')
        
        for line in filedata:
            filename.write(line)
        
        filename.close()
        
        return True
    except:
        return False

CONSUMER_KEY = open('consumer.key', 'r').readline().strip()
CONSUMER_SECRET = open('consumer_secret.key', 'r').readline().strip()
ACCESS_KEY = open('access.key', 'r').readline().strip()
ACCESS_SECRET = open('access_secret.key', 'r').readline().strip()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class StdOutListener(StreamListener):
    def on_status(self, status):
        user = status.user
        screen_name = user.screen_name
        text = status.text.lower()
        id = status.id
        
        if (user and text and id):
            if screen_name == "cookietipbot":
                return True
            
            print screen_name, "says", text
            
            type = ""
            
            if "new" in text:
                type = "new"
            
            if "close" in text:
                type = "cls"
            
            if "balance" in text:
                type = "bal"
            
            if "send" in text or "#cookietip" in text:
                if "bag" in text:
                    type = "bag"
                else:
                    type = "sen"
            
            if "help" in text:
                type = "hlp"
            
            if "clean" in text and screen_name == "stvr_tweets":
                type = "cln"
            
            if "more" in text and "please" in text:
                type = "mor"
            
            hasaccount = account_exists(screen_name)
            balance = account_balance(screen_name)
            
            message = random.choice(fail_strings) + ", I only understand new, balance, send (bag), help, close, or more please"
            
            if type == "new":
                if hasaccount:
                    message = "You already have an account!"
                else:
                    if account_add(screen_name, 10):
                        message = random.choice(conf_strings) + ", you have an account with 10 cookies!"
                    else:
                        message = random.choice(fail_strings) + ", I tried to open an account for you, but failed."
            
            if type == "cls":
                if not hasaccount:
                    message = random.choice(fail_strings) + ", You don't even have an account!"
                else:
                    if account_close(screen_name):
                        message = random.choice(conf_strings) + ", closed your account. :("
                    else:
                        message = random.choice(fail_strings) + ", I tried to close your account, but failed"
            
            if type == "bal":
                if hasaccount:
                    message = random.choice(conf_strings) + ", your balance is " + str(balance) + " cookies"
                else:
                    message = random.choice(fail_strings) + ", you don't have an account!"
            
            if type == "sen" or type == "bag":
                if hasaccount:
                    names = re.findall('(?<=@)\w+', text);
                    amount = 0
                    cookieword = "cookie"
                    
                    if type == "sen":
                        amount = 1
                    else:
                        amount = 5
                        cookieword = "cookies"
                    
                    message = random.choice(conf_strings) + ", you sent " + str(amount) + " " + cookieword + " to "
                    
                    for username in names:
                        if username is not screen_name:
                            if username != "cookietipbot":
                                if balance >= amount:
                                    account_change(screen_name, -amount)
                                    
                                    if account_exists(username):
                                        account_change(username, amount)
                                    else:
                                        account_add(username, 10 + amount)
                                        message_part = "cookie"
                                        
                                        if type == "bag":
                                            message_part = "bag of cookies"
                                        
                                        tweet_to(username, " " + random.choice(hi_strings) + "! @" + screen_name + " just sent you a " + message_part + ". You get 10 free too! How " + random.choice(nice_strings) + " is that!", 0)
                                    
                                    message += "@" + username + " "
                                else:
                                    message = random.choice(fail_strings) + ", you don't have any cookies to send!"
                                    break
                else:
                    message = random.choice(fail_strings) + ", you need an account to do that."
            
            if type == "cln":
                if clean_db():
                    message = random.choice(conf_strings) + ", the database is all cleaned up!"
                else:
                    message = random.choice(fail_strings) + ", I tried to clean up the database but failed."
            
            if type == "mor":
                if random.random() > 0.25:
                    message = random.choice(fail_strings) + ", I can't give you any more cookies right now."
                else:
                    newcookies = random.randint(1, 5)
                    account_change(screen_name, newcookies)
                    message = random.choice(conf_strings) + ", I'll give you " + str(newcookies) + " more cookies."
            
            if type == "hlp":
                message = random.choice(hi_strings) + "! Commands are: new, balance, send (bag), help, join, close, more please"
            
            tweet_to(screen_name, message, id)
            
            clean_db()
        return True
    
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream
    
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # same

def main():
    listener = StdOutListener()
    
    print "Listening for mentions"
    
    stream = Stream(auth, listener)
    stream.filter(track=['@cookietipbot', '#cookietip'])

if __name__ == '__main__':
    main()