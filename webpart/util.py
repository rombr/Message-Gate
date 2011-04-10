# -*- coding: utf-8 -*-

'''
Created on 12.01.2010
 
@author: WQ85KUH

Вспомогательные средства
'''

import os, logging

from google.appengine.ext.webapp import template

from data_models import *

def RenderPage(self=None, template_name='', template_values={}):
    """Осуществляет рендеринг страницы по шаблону и параметрам
    """
    #path = os.path.join(os.path.dirname(__file__), 'template/'+template_name+'.html') 
    self.response.out.write(template.render('./../templates/' + template_name + '.html', template_values))  
    
def IsOperator(str=None):
    """Оператор или нет
    """
    result = appOperators.all().filter('login =', str).get()
    if result == None:
        logging.debug('web: not operator')
        return False

    return True


def CheckMessageText(s):
    '''Преобразование строки для хранения ивывода
    '''
    replace_map = {
                   #'&' : '&amp;',
                   '"' : '&quot;',
                   "'" : '&#039;',
                   '<' : '&lt;',
                   '>' : '&gt;',
                   }
    s = s.strip()
    for k, v in replace_map.items(): s = s.replace(k, v)
    return s
