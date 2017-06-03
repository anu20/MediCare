import os
import logging
import httplib2
import argparse
import base64
import markdown
import time 
import requests
import cv2
import operator
import json
import numpy as np

from django.http import JsonResponse
# Import library to display results
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Display images within Jupyter
from PIL import Image

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings as django_settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from MediCare import settings
from MediCare.products.models import ProdCategory,Product
from MediCare.carts.models import Cart,CartItem
from MediCare.labs.models import Lab,Category
from MediCare.chat.models import Message
import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob


GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["Hey would you like to schedule an appointment or schedule a lab test or buy medicines?"]

GREETING=("okay","thank you","welcome","sure")
RESPONSE=["would you like to do something else?"]

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)
    for word in sentence.words:
        if word.lower() in GREETING:
            return random.choice(RESPONSE)


def find_pronoun(sent):
    """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
    pronoun is found in the input"""
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # Disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            pronoun = 'You'
    return pronoun
# end

def find_verb(sent):
    """Pick a candidate verb for the sentence."""
    verb = []
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):  # This is a verb
            verb.append(word)
            pos = part_of_speech
    return verb, pos


def find_noun(sent):
    """Given a sentence, find the best candidate noun."""
    noun = []

    if not noun:
        for w, p in sent.pos_tags:
            if p.startswith('NN'):  # This is a noun
                noun.append(w)
   
    return noun

def find_adjective(sent):
    """Given a sentence, find the best candidate adjective."""
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':  # This is an adjective
            adj = w
            break
    return adj

mon=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def find_date(sent):
    num=""
    flag=0
    for w in sent.split():
      if w.isdigit():
         num=num+" "+w
      elif w in mon:
         num=num+" "+w 
         flag=1
    if flag==1: 
       return num
    else:
       return '-1'
def find_job(request):
  messages = Message.objects.filter(
            user=request.user).order_by('-id')[0]
  return messages.message

def preprocess_text(sentence):
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)


job=""
def find_candidate_parts_of_speech(request,parsed):
    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
    pronoun = None
    noun = None
    adjective = None
    verb = None
    date=None
    month=None
    case1=False
    case2=False
    case3=False
    case4=False
    case5=False
    case0=False
    global job
    v=["need","wish","want","like","thinking","have",'looking']
    vnext=["buy","purchase","see","checkout","buying","book","reserve","schedule"]
    vrb=["help","provide","assist","tell","give","advice"]
    nn=["medicine","appointment","lab","test","medicines","products"]
    nn2=["book","schedule"]
    ans=None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
        date=find_date(sent)
    cat=""
       
    if case0:
       ans="Sure"
    
    case7=False
    #to find verb
    if pronoun=="You":
      for vr in verb[0]:
        if vr in v:
          case1=True
          break
    elif pronoun=="I":
      for vr in verb[0]:
        if vr in vrb:
          case2=True
          break
    for vr in verb[0]:
      if vr in vnext:
         case3=True
         break
    for n in noun:
      if n in nn2:
         case3=True
         ans="noun"
         break
    for n1 in noun:
      if n1 in nn:
         case4=True
         job=n1
         break
    if case3:
       for n in noun:
         category=Category.objects.filter(title=n)
         if category:
            case7=True
            cat=n
            ans1=Lab.objects.filter(category=category)
            ans="You can have following lab for "+n+": "
            for p in ans1:
                ans+=p.title+" "
            break
                  
    if case7:
       return pronoun, noun, adjective, verb,ans

    for n in noun:
        category = ProdCategory.objects.filter(title=n)
        if category:
           case0=True
           cat=n
           ans1=Product.objects.filter(category=category)
           ans="You can have following medicines for "+n+" : "
           for p in ans1:
               ans+=p.title+" "
           break

           
    if not case0:
      for n in noun:
        prod=Product.objects.filter(slug=n)
        if prod:
           case0=True
           try:
		the_id = request.session['cart_id']
	   except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	   product=Product.objects.get(slug=n)
	   cart = Cart.objects.get(id=the_id)
           cart_item = CartItem.objects.create(cart=cart, product=product)
           cart_item.quantity = 1
	   cart_item.save()

           ans=n+" has been added to your cart"
           break
    if case0:
       return pronoun, noun, adjective, verb,ans
    if date=='-1':
       case5=False
    else:
       case5=True
    
    
    if job:
     if case5==True and (job=="appointment" or job=="lab" or job=="test"):
       ans="Your "+job+" has been scheduled for "+date
     elif case1 or case2 or case3 and case4:
       if job=="medicine" or job=="drug" or job=="product" or job=="medicines" or job=="products":
          ans="Sure, which "+job+" you would like?"
       elif job=="appointment":
          ans="Sure,on which date you like to schedule your appointment"
       elif job=="lab" or job=="test":
          ans="Sure, which lab test you want to schedule"    

    return pronoun, noun, adjective, verb,ans

# end


def respond(request,sentence):
  
    prescription_images = '/home/anushka/MediCare/media/respond/'
    if not os.path.exists(prescription_images):
            os.makedirs(prescription_images)   

    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    pronoun, noun, adjective, verb ,ans= find_candidate_parts_of_speech(request,parsed)

    # If we said something about the bot and used some kind of direct noun, construct the
    # sentence around that, discarding the other candidates
    resp = check_for_greeting(parsed)
    if resp:
       ans=resp
    
    # Check that we're not going to say anything obviously offensive
    return ans

@login_required
def messages(request):
    messages = Message.objects.filter(user=request.user)

    return render(request, 'messenger/inbox.html', {
        'messages': messages
        })




@login_required
def receive(request):
    if request.method == 'POST':
        from_user = request.user
        message = request.POST.get('message')

        Message.receive_message(from_user, message)
        if not job:
          last_msg=find_job(request)
          last_job=respond(request,last_msg)
        msg=respond(request,message)
        Message.send_message(from_user,msg)
        messages = Message.objects.filter(user=request.user)

        return render(request, 'medicine/cover.html', {
            'messages': messages
            })


    else:
        messages = Message.objects.filter(user=request.user)
        return render(request, 'medicine/cover.html', {
            'messages': messages
            })







