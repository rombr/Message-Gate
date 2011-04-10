 # -*- coding: utf-8 -*-
 
"""Центральный модуль обработки XMPP запросов
"""   
  
import logging 

from google.appengine.dist import use_library
#use_library('django', '1.2')

from xmpps import commands, not_command

from google.appengine.api import xmpp 
from google.appengine.ext import webapp 
from google.appengine.ext.webapp import xmpp_handlers 
from google.appengine.ext.webapp.util import run_wsgi_app
  
class XmppHandler(xmpp_handlers.CommandHandler): 
    """Handler class for all XMPP activity.""" 
    
    def text_message(self, message=None):
        not_command.MainHandler(self, message)
     
    def unhandled_command(self, message=None): 
        commands.cUnhandled(self, message)
    
    def help_command(self, message=None): 
        commands.cHelp(self, message)      
    
    def quit_command(self, message=None): 
        commands.cQuit(self, message)

  
def main(): 
    app = webapp.WSGIApplication([ 
       ('/_ah/xmpp/message/chat/', XmppHandler), 
       ], debug=True) 
    run_wsgi_app(app) 
  
  
if __name__ == '__main__': 
    main() 