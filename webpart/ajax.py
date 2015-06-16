# -*- coding: utf-8 -*-
'''
Created on 14.01.2010

@author: WQ85KUH

Обработчики AJAX команд
'''
from data_models import *
import json
from google.appengine.api import memcache, xmpp
from params import *
from time import sleep
from util import CheckMessageText
from webpart.exceptions import *
import logging
import datetime
import time


def test(self=None, operator=None):
    '''Тестовая команда
    @todo: release
    '''
    self.response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    str = json.dumps(
           {
                'a': u'фываQ',
                'operator': operator,
                'body': self.request.body
            },
           )
    self.response.out.write(str)


def prefs(self=None, operator=None):
    '''Сохраняет настройки
    @todo: release
    '''
    pass


def send(self=None, operator=None):
    '''сохраняет и пересылает сообщение
    '''
    try:
        result = appOperators.all().filter('active =', True).filter('isweb =', True).filter('login =', operator).get()
        opinfo = memcache.get(result.login)
        # проверка связи с пользователем
        if opinfo is None or opinfo.get('users') == None or opinfo.get('web') == None:
            logging.debug(u'web: что-то не так в processOperatorMsg(operator info)')
            raise Exception()
        else:
            # пишем сообщение в хранилище
            m = appOperatorsMsg(
                                sender=result.jid,
                                to=opinfo['users'][0],
                                text=CheckMessageText(self.request.get('msg')),
                                date=datetime.datetime.now(),
                                read=True
                                )
            m.put()
            # пересылаем сообщение пользователю
            xmpp.send_message(m.to, m.text)
            # обновляем timeout беседы
            memcache.set(result.login, opinfo, TALK_TIMEOUT)
            userinfo = memcache.get(m.to)
            if userinfo is None:
                answer.write(u'\nНеожиданное отсутствие связи с пользователем(processOperatorMsg)')
                raise Exception()
            else:
                memcache.set(m.to, userinfo, TALK_TIMEOUT)
            #вернуть что-нибудь
            self.response.out.write("{'status': 'ok'}")
    except Exception:
        pass


def getmsgs(self=None, operator=None, timestamp=0):
    '''Отдает новые сообщения
    '''
    self.response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    res = {}
    try:
        if not timestamp:
            res['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple())); #получать с текущего момента
        else:
            opJid = appOperators.all().filter('active =', True).filter('isweb =', True).filter('login =', operator).get().jid
            opinfo = memcache.get(operator)
            # проверка связи с пользователем
            if opinfo is None or opinfo.get('users') == None or opinfo.get('web') == None:
                logging.debug(u'web: что-то не так в getmsg(AJAX), возможно пользователь оффлфйн')
                raise UserOfflineError('возможно пользователь оффлфйн')

            # получаем непрочитанные сообщения
            logging.debug("Start : %s" % time.ctime())
            timeout = GET_MESSAGES_TIMEOUT / 1000 # переводим в секунды
            while timeout >= 0:
                results = appUserMsg.all().filter('to =', opJid).filter('read =', False).filter('sender =', opinfo['users'][0])
                if results.count() > 0 :
                    # выбираем сообщения и помечаем прочтенными
                    msgArray = []
                    results.fetch(limit=100)
                    for result in results:
                        msgArray.append({
                                         'message' : result.text,
                                         'user' : result.sender,
                                         'date' : result.date.strftime('%d.%m.%Y %H:%M:%S'),
                                         'timestamp' : int(time.mktime(result.date.timetuple())),
                                         })
                        result.read = True
                        # помнщаем опять в хранилище
                        try:
                            result.put()
                        except Exception:
                            logging.debug("web getmsgs: Put readed error!!!")
                    # возвращаем сообщения в результат
                    msgArray.sort(key=(lambda x: x['timestamp']))
                    res['messages'] = msgArray
                    res['timestamp'] = msgArray[-1]['timestamp'] #получать время последнего сообщения
                    break
                sleep(1)
                timeout = timeout - 1
            logging.debug("End : %s" % time.ctime())

    except UserOfflineError:
        res['error'] = u'Сейчас вы не связаны ни с одним клиентом!'
    except Exception:
        logging.debug('error in getmsgs!')
        self.error(403)
        raise

    # возвращаем JSON объект
    finally:
        self.response.out.write(json.dumps(res))
