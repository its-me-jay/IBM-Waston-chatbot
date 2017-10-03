from __future__ import division
import json
import watson_developer_cloud
import pprint
import numpy as np
import random, string
import sqlite3 as lite
import sys
import os
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    username='c31fff66-9103-443d-949e-55f8f30c8f41',
    password='5Z0mEIPUze4u',
    version='2016-05-19')

conversation = watson_developer_cloud.ConversationV1(
username='0edb3d15-278c-4a64-b8f9-e739979cd896',
password='qSw7ZR8Oap4G',
version='2017-04-21'
)
workspace_id = '682d4548-5f07-4fd3-b5c1-f31b50eb4d88'

def sendmessage(text):
    context = {}
    response = conversation.message(
      workspace_id = workspace_id,
      message_input = {'text': text},
      context = context
    )
    received = response['output']['text'][-1]
    parsed_response=json.dumps(response, indent=2)
    intent=response['intents'][0]
    intent=intent['intent']
    #print parsed_response
    entities=response["entities"]
    #print "------"

    if(intent=="number"):
        size=len(entities)
        entity_values=[]
        entity_names=[]
        for i in range(size):
            entity_values.append(entities[i]['value'])
            entity_names.append(entities[i]['entity'])
        #print entity_names
        #print "-------"
        #print entity_values
        #print "------"
        #print "size is %d" %size

        if("client" in entity_names) and ("status" in entity_names) and ("severity_value" in entity_names):
            #print "yefygefygefu"
            count3(entity_values[list.index(entity_names,"client")],entity_values[list.index(entity_names,"severity_value")],entity_values[list.index(entity_names,"status")])
        elif("client" in entity_names) and ("status" in entity_names):
            count(entity_values[list.index(entity_names,"client")],entity_values[list.index(entity_names,"status")])
        elif("client" in entity_names) and ("severity_value" in entity_names):
            count1(entity_values[list.index(entity_names,"client")],entity_values[list.index(entity_names,"severity")])


    #if(intent=="list"):

    if(intent=="average"):
        size=len(entities)
        entity_values=[]
        entity_names=[]
        for i in range(size):
            entity_values.append(entities[i]['value'])
            entity_names.append(entities[i]['entity'])

        if("client" in entity_names):
            average_time_client(entity_values[list.index(entity_names,"client")])

        if("Product" in entity_names):
            average_time_product(entity_values[list.index(entity_names,"Product")])

    if(intent=="status"):
        size=len(entities)
        entity_values=[]
        entity_names=[]
        for i in range(size):
            entity_values.append(entities[i]['value'])
            entity_names.append(entities[i]['entity'])
        stat_from_ticket(entity_values[list.index(entity_names,"ticket")])


    if(intent=="bye"):
        print "Watson: %s" %received

    if(intent=="tone"):
        size=len(entities)
        entity_values=[]
        entity_names=[]
        for i in range(size):
            entity_values.append(entities[i]['value'])
            entity_names.append(entities[i]['entity'])

        if("ticket" in entity_names):
            ticket_tone(entity_values[list.index(entity_names,"ticket")])
        if("client" in entity_names):
            client_tone(entity_values[list.index(entity_names,"client")])
        if("Product" in entity_names):
            product_tone(entity_values[list.index(entity_names,"Product")])



    if(intent=="greet"):
        print "Watson: %s" %received

    userinput()

def userinput():
    text=raw_input("You: ")
    sendmessage(text)


def count3(upda,severity,status):

   con = lite.connect('test_final.db')
   a= "SELECT * FROM Contacts WHERE client = " + "'" + upda + "'"
   #cursor = con.execute("SELECT * FROM Contacts WHERE client = 'PAT Ltd' ")
   cursor=con.execute(a)
   b = 0
   for row in cursor:
       #print row[4]
       #print row[1]
       if (str(row[4]) == str(severity)) and (str(row[1]) == str(status)):
           b = b + 1
   print "Watson: %d" %b


def count1(upda,severity):

   con = lite.connect('test_final.db')
   a= "SELECT * FROM Contacts WHERE client = " + "'" + upda + "'"
   #cursor = con.execute("SELECT * FROM Contacts WHERE client = 'PAT Ltd' ")
   cursor=con.execute(a)
   a = 0
   for row in cursor:
       if row[4] == severity :
         a = a + 1
   print "Watson: %d" %a
   con.close()

def average_time_product(product):

     con = lite.connect('test_final.db')
     a= "SELECT * FROM Contacts WHERE Product = " + "'" + product + "'"
     #cursor = con.execute("SELECT * FROM Contacts WHERE client = 'PAT Ltd' ")
     cursor=con.execute(a)
     a = 0
     i=0
     for row in cursor:
         if row[3] == product :
           a = a + row[9]
           i=i+1

     print "Watson: Average time is %s seconds" %(a/i)
     con.close()

def average_time_client(client):

     con = lite.connect('test_final.db')
     a= "SELECT * FROM Contacts WHERE client = " + "'" + client + "'"
     #cursor = con.execute("SELECT * FROM Contacts WHERE client = 'PAT Ltd' ")
     cursor=con.execute(a)
     a = 0
     i=0
     for row in cursor:
         if row[2] == client :
           a = a + row[9]
           i=i+1

     print "Watson: Average time is %f seconds" %(a/i)
     con.close()


def stat_from_ticket(ticket):

   con = lite.connect('test_final.db')
   a= "SELECT * FROM Contacts WHERE Ticket_no = " + "'" + ticket + "'"
   #cursor = con.execute("SELECT * FROM Contacts WHERE client = 'PAT Ltd' ")
   cursor=con.execute(a)
   a = 0
   for row in cursor:
       if str(row[0]) == str(ticket):
           status=row[1]
           break
   print "Watson: %s" % status
   con.close()

def count(upda,status):

   con = lite.connect('test_final.db')
   a= "SELECT * FROM Contacts WHERE client = " + "'" + upda + "'"
   #cursor = con.execute("SELECT * FROM Contacts WHERE client = 'PAT Ltd' ")
   cursor=con.execute(a)
   count = 0
   for row in cursor:
       if row[1] == status :
         count = count + 1
   print "Watson: %d" % count
   con.close()

def ticket_tone(ticket):

   #print upda , severity

   con = lite.connect('test_final.db')
   a= "SELECT * FROM Contacts WHERE Ticket_no = " + "'" + ticket + "'"
   cursor=con.execute(a)

   a = 0
   x=[]
   for row in cursor:
       #print row[4]
       a = row[11]
       utterances = [{'text': a, 'user': 'glenn'}]
       j=tone_analyzer.tone_chat(utterances)
       #print j
       z=j["utterances_tone"][0]["tones"][0]["tone_name"]
       if z == 'frustated':
          x.append('negative')
       if z == 'sad':
          x.append('negative')
       if z == 'sympathetic':
          x.append('neutral')
       if z == 'excited':
          x.append('positive')
       if z == 'polite':
          x.append('neutral')
       if z == 'satisfied':
          x.append('positive')
   print x


def product_tone(product):

   #print upda , severity

   con = lite.connect('test_final.db')
   a= "SELECT * FROM Contacts WHERE Product = " + "'" + product + "'"
   cursor=con.execute(a)

   a = 0
   x = []
   for row in cursor:
       #print row[4]
       a =row[11]
       utterances = [{'text': a, 'user': 'glenn'}]
       j=tone_analyzer.tone_chat(utterances)
       #print j
       z = j["utterances_tone"][0]["tones"][0]["tone_name"]
       #print z
       if z == 'frustated':
          x.append('negative')
       if z == 'sad':
          x.append('negative')
       if z == 'sympathetic':
          x.append('neutral')
       if z == 'excited':
          x.append('positive')
       if z == 'polite':
          x.append('neutral')
       if z == 'satisfied':
           x.append('positive')
       print x

def client_tone(client):
    #print upda , severity

    con = lite.connect('test_final.db')
    a= "SELECT * FROM Contacts WHERE client = " + "'" + client + "'"
    cursor=con.execute(a)
    a = 0
    x = []
    for row in cursor:
        #print row[4]
        a =row[11]
        utterances = [{'text': a, 'user': 'glenn'}]
        j=tone_analyzer.tone_chat(utterances)
        #print j
        z = j["utterances_tone"][0]["tones"][0]["tone_name"]
        #print z
        if z == 'frustated':
           x.append('negative')
        if z == 'sad':
           x.append('negative')
        if z == 'sympathetic':
           x.append('neutral')
        if z == 'excited':
           x.append('positive')
        if z == 'polite':
           x.append('neutral')
        if z == 'satisfied':
           x.append('positive')
        print x



userinput()
