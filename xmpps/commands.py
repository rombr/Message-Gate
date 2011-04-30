# -*- coding: utf-8 -*-

'''Команды бота.
'''
from xmpps.msg_consts import *

from google.appengine.api import memcache

def cHelp(app, message=None):
    '''Команда помощи
    '''
    message.reply(u'Команда "/help". \n' #+ u'Ваш адрес: ' + message.sender
                  + HELP_MSG % (app.request.host_url,))
    
def cQuit(app, message=None):
    '''Команда завершения сессии 
    '''
    memcache.delete(message.sender)
    message.reply(u'Команда "/quit". \n')#+ u'Ваш адрес: ' + message.sender)
        
def cUnhandled(app, message=None):
    '''Неправильная команда
    '''
    message.reply(HELP_MSG % (app.request.host_url,)) 
