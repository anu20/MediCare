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

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from MediCare import settings

import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob


GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["Hey would you like to schedule an appointment or schedule a lab test or buy medicines?"]

_url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'
_key = 'cafca9e336d2462bb03796513504f22d'
_maxNumRetries = 10 

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break
        
    return result


def getOCRTextResult( operationLocation, headers ):
    """
    Helper function to get text result from operation location

    Parameters:
    operationLocation: operationLocation to get text result, See API Documentation
    headers: Used to pass the key information
    """

    retries = 0
    result = None

    while True:
        response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break

    return result


def showResultOnImage( result, img ):
    
    """Display the obtained results onto the input image"""
    img = img[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(img, aspect='equal')

    lines = result['recognitionResult']['lines']

    for i in range(len(lines)):
        words = lines[i]['words']
        for j in range(len(words)):
            tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
            tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
            br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
            bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
            text = words[j]['text']
            x = [tl[0], tr[0], tr[0], br[0], br[0], bl[0], bl[0], tl[0]]
            y = [tl[1], tr[1], tr[1], br[1], br[1], bl[1], bl[1], tl[1]]
            line = Line2D(x, y, linewidth=3.5, color='red')
            ax.add_line(line)
            ax.text(tl[0], tl[1] - 2, '{:s}'.format(text),
            bbox=dict(facecolor='blue', alpha=0.5),
            fontsize=14, color='white')

    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.show()




def index(request,filename):
   pathToFileInDisk = filename
   with open(pathToFileInDisk, 'rb') as f:
      data = f.read()

   # Computer Vision parameters
   params = {'handwriting' : 'true'}

   headers = dict()
   headers['Ocp-Apim-Subscription-Key'] = _key
   headers['Content-Type'] = 'application/octet-stream'

   json = None

   operationLocation = processRequest(json, data, headers, params)

   result = None
   if (operationLocation != None):
     headers = {}
     headers['Ocp-Apim-Subscription-Key'] = _key
     while True:
        time.sleep(1)
        result = getOCRTextResult(operationLocation, headers)
        if result['status'] == 'Succeeded' or result['status'] == 'Failed':
            break

   # Load the original image, fetched from the URL
   if result is not None and result['status'] == 'Succeeded':
     data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
     img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
     showResultOnImage(result, img)
   
   return render(request, 'medicine/cover.html',{'filename':filename})




def prescription(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception, e:
        pass

    return render(request, 'medicine/cover.html',{'uploaded_picture':uploaded_picture})

@login_required
def upload_picture(request):
    try:
        prescription_images = '/home/anushka/MediCare/media/prescriptions/'
        if not os.path.exists(prescription_images):
            os.makedirs(prescription_images)
        f = request.FILES['picture']
        print f;
        filename = prescription_images + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/?upload_picture=uploaded')

    except Exception, e:
        print e
        return redirect('/')


@login_required
def save_uploaded_picture(request):
    tmp_filename=''
    try:
        prescription_images = '/home/anushka/MediCare/media/prescriptions/'
       
        tmp_filename = prescription_images + request.user.username + '_tmp.jpg'
        filename = prescription_images+ request.user.username + '.jpg'
        
        return _index(request,tmp_filename)
    except Exception, e:
        pass
   
    return index(request,tmp_filename)




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




def find_candidate_parts_of_speech(parsed):
    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
    pronoun = None
    noun = None
    adjective = None
    verb = None
    case1=False
    case2=False
    case3=False
    case4=False
    v=["need","wish","want","like","thinking","have",'looking']
    vnext=["buy","purchase","see","checkout","buying","book","reserve","schedule"]
    vrb=["help","provide","assist","tell","give","advice"]
    nn=["medicine","appointment","lab","test"]
    nn2=["book","schedule"]
    ans=None
    for sent in parsed.sentences:
        logger.info(sent)
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
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
    if case3 and case4:
       if job=="medicine" or job=="drug" or job=="product":
          ans="Sure, which "+job+" you would like?"
       elif job=="appointment":
          ans="Sure,on which date you like to schedule your appointment"
       elif job=="lab" or job=="test":
          ans="Sure,on which date you like to schedule your lab test"    
    return pronoun, noun, adjective, verb,ans


# end


def respond(request,sentence):
  
    prescription_images = '/home/anushka/MediCare/media/respond/'
    if not os.path.exists(prescription_images):
            os.makedirs(prescription_images)   

    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    pronoun, noun, adjective, verb ,ans= find_candidate_parts_of_speech(parsed)

    # If we said something about the bot and used some kind of direct noun, construct the
    # sentence around that, discarding the other candidates
    resp = check_for_greeting(parsed)
    if resp:
       ans=resp
    
    # Check that we're not going to say anything obviously offensive
    return JsonResponse(response_data, status=200)


def post(request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        """



        input_data = request.POST.get('message')
        prescription_images = '/home/anushka/MediCare/media/'+input_data+'/'
        if not os.path.exists(prescription_images):
            os.makedirs(prescription_images)

        response = respond(request,input_data)
        response_data = response.serialize()
        return JsonResponse(response_data, status=200)



