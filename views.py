from django.shortcuts import render
import requests,math,datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytz import timezone
from .models import openUVData, WilyWeatherData

##
#Helper function to make calls to the Open UV API.
#There are 2 situations where a call might need to be made
#If no entry exists, or if the most recent entry is too old
#Using this function keeps the code tidy and reduces repetition

def openUVgetter():

    lat = "-27.64";
    lng = "153.12";
    alt = "24";
    headers={'x-access-token':'1827407a260b51ff5b11161aac9c7f5d'}
    url='https://api.openuv.io/api/v1/uv?lat=' + lat + '&lng=' + lng + '&alt=' + alt
    try:
        response = requests.get(url,headers=headers)
        UVou=response.json()['result']['uv']
        time=response.json()['result']['uv_time']
        uv_info = openUVData(uv_date=time,uv=UVou)
        uv_info.save()

    except:
        UVou = -1
        
    finally:
        return UVou
##
#Helper function to make calls to scrape wilyweather
#There are 2 situations where a call might need to be made
#If no entry exists, or if the most recent entry is too old
#Using this function keeps the code tidy and reduces repetition
def WWgetter():
    
    now = datetime.datetime.now()
    now = now.astimezone(timezone('Australia/Brisbane'))
    try:
        url = 'https://uv.willyweather.com.au/qld/brisbane/slacks-creek.html'
        driver = webdriver.PhantomJS(executable_path='C:/Users/Locke/AppData/Roaming/npm/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
        driver.get(url)
        element = driver.find_elements(By.CLASS_NAME, "real-time")
        UVww =element[0].text.split()[0]
        uv_info = WilyWeatherData(uv_date=now,uv=UVww)
        uv_info.save()
        driver.quit()
    except:
        UVww=-1
    finally:
        return UVww
            
    
##
#Code for the UV display page
def index(request):
    #Get the current time in AEST
    now = datetime.datetime.now()
    now = now.astimezone(timezone('Australia/Brisbane'))

    #openuv - makes a call to the Open UV API

    #If there are no entries in the database
    if ((openUVData.objects.exists()==False)):
        #Make call to API
        UVou = openUVgetter();
        outime=now
    else:
        #Prepare the data for display
        reading = openUVData.objects.last()
        UVou=reading.uv
        outime=reading.uv_date
        outime=outime.astimezone(timezone('Australia/Brisbane'))     
        #If the data is older than aprox 17 minutes, get new data
        #17 minutes because the free API allows 50 calls per day, so on the summer solstice
        #(Longest day), 50 calls equates to one every 17.3ish minutes between sunrise and sunset
        if ((now.timestamp()-outime.timestamp())>1020):
            UVou = openUVgetter(); 


    #wily weather - scrapes the website after javascript populates it to get hourly UV updates
    #makes site slightly more accurate
    #Can only get data once per hour, at at any time during that hour
    if (WilyWeatherData.objects.exists()==False):
        UVww=WWgetter()
        wwtime=now
    else:
        reading = WilyWeatherData.objects.last()
        UVww=reading.uv
        wwtime=reading.uv_date
        wwtime=wwtime.astimezone(timezone('Australia/Brisbane'))
        if (not((wwtime.day==now.day)&(wwtime.hour==now.hour))):
            UVww=WWgetter()

    #Choose the most recent of the 2 to display   
    if(wwtime.timestamp()>outime.timestamp()):
        uv=UVww
    else:
        uv=UVou

    context={'uv':uv}  
    return render(request,'rasppi/index.html',context)
