# -*- coding: utf-8 -*-

"""определяет web-интерфейс
"""
from google.appengine.dist import use_library
#use_library('django', '1.2')

import cgi, os, re 
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users 
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.ext import db 

from google.appengine.runtime import DeadlineExceededError 

from params import *
from webpart.util import RenderPage, IsOperator
from webpart import  ajax
 
class Greeting(db.Model): 
    author = db.UserProperty() 
    content = db.StringProperty(multiline=True) 
    date = db.DateTimeProperty(auto_now_add=True) 
 
class oldMainPage(webapp.RequestHandler): 
    def get(self): 
        greetings_query = Greeting.all().order('-date') 
        greetings = greetings_query.fetch(10) 
 
        if users.get_current_user(): 
            url = users.create_logout_url(self.request.uri) 
            url_linktext = 'Logout' 
        else: 
            url = users.create_login_url(self.request.uri) 
            url_linktext = 'Login' 
    
        template_values = { 
          'greetings': greetings,
          'url': url,
          'url_linktext': url_linktext,
          } 

        RenderPage(self, 'old_index', template_values)     
        
    
class Guestbook(webapp.RequestHandler): 
    def post(self): 
        greeting = Greeting() 
     
        if users.get_current_user(): 
            greeting.author = users.get_current_user() 
     
        greeting.content = self.request.get('content') 
        greeting.put() 
        self.redirect('/')     
        
class MainPage(webapp.RequestHandler): 
    """Обработчик главной страницы
    """
    def get(self):    
        template_values = { 
          'app_id': os.environ['APPLICATION_ID'] ,
          } 
        RenderPage(self, 'main', template_values)
        

class AjaxHandler(webapp.RequestHandler): 
    """Обработчик запросов AJAX
    """
    def post(self, operator, action): 
        #logging.debug(operator)  
        try: 
            if self.request.headers.get('X-Requested-With') != 'XMLHttpRequest' and not IsOperator(operator):
                self.error(403)
            if action == '':
                self.error(404)
            elif action == 'test': 
                ajax.test(self, operator)            
            elif action == 'prefs':
                ajax.prefs(self, operator)
            elif action == 'send':
                ajax.send(self, operator)
            elif action == 'get':
                try:
                    timestamp = int(self.request.get("timestamp", default_value="0"))
                except:
                    timestamp = 0
                finally:
                    ajax.getmsgs(self, operator, timestamp)
            else:
                self.error(403)
        except DeadlineExceededError: 
            self.response.clear() 
            self.response.set_status(500) 
            self.response.out.write("This operation could not be completed in time...") 

        
class RemoteInterface(webapp.RequestHandler):
    """Внешний интерфейс оператора
    """
    #@todo: release
    def get(self, operator):
        RenderPage(self, 'operator_remote')

    
class WebInterface(webapp.RequestHandler):
    """Web интерфейс оператора
    """
    def get(self, operator):
        #logging.debug(operator)   
        template_values = { 
          'action_adr': '/' + ADR_AREA + ADR_DELIM + ADR_OPERATORS + ADR_DELIM + 
                        operator + ADR_DELIM + ADR_AJAX + ADR_DELIM,
          'opName': operator,
          'get_timeout': GET_MESSAGES_TIMEOUT,
          'get_interval_normal': GET_MESSAGES_INTERVAL_NORMAL,
          'get_interval_error': GET_MESSAGES_INTERVAL_ERROR,
          } 
        if IsOperator(operator): 
            RenderPage(self, 'operator_web', template_values)
        else:
            self.redirect('/error', permanent=False)
            
    
class ErrorPage(webapp.RequestHandler): 
    """Обработчик остальных запросов
    """
    def post(self, uri):
        '''POST запрос на неправильный адрес
        '''  
        self.error(404)
        self.response.out.write('O_o!')
      
    def get(self, uri):
        """Если введено имя оператора, то редирект на его страницу
        """
        try: 
            result = re.match('([a-zA-Z_0-9]+)$', uri)
            str = result.groups(1)[0]
        except:
            self.error(404)
            RenderPage(self, 'error', {'uri': uri})
        else:
            if not IsOperator(str):
                self.error(404)
                RenderPage(self, 'error', {'uri': uri})
            else:
                self.redirect(uri='/' + ADR_AREA + ADR_DELIM + ADR_OPERATORS + ADR_DELIM + str + ADR_DELIM, permanent=False)
            
 
application = webapp.WSGIApplication(
         [
          (r'/old', oldMainPage),
          (r'/sign', Guestbook),
          (r'/', MainPage),
          (r'/' + ADR_AREA + ADR_DELIM + ADR_OPERATORS + ADR_DELIM + '([a-zA-Z_0-9]+)' + ADR_DELIM + ADR_AJAX + ADR_DELIM + '([a-zA-Z_0-9]*)', AjaxHandler),
          (r'/' + ADR_AREA + ADR_DELIM + ADR_OPERATORS + ADR_DELIM + '([a-zA-Z_0-9]+)' + ADR_DELIM + ADR_IFRAME + ADR_DELIM + '?', RemoteInterface),
          (r'/' + ADR_AREA + ADR_DELIM + ADR_OPERATORS + ADR_DELIM + '([a-zA-Z_0-9]+)' + ADR_DELIM + '?', WebInterface),
          (r'/(.*)', ErrorPage)
         ],
        debug=True) 
 
def main(): 
    run_wsgi_app(application) 
 
if __name__ == "__main__": 
    main()
