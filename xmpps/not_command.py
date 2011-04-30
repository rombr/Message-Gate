# -*- coding: utf-8 -*-

'''Обработка входящих сообщений
'''

from xmpps.msg_consts import *
from params import *
from data_models import *
from webpart.util import CheckMessageText

import datetime, os

import logging
from StringIO import StringIO
from random import randrange

from google.appengine.api import xmpp 
from google.appengine.api import memcache

def getServicesList(ret):
    '''Получает список доступных служб и
    выводит в сообщение
    ''' 
    results = appService.all().order('sname')#.filter('active !=', False)
    i = 0
    for result in results:
        if result.active:
            i += 1  
            ret.write("%s) %s\n" % (i, result.sname))

def initTalk(n=0, message=None):
    '''Инициализирует сессию между пользователем и оператором
    '''
    # выбор службы с номером n
    results = appService.all().order('sname').fetch(100)
    srv = ''
    i = j = 0
    while srv == '' and j < len(results):
        if results[j].active:
            i += 1  
            if i == n:
                srv = results[j].sname
        j += 1
    if srv == '': return False
    # выбор активного оператора этой службы
    results = appOperators.all().filter('active =', True).filter('sname =', srv).fetch(1000)
    if len(results) == 0:
        logging.debug('no operators ') 
        return False 
    #@warning: берется случайным образом, но в целях отладки первый
    op = results[0]#randrange(0, len(results))]
    # пишем сессии
    memcache.set(message.sender,
                 {'operator': op.login} 
                 , TALK_TIMEOUT)
    opinfo = memcache.get(op.login)
    if opinfo is None:
        memcache.set(op.login,
                     {
                      'users': [message.sender],
                      'web': op.isweb
                     } 
                     , TALK_TIMEOUT)
    else:
        memcache.set(op.login,
                     {
                      'users': opinfo['users'].append(message.sender),
                      'web': op.isweb
                     } 
                     , TALK_TIMEOUT)
    return True
    

def isOperator(message=None):
    '''является ли оператором
    '''
    results = appOperators.all().filter('active =', True).filter('isweb =', False).fetch(1000)
    if len(results) == 0:
        logging.debug('no Jabber operators free')
        return False
    for result in results:
        if result.jid == message.sender.split('/')[0]: return True
    return False

def processUserMsg(message=None, answer=None):
    '''Обработка сообщения от пользователя
    '''
    userinfo = memcache.get(message.sender)
    if  userinfo.get('operator') == None:
        logging.debug(u'что-то не так в processUserMsg(user info)')
        answer.write(u'В данный момент вы ни связаны ни с каким оператором(no user)!')
        raise Exception()
    else:
        opinfo = memcache.get(userinfo.get('operator'))
        if opinfo is None or opinfo.get('users') == None :#or opinfo.get('web')==None:
            logging.debug(u'что-то не так в processUserMsg(operator info)')
            answer.write(u'В данный момент вы ни связаны ни с каким оператором(no operator)!')
            raise Exception()
        else:
            # пишем сообщение в хранилище
            result = appOperators.all().filter('active =', True).filter('login =', userinfo.get('operator')).get() #.filter('isweb =', False)
            m = appUserMsg(
                    sender=message.sender, #.split('/')[0],
                    operator=userinfo.get('operator'),
                    to=result.jid,
                    text=CheckMessageText(message.body),
                    date=datetime.datetime.now(),
                    read=True
                    )
            # web сообщения помечаем непрочитанными
            if opinfo.get('web'):
                #logging.debug('web work')
                m.read = False
            else:
                # пересылаем сообщение оператору
                xmpp.send_message(m.to, u'Беседа с %s \n' % (message.sender,) + m.text)
            m.put()
            # обновляем timeout беседы
            memcache.set(userinfo.get('operator'), opinfo, TALK_TIMEOUT)
            memcache.set(message.sender, userinfo, TALK_TIMEOUT)
                
def processOperatorMsg(message=None, answer=None):
    '''Обработка сообщения от оператора
    '''
    result = appOperators.all().filter('active =', True).filter('isweb =', False).filter('jid =', message.sender.split('/')[0]).get()
    opinfo = memcache.get(result.login)
    # проверка связи с пользователем
    if opinfo is None or opinfo.get('users') == None or opinfo.get('web') == None:
        logging.debug(u'что-то не так в processOperatorMsg(operator info)')
        answer.write(u'\nВ данный момент вы ни с кем не переписываетесь!')
    else:
        # пишем сообщение в хранилище
        m = appOperatorsMsg(
                            sender=message.sender.split('/')[0],
                            to=opinfo['users'][0],
                            text=CheckMessageText(message.body),
                            date=datetime.datetime.now(),
                            read=True
                            )
        m.put()
        # пересылаем сообщение оператору
        xmpp.send_message(m.to, m.text)  
        # обновляем timeout беседы
        memcache.set(result.login, opinfo, TALK_TIMEOUT)
        userinfo = memcache.get(m.to)
        if userinfo is None:
            answer.write(u'\nНеожиданное отсутствие связи с пользователем(processOperatorMsg)')            
        else:
            memcache.set(m.to, userinfo, TALK_TIMEOUT)              
                                  

def MainHandler(app, message=None):
    '''Логика формирования ответного сообщения
    '''
    answer = StringIO()
    #answer.write(u'Время: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    #answer.write(u'\nВы ввели текст: '+ message.body + u'\nВаш адрес: ')
    #answer.write(message.sender + u'\nНаш адрес: ' + message.to + '\n')
    try:
        if not isOperator(message):
            # пользователь
            user_state = memcache.get(message.sender)
            if user_state is None:
                # новый
                answer.write(u'Выберите службу из списка, введя номер(для тестирования доступна 2)\n или /help для списка команд!\n')
                getServicesList(answer)
                answer.write(u'Введите номер')
                memcache.add(message.sender, 0, CHOOSE_TIMEOUT)
                message.reply(answer.getvalue())
            else:
                # выбирает службу
                if user_state == 0:
                    if message.body.isdigit():
                        if initTalk(int(message.body), message):
                            answer.write(u'Вы ввели число: ' + message.body + u', беседа будет начата')
                        else:
                            answer.write(u'Служба с таким номером не найдена, либо все операторы заняты!\n' + u'Попробуйте еще раз!') 
                            memcache.set(message.sender, 0, CHOOSE_TIMEOUT)
                    else:
                        # неправильный выбор
                        answer.write(u'Попробуйте еще раз!')
                        memcache.set(message.sender, 0, CHOOSE_TIMEOUT)
                    message.reply(answer.getvalue())
                else:
                    # ведет беседу
                    answer.write(u'Служба выбрана, беседа идет:\n')
                    processUserMsg(message, answer)
        else:
            # оператор
            answer.write(u'Вы оператор!')
            processOperatorMsg(message, answer)
    except ValueError:
        # ошибка
        logging.debug('ValueError inmessage exception(MainHandler)')
        #message.reply(answer.getvalue())
