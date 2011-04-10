# -*- coding: utf-8 -*-

"""Просто кусочки кода. 
"""

# Our function to get the MD5 hash of a string
def getMD5Hash(textToHash=None):
    return hashlib.md5(textToHash).hexdigest()

# Example Usage
print getMD5Hash("Hello World!")


raise RuntimeError('You can\'t use person and system here')

channels.sort(key=lambda c: c.name)

from google.appengine.api import xmpp 
import os
#print xmpp.NO_ERROR
xmpp.send_invite('rombr@jabber.org', 'test'+'@'+os.environ['APPLICATION_ID']+'.appspotchat.com')
state = xmpp.send_message('ba2t@jabber.ru', 
                      "SEndPSY"
                      #, 'anything@krd-app.appspotchat.com'
                      #, 'about'+'@'+os.environ['APPLICATION_ID']+'.appspotchat.com'
                      )
print state



from google.appengine.api import memcache
from md5 import md5
#md5('ttttt')
#memcache.Client.add 


q = data_models.appService.all()
results1 = q.filter('active !=', False)
results =  results1.order('name')
i=0
for result in results:
 print "%s) %s\n" % (++i, result.name) 
 
 
 a = {'b':1, 'c':8}
print a.get('c')


try:
    #здесь код, который может вызвать исключение
    raise ExceptionType("message")
except (Тип исключения1, Тип исключения2, …), Переменная:
    #Код в блоке выполняется, если тип исключения совпадает с одним из типов
    #(Тип исключения1, Тип исключения2, …) или является наследником одного
    #из этих типов.
    #Полученное исключение доступно в необязательной Переменной.
except (Тип исключения3, Тип исключения4, …), Переменная:
    #количество блоков except не ограниченно
    raise #Сгенерировать исключение "поверх" полученного; без параметров - повторно сгенерировать полученное
except:
    #Будет выполнено при любом исключении, не обработанном типизированными блоками except
else:
    #Код блока выполняется, если не было поймано исключений.
finally:
    #будет исполненно в любом случае, возможно после соответствующего
    #блока except или else
    
    
from django.utils import simplejson

s = u'{"k": "кук", "b": "a"}'
o = simplejson.loads(s)
print o
so = simplejson.dumps(o)
print so    


result = re.match(pat, str)

