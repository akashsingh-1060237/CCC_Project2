# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:41:54 2020

@author: sudhe
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:02:37 2020

@author: sudhe
"""

import tweepy
import couchdb
from tweepy import StreamListener
from tweepy import Stream
import re
import time
import json
start_time=time.time()
access_token = "1251831797089886210-KawGdu5lvWNBTJpQE1sjjML3L2V9Nn"
access_token_secret ="tFhySpFIU23zzwGs85NGWNabCLA37kiwPb0oBYtUmWXke"
consumer_key = "3CwCe94hzHkFa2Ydd5Bp76Cxr"
consumer_secret = "uveX5gXCJgkZFqrUY0KZHlfovdN8O6305XaH4H03drUv4Qjk1l"
tweet_tracker=0#keeps track of tweets collected
tweet_cutoffs=80000#number of live tweets from australia to collect
interested_text=['covid19','coronavirus','covid-19','economy','employment','income','covid','pandemic','outbreak','social distancing','community spread','self-isolation','quarantine','selfquarantine','self-quarantine','flatten the curve','economycrisis','jobloss','wage','wageloss','socialdistancing','aid','financialaid','financial aid','governmentsupport','govtsupport','economic slowdown','economicslowdown','slowdown','unemployment','debt','inflation','house prices','gdp','deflation','relief','jobkeeper','job keeper','subsidy','wages','wage subsidy','centrelink','employer','employee','employed','jobseeker','package','stimulus package','stimulus','stocks','budget','rent','rental','speculation','reccession','tax','taxes','emi','bailout','work hours','pension','self-employed','working hours','minimum wage','unemployment benefits','tution fee','tutionfee','accommodation','housing','unemployed','lockdown','lock down']#the terms we are interestedin, all tweets with atleast one of these terms in the tweet text,hashtag text would be considered
user_ids=[]#list of user ids of tweets collected via streaming
tweet_ids=[]#list of ids of tweet ids which are relevant or to be more specific the tweets which contain atleast one of the above mentioned terms
relevant_tweet_tracker=0#keeps track of relevant tweets
non_relevant_tweet_tracker=0
#connecting to couchdb and creating a new database
couch=couchdb.Server('http://user:pass@localhost:5984')#connect to the server
db_name='final_tweet_harvester2'#database name that you would like to have
if couch.__contains__(db_name)==False:#if there is no existing database with same name then just the create the database
    db=couch.create(db_name)
else:#if there is a existing database use it
    db=couch[db_name]
class liveTweets(StreamListener):
    def on_data(self,data):
        global tweet_tracker
        global tweet_cutoffs
        global stream_object
        global user_ids
        global interested_text
        global tweet_ids
        global relevant_tweet_tracker
        global non_relevant_tweet_tracker
        while True:
            decoded_tweet=json.loads(data)#decode a tweet
            interested_tweet_text=''#it is total text from a tweet that would compared with the terms mentioned above
            current_id=''#tweet id of a tweet in string format so as to reduce memory consumption
            current_user_id=''#user id of a tweet
            current_country_name=''#country name from the tweet has been tweeted
            if decoded_tweet.get('retweeted_status','null')=='null' and decoded_tweet.get('quoted_status','null')=='null':#original tweet
                tweet_id=decoded_tweet.get('id_str','null')#tweet id in string representation
                total_text=''
                tweet_text=''
                if decoded_tweet.get('extended_tweet','null')!='null':#this tweet is an extended tweet when text of a tweet is much longer than 140 characters
                    extended_tweet=decoded_tweet.get('extended_tweet')
                    tweet_text=extended_tweet.get('full_text')#the text of a tweet
                    entity_info=extended_tweet.get('entities','null')#get entities information
                    hashtag_info=entity_info.get('hashtags','null')#it is a list of dictionary containing text and other details
                    if len(hashtag_info)>0:#if there is any information in the hashtag list then gather all text of the hashtags

                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext # separate the hashtag texts by comma
                    else:
                        pass
                else:#just normal tweeet with text upto 140 characters
                    tweet_text=decoded_tweet.get('text','null')#the text of the tweet
                    entity_info=decoded_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:#gather all hashtags text if there is any information related to the hashtag
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                place_info=decoded_tweet.get('place','null')
                country_name=''
                if isinstance(place_info,dict):
                    country_name=place_info.get('country','null')
                current_country_name=country_name
                user_info=decoded_tweet.get('user','null')
                user_id=user_info.get('id_str','null')
                current_id=tweet_id
                current_user_id=user_id
                interested_tweet_text=tweet_text+'  '+total_text#text of tweet and text gathered from hashtags separated by space
            if decoded_tweet.get('retweeted_status','null')!='null':#retweet
                tweet_text=''
                total_text=''
                if decoded_tweet.get('extended_tweet','null')!='null':#this retweet is an extended tweet
                    extended_tweet=decoded_tweet.get('extended_tweet')
                    tweet_text=extended_tweet.get('full_text')
                    entity_info=extended_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                else:
                    #retweet id ins string representation
                    original_info=decoded_tweet.get('retweeted_status')
                    tweet_text=original_info.get('text','null')
                    entity_info=original_info.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                orig_info=decoded_tweet.get('retweeted_status','null')#as retweet doesn't have place information so we take the original tweet place information
                place_info=orig_info.get('place','null')
                #place_info=tweet.get('place','null')
                country_name=''
                if isinstance(place_info,dict):
                    country_name=place_info.get('country','null')
                current_country_name=country_name
                retweet_id=decoded_tweet.get('id_str','null')
                user_info=decoded_tweet.get('user','null')
                user_id=user_info.get('id_str','null')
                current_id=retweet_id
                current_user_id=user_id
                interested_tweet_text=tweet_text+'  '+total_text
            if decoded_tweet.get('quoted_status','null')!='null':#quoted tweet
                #quoted tweet has some additional information along with
                tweet_text=''
                total_text=''
                if decoded_tweet.get('extended_tweet','null')!='null':#this  quoted tweet is an extended tweet
                    extended_tweet=decoded_tweet.get('extended_tweet')
                    tweet_text=extended_tweet.get('full_text')
                    entity_info=extended_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass

                else:

                    additional_text=decoded_tweet.get('text','null')
                    original_info=decoded_tweet.get('quoted_status','null')
                    original_text=original_info.get('text','null')
                    tweet_text=additional_text+' '+original_text
                    entity_info=decoded_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    org_entity_info=original_info.get('entities','null')
                    org_hashtag_info=org_entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+', '+htext
                    else:
                        pass
                    if len(org_hashtag_info)>0:
                        #total_text=''
                        for element in org_hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+', '+htext
                    else:
                        pass
                place_info=decoded_tweet.get('place','null')
                country_name=''
                if isinstance(place_info,dict):
                    country_name=place_info.get('country','null')
                current_country_name=country_name
                quoted_tweet_id=decoded_tweet.get('id_str','null')
                user_info=decoded_tweet.get('user','null')
                user_id=user_info.get('id_str','null')
                current_id=quoted_tweet_id
                current_user_id=user_id
                interested_tweet_text=tweet_text+' '+total_text
            matches=[]
            for term in interested_text:
                match_object=re.search(term,interested_tweet_text.lower())
                #if isinstance(match_object,re.Match):#if there is a match for the given term in the string then it is true else false
                    #matches.append('matched')
                if match_object is not None:
                    matches.append('matched')
            pat='australia'
            mat=re.search(pat,current_country_name.lower())
            res=False
            if mat is not None:
                res=True
            #res=isinstance(mat,re.Match)#if the country name is australia then it returns true else false
            if len(matches)>=1 and res:#atleaast the tweet contains one of the many interested terms then append that tweet id to the list
                if current_id not in db:#to avoid duplication
                    db[current_id]=decoded_tweet
                    tweet_ids.append(current_id)
                    relevant_tweet_tracker+=1
            if len(matches)==0 and res:#tweets which don't contain any text and tweet is from australia
                if current_id not in db:
                    db[current_id]=decoded_tweet
                    tweet_ids.append(current_id)
                    non_relevant_tweet_tracker+=1
            tweet_tracker+=1
            if current_user_id not in user_ids:#to avoid gathering tweets same user multiple times i.e storing unique user ids
                    user_ids.append(current_user_id)
            if tweet_tracker%300==0:
                print('streamed %r live tweets' % tweet_tracker)
                print('until now found %r interested tweets' % relevant_tweet_tracker)
                print('until now found %r not related tweets' % non_relevant_tweet_tracker)
            if tweet_tracker==tweet_cutoffs:
                print('so lets  go to user timeline method')
                break
            return True
        stream_object.disconnect()
    def on_error(self, status):
        print(status)
lobj=liveTweets()#stream listener instance
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,proxy='https://www.proxy.unimelb.edu.au:8000')#creating api object the last two parameters helps in automatically pushing the application to sleep for sometime incase rate limit is exceeded
stream_object=Stream(api.auth,lobj)
stream_object.filter(locations=[110.7,-45.4,155.7,-9.7])
print('done with streaming')
unq=len(set(tweet_ids))
print('number of tweets obtained through streaming are %r' % tweet_tracker)
print('out of all tweets gathered via streaming the  unique  tweets are %r' % unq)
print('out of all tweets gathered via streaming relevant tweets are %r' % relevant_tweet_tracker)
print('out of all tweets gathered via streaming non-relevant tweets are %r' % non_relevant_tweet_tracker)
user_timeline_counter=0#tracking number of tweets looked at by using the user timeline method
final_user_ids=[]#store user ids for upto  4 followers of each user whose tweeted was collected via streaming
print('total number of unique users considered for user timeline method are %r' % len(user_ids))
for id in user_ids:
    try:
        iterating_cursor=tweepy.Cursor(api.user_timeline,id).items(45)#recent 45 tweets
        for element in iterating_cursor:
            user_timeline_counter+=1
            tweet=element._json#tweet data
            interested_tweet_text=''
            current_id=''#tweet id
            current_country_name=''
            if tweet.get('retweeted_status','null')=='null' and tweet.get('quoted_status','null')=='null':
                tweet_text=''
                total_text=''
                if tweet.get('extended_tweet','null')!='null':#this tweet is an extended tweet
                    extended_tweet=tweet.get('extended_tweet')
                    tweet_text=extended_tweet.get('full_text')
                    entity_info=extended_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                else:
                    tweet_text=tweet.get('text','null')
                    entity_info=tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                place_info=tweet.get('place','null')
                country_name=''
                if isinstance(place_info,dict):
                    country_name=place_info.get('country','null')
                current_country_name=country_name
                current_id=tweet.get('id_str','null')
                interested_tweet_text=tweet_text+' '+total_text

            if tweet.get('retweeted_status','null')!='null':
                tweet_text=''
                total_text=''
                retweeted_id=tweet.get('id_str','null')
                if tweet.get('extended_tweet','null')!='null':#this tweet is an extended tweet
                    extended_tweet=tweet.get('extended_tweet')
                    tweet_text=extended_tweet.get('full_text')
                    entity_info=extended_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                else:
                    original_info=tweet.get('retweeted_status','null')
                    tweet_text=original_info.get('text','null')
                    entity_info=tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                orig_info=tweet.get('retweeted_status','null')
                place_info=orig_info.get('place','null')
                country_name=''
                if isinstance(place_info,dict):
                    country_name=place_info.get('country','null')
                current_country_name=country_name
                current_id=retweeted_id
                interested_tweet_text=tweet_text+' '+total_text
            if tweet.get('quoted_status','null')!='null':
                tweet_text=''
                total_text=''
                quoted_tweet_id=tweet.get('id_str','null')
                if tweet.get('extended_tweet','null')!='null':#this tweet is an extended tweet
                    extended_tweet=tweet.get('extended_tweet')
                    tweet_text=extended_tweet.get('full_text')
                    entity_info=extended_tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                else:
                    original_info=tweet.get('quoted_status','null')
                    additional_text=tweet.get('text','null')
                    original_text=original_info.get('text','null')
                    tweet_text=additional_text+' '+original_text
                    entity_info=tweet.get('entities','null')
                    hashtag_info=entity_info.get('hashtags','null')
                    org_entity_info=original_info.get('entities','null')
                    org_hashtag_info=org_entity_info.get('hashtags','null')
                    if len(hashtag_info)>0:
                        #total_text=''
                        for element in hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                    if len(org_hashtag_info)>0:
                        #total_text=''
                        for element in org_hashtag_info:
                            htext=element.get('text','null')
                            total_text=total_text+','+htext
                    else:
                        pass
                place_info=tweet.get('place','null')
                country_name=''
                if isinstance(place_info,dict):
                    country_name=place_info.get('country','null')
                current_country_name=country_name
                current_id=quoted_tweet_id
                interested_tweet_text=tweet_text+' '+total_text
            matches=[]
            for term in interested_text:
                match_object=re.search(term,interested_tweet_text.lower())
                #if isinstance(match_object,re.Match):#if there is a match for the given term in the string then it is true else false
                    #matches.append('matched')
                if match_object is not None:
                    matches.append('matched')
            pat='australia'
            mat=re.search(pat,current_country_name.lower())
            res=False
            if mat is not None:
                res=True
            #res=isinstance(mat,re.Match)
            if len(matches)>=1 and res:#atleaast the tweet contains one of the many interested terms then append that tweet id to the list
                if current_id not in db:
                    db[current_id]=tweet
                    relevant_tweet_tracker+=1
                    tweet_ids.append(current_id)
            if len(matches)==0 and res:
                if current_id not in db:
                    db[current_id]=tweet
                    non_relevant_tweet_tracker+=1
                    tweet_ids.append(current_id)
                #user_ids.append(current_user_id)
            if user_timeline_counter%1000==0:
                print('number of tweets obtained through user timeline method  until now are %r ' % user_timeline_counter)
                print('until now  number of interested tweets found are %r ' % relevant_tweet_tracker)
                print('until now  number of not-topic related  tweets found are %r ' % non_relevant_tweet_tracker)

    except tweepy.TweepError:#if we don't have access then execute this
        print('some error has occurred')
print('total number of tweets looked at are %r' % (tweet_cutoffs+user_timeline_counter))
print('total number of tweets both relevant and non-relevant are %r' % len(tweet_ids))
print('number of  unique tweets obtained by streaming  and  user timeline methods with or with out interested terms  are %r ' % len(set(tweet_ids)))
print('topic related tweets from streaming and user timeline methods are %r' % relevant_tweet_tracker)
print('australia tweets but not related to topic from streaming and user timeline methods are %r' % non_relevant_tweet_tracker)
endtime=time.time()
#print(endtime-start_time)
print('total time taken to execute this code is %r seconds' % (endtime-start_time))
#print('total time taken to execute the above logic is %r minutes' % (endtime-start_time)/60)
