#!c:/Python32/python.exe
'''
Created on May 05, 2014
@description: checks whether a course is open or not and then message and call me!
@author: Poojan Khanpara

@notes:
Create Twilio developer account.
Change the phone_no to your phone number.
Change the account_sid to your Twilio account_sid
Change the auth_token to your Twilio auth_token
Change the twilioPhoneNumber to the Twilio number provided to you by Twilio
Right now it checks for Summer courses of graduate level in 2014 in Computer Science Department,
changing the url changes that.

And please use it judiciously, don't kill our UTD servers and I'll not be liable for anything you do with this script.
'''
import requests
import datetime
import time
import sys
from twilio.rest import TwilioRestClient
from bs4 import BeautifulSoup

#mycourses = ['CS 6364.0U1']
myprofessor = ['Haim']
#Your phone number where you want your sms and call
phone_no = '+1469XXX1234'
# Your Twilio account_sid
account_sid = "AX1a7d1XXXXXXXXXXXXXXXXXXXXXXXXX"
#Your Twilio auth_token
auth_token  = "4X4c965XXXXXXXXXXXXXXXXXXXXXXXXX"
#Your Twilio phone number
twilioPhoneNumber="+18152463XXX"

#Edit the below part with caution.. you have been warned!

# checks for mycourse to be in courses and if its open msgs me and calls me.
def CheckAndSMS(courses):
    client = TwilioRestClient(account_sid, auth_token)     
    for course in courses:
        for myc in myprofessor:
            if(myc in course[2]):
                if('Open' in course[1]):
                    temp = '\n'+course[0]+'\n'+ course[1]+'\n'+course[2]+'\n'+ course[3]+'\n'+course[4]+'\n'+course[5]
                    client.messages.create(to=phone_no, from_=twilioPhoneNumber, body=temp, )
                    client.calls.create(to = phone_no, from_=twilioPhoneNumber, url="http://twimlets.com/message?Message%5B0%5D=Jarvis%20has%20sent%20you%20a%20message&")
                    print('open::###-------------->>'+temp)

# Parses the given tr tag and removes the imp content and returns a list of course
def parseCourse(row):
    i = 0
    course = ["", "","", "", "", ""]
    for td in row.find_all("td"):
        i = i + 1
        if(i==1):
            #status of class
            status = td.br.span.string
        elif(i==2):
            #section number and class number
            section = td.a.string+" "+str(td)[-10:-5]
        elif(i==3):
            #course name
            name = td.string
        elif(i==4):
            #professor name
            try:
                prof=''
                prof = td.a.string
            except AttributeError as a:
                pass #do nothing
        elif(i==5):
            #time
            time = str(td)[4:36]
        elif(i==6):
            #filled%
            filled = td.div["title"]
            course = [name, status, prof, section, filled, time ]
    #print(course)
    return course

if __name__ == '__main__':
    pass
ptgsessid = ''
cookies = {'__utma':'25620399.1333872118.1399675652.1399675652.1399675652.1','__utmz':'25620399.1399675652.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','PTGSESSID':ptgsessid,'__utmb':'25620399.1.10.1399675652','__utmc':'25620399'}
headers = {
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
                "Accept-Language" : "en-us,en;q=0.5",
                "Accept-Charset" : "ISO-8859-1",
                "Content-type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "Host" : "coursebook.utdallas.edu",
                "Referer" : 'http://coursebook.utdallas.edu/'
                }
url = 'http://coursebook.utdallas.edu/clips/clip-searchresults.zog?s=term_14u%20cp_cs%20clevel_g'

while 1:       
    try:
        r = requests.get(url, headers = headers, cookies = cookies,verify=False)
        html = r.text
        if('please refresh your browser screen' in html):
            print('cookie expired at ',datetime.datetime.now())
            # Renewing cookie
            url4c = 'http://coursebook.utdallas.edu/'
            cookie4c = {'__utma':'25620399.1333872118.1399675652.1399675652.1399675652.1','__utmz':'25620399.1399675652.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','__utmb':'25620399.1.10.1399675652'}
            header4c = {
                "Host" : "coursebook.utdallas.edu",
                       "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
                "Accept-Language" : "en-us,en;q=0.5",
                "Accept-Charset" : "ISO-8859-1",
                "Connection": "keep-alive"
                }
            r4c = requests.get(url4c, headers = header4c, cookies = cookie4c,verify=False)
            html = r4c.text
            ptgsessid = str(r4c.headers['Set-Cookie'])[10:36]
            # requesting new page
            cookies = {'__utma':'25620399.1333872118.1399675652.1399675652.1399675652.1','__utmz':'25620399.1399675652.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','PTGSESSID':ptgsessid,'__utmb':'25620399.1.10.1399675652','__utmc':'25620399'}
            r = requests.get(url, headers = headers, cookies = cookies,verify=False)
            html = r.text
            print('new cookie set on:', str(datetime.datetime.now()))

        #print(html)
        soup= BeautifulSoup(html)
        courses = []
        for row in soup.find_all("tr"):
            courses.append(parseCourse(row))
        CheckAndSMS(courses)
        print('Checked '+str(len(courses))+' courses at: ',str(datetime.datetime.now()))
        time.sleep(60*60*2)

    except KeyboardInterrupt as ke:
        print ('Program exited as per user request...',ke)
        sys.exit(0)
