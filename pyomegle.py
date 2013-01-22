import urllib2 as url
import urllib
import httplib as http
import sys
from threading import Thread
import time

t=None
def fmtId( string ):
    return string[1:len( string ) - 1]

def talk(id,req,text=''):
    typing = url.urlopen('http://omegle.com/typing', '&id='+id)
    typing.close()
    if text=='':
        msg = str(raw_input('> '))
    else:
        msg=text

    msgReq = url.urlopen('http://omegle.com/send', '&msg='+msg+'&id='+id)
    msgReq.close()

def listenServer( id, req ):
    site = url.urlopen(req)
    rec = site.read()
    while('connected' not in rec):
        site = url.urlopen(req)
        rec = site.read()
        if 'waiting' in rec:
            print("Waiting...")
    print('Found one')
    t = Thread(None,listen,None,(id,req))
    t.start()
    try:
        say(id,req)
    except  KeyboardInterrupt:
        omegleConnect()
        
def listen(id,req):
    while True:
        site = url.urlopen(req)
        rec = site.read()
        if 'strangerDisconnected' in rec:
                print('He is gone')
                disconnect(id)
                omegleConnect()
        elif 'typing' in rec:
                print("He's typing something...")          
        elif 'gotMessage' in rec:
                if 'asl' in rec[16:len( rec ) - 2] or 'm/f' in rec[16:len( rec ) - 2] or 'webcam' in rec[16:len( rec ) - 2]:
                    print(rec[16:len( rec ) - 2])
                    talk(id,req,'fuck you ass wipe.Get a life.')
                    disconnect(id)
                    print('Disconnected')
                else:
                    print(rec[16:len( rec ) - 2])
            
def say(id,req):
    while True:
        talk(id,req)
        time.sleep(5)

def omegleConnect():
    site = url.urlopen('http://omegle.com/start','')
    id = fmtId( site.read() )
    print(id)
    req = url.Request('http://omegle.com/events', urllib.urlencode( {'id':id}))
    print('Gotta find one')
    listenServer(id,req)

def disconnect( id ):
    url.urlopen( 'http://omegle.com/disconnect', urllib.urlencode( {'id':id} ) )
   
omegleConnect()
