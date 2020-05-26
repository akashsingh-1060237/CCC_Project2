# -*- coding: utf-8 -*-
"""
Created on Tue May 26 23:52:17 2020

@author: sudhe
"""
import requests
payload= {
  "id": "_design/final",
  "views": {
   "economy": {
    "reduce": "_count",
    "map": "function (doc) {\n  var tweetext=doc.text\n  var corterms=['economy','economycrisis','aid','financialaid','financial aid','governmentsupport','govtsupport','economic slowdown','economicslowdown','slowdown','debt','inflation','house prices','gdp','deflation','relief','package','stimulus package','stimulus','stocks','budget','recession','tax','emi','bailout']\n  var ltweetext=tweetext.toLowerCase()\n  var results=corterms.map(checkterm)\n  function checkterm(value,index,array){\n    var r = ltweetext.search(value)\n    return r\n  }\n  var reslength=results.length\n  for(i=0;i<reslength;i++){\n    if (results[i]!=-1){\n      emit({'term':'economy','location':doc.place.name},1);\n      break\n       }\n      \n    }\n  }\n  \n  \n  \n\n  \n  \n  \n  \n  \n"
   },
   "corona": {
    "reduce": "_count",
    "map": "function (doc) {\n  var tweetext=doc.text\n  var corterms=['covid19','coronavirus','covid-19','covid','pandemic','outbreak','socialdistancing','social distancing','community spread','self-isolation','quarantine','selfquarantine','self-quarantine','flatten the curve','lockdown','lock down']\n  var ltweetext=tweetext.toLowerCase()\n  var results=corterms.map(checkterm)\n  function checkterm(value,index,array){\n    var r = ltweetext.search(value)\n    return r\n  }\n  reslength=results.length\n  for(i=0;i<reslength;i++){\n    if (results[i]!=-1){\n      emit({'term':'covid','location':doc.place.name},1);\n      break\n    }\n  }\n  \n  }\n  \n"
   },
   "employment": {
    "reduce": "_count",
    "map": "function (doc) {\n  var tweetext=doc.text\n  var corterms=['employment','income','unemployment','jobloss','wage','wageloss','jobkeeper','job keeper','subsidy','wages','wage subsidy','centrelink','employer','employee','jobseeker','employed','rent','rental','work hours','pension','self-employed','working hours','minimum wage','unemployment benefits','housing','unemployed']\n  var ltweetext=tweetext.toLowerCase()\n  var results=corterms.map(checkterm)\n  function checkterm(value,index,array){\n    var r = ltweetext.search(value)\n    return r\n  }\n  reslength=results.length\n  for(i=0;i<reslength;i++){\n    if (results[i]!=-1){\n      emit({'term':'employment','location':doc.place.name},1);\n      break\n    }\n  }\n  \n  }\n  \n"
   },
   "location": {
    "reduce": "_count",
    "map": "function (doc) {\n  emit({'location name':doc.place.name,'location coordinates':doc.place.bounding_box.coordinates}, 1);\n}"
   },
   "hashtag_covid": {
    "reduce": "_count",
    "map": "function (doc) {\n  var hashtaginfo=doc.entities.hashtags\n  var hashtaglength=hashtaginfo.length\n  var hasht=[]\n  var covidterms=['covid19','coronavirus','covid-19','covid','pandemic','outbreak','socialdistancing','social distancing','community spread','self-isolation','quarantine','selfquarantine','self-quarantine','flatten the curve','lockdown','lock down']\n  if (hashtaglength>0){\n    for(i=0;i<hashtaglength;i++){\n      var hashtagtext=hashtaginfo[i].text\n      var lhashtagtext=hashtagtext.toLowerCase()\n      hasht.push(lhashtagtext)\n    }\n    \n  }\n  var hatext=hasht.join(',')\n  var covidhashresults=covidterms.map(checkhashtagcovid)\n  function checkhashtagcovid(value,index,array){\n    re=hatext.search(value)\n    return re\n  }\n  var covidhashlen=covidhashresults.length\n  if (covidhashlen>0){\n    for(i=0;i<covidhashlen;i++){\n      if (covidhashresults[i]!=-1){\n     emit({'term':'covid','location':doc.place.name}, 1);\n     break\n    }\n    \n  }\n  \n  }\n \n}"
   },
   "hashtag_economy": {
    "reduce": "_count",
    "map": "function (doc) {\n  var hashtaginfo=doc.entities.hashtags\n  var hashtaglength=hashtaginfo.length\n  var hasht=[]\n  var ecoterms=['economy','economycrisis','aid','financialaid','financial aid','governmentsupport','govtsupport','economic slowdown','economicslowdown','slowdown','debt','inflation','house prices','gdp','deflation','relief','package','stimulus package','stimulus','stocks','budget','recession','tax','emi','bailout']\n  if (hashtaglength>0){\n    for(i=0;i<hashtaglength;i++){\n      var hashtagtext=hashtaginfo[i].text\n      var lhashtagtext=hashtagtext.toLowerCase()\n      hasht.push(lhashtagtext)\n    }\n    \n  }\n  var hatext=hasht.join(',')\n  var ecohashresults=ecoterms.map(checkhashtageco)\n  function checkhashtageco(value,index,array){\n    re=hatext.search(value)\n    return re\n  }\n  var ecohashlen=ecohashresults.length\n  if (ecohashlen>0){\n    for(i=0;i<ecohashlen;i++){\n      if (ecohashresults[i]!=-1){\n     emit({'term':'economy','location':doc.place.name}, 1);\n     break\n    }\n    \n  }\n  \n  }\n\n \n}"
   },
   "hashtag_employment": {
    "reduce": "_count",
    "map": "function (doc) {\n  var hashtaginfo=doc.entities.hashtags\n  var hashtaglength=hashtaginfo.length\n  var hasht=[]\n  var employterms=['employment','income','unemployment','jobloss','wage','wageloss','jobkeeper','job keeper','subsidy','wages','wage subsidy','centrelink','employer','employee','jobseeker','employed','rent','rental','work hours','pension','self-employed','working hours','minimum wage','unemployment benefits','housing','unemployed']\n  if (hashtaglength>0){\n    for(i=0;i<hashtaglength;i++){\n      var hashtagtext=hashtaginfo[i].text\n      var lhashtagtext=hashtagtext.toLowerCase()\n      hasht.push(lhashtagtext)\n    }\n    \n  }\n  var hatext=hasht.join(',')\n  var employhashresults=employterms.map(checkhashtagemploy)\n   function checkhashtagemploy(value,index,array){\n    re=hatext.search(value)\n    return re\n  }\n  var emphashlen=employhashresults.length\n  if (emphashlen>0){\n    for(i=0;i<emphashlen;i++){\n      if (employhashresults[i]!=-1){\n     emit({'term':'employment','location':doc.place.name}, 1);\n     break\n    }\n    \n  }\n  \n  }\n \n}"
   },
   "precise": {
    "reduce": "_count",
    "map": "function (doc) {\n  var g=doc.geo\n  if (g!='null'){\n     emit({'location name':doc.place.name,'location coordinates':doc.geo.coordinates}, 1);\n  }\n \n}"
   }
  },
  "language": "javascript"
 }
hes = {"content-type": "application/json" }
#url=http://username:passwordipaddress/databasename/_design/designdocumentname
ur='http://user:pass@172.26.129.249:5984/final_tweet_harvester2/_design/final'
resty=requests.put(ur,json=payload,headers=hes)
str_result=str(resty)
inter_res=str_result[1:-1]
if inter_res=='Response [201]':#if it is true then  it means that the document have been succesfully insterted.
    print('success....!')
    print('design document created')
else:
    print(resty)