import time 
import xbmc
import xbmcaddon
import xbmcgui
import urllib2
import base64

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
tiempo = addon.getSetting('tiempo') 

def do_the_job():

    myurl = addon.getSetting('hostname') 
    if myurl == "" :
          keyboard = xbmc.Keyboard("","HostName")
          keyboard.doModal()
          if (keyboard.isConfirmed()):
             myurl = keyboard.getText()
             addon.setSetting("hostname", myurl)
    
    username = addon.getSetting('username') 
    if username == "" :
          keyboard = xbmc.Keyboard("","Username")
          keyboard.doModal()
          if (keyboard.isConfirmed()):
             username = keyboard.getText()
             addon.setSetting("username", username)
             
    password =  addon.getSetting('password') 
    if password == "" :
          keyboard = xbmc.Keyboard("","Password")
          keyboard.setHiddenInput(True)
          keyboard.doModal()
          if (keyboard.isConfirmed()):
             password = keyboard.getText()
             addon.setSetting("password", password)
    
    notify = addon.getSetting("notify")

    web_page = urllib2.urlopen("http://iptools.bizhat.com/ipv4.php")
    myip = web_page.read()
    #toshow = "IP actual : " + myip + "\n"

    update_url = "https://dynupdate.no-ip.com/nic/update?hostname=" + myurl + "&myip=" + myip

    req = urllib2.Request(update_url)
    req.add_header('Authorization', 'Basic '+base64.encodestring(username+":"+password).replace("\n",""))
    resp = urllib2.urlopen(req)
    content = resp.read()

    time = 7000 #in miliseconds
    if notify:
       xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname," "+content, time, icon))
    #xbmc.log("IP: %s. NoIp service executed at %s" % (content, time.time()))
    xbmc.log("ejecutado NoIp")
    
    return;

do_the_job()

if __name__ == '__main__':

    monitor = xbmc.Monitor()
 
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds ( media hora )
        if monitor.waitForAbort(60*int(tiempo)):
            # Abort was requested while waiting. We should exit
            break
        do_the_job()




        