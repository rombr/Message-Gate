# -*- coding: utf-8 -*-

"""Модели данных
"""

from google.appengine.ext import db

class appService(db.Model):
    active = db.BooleanProperty(default=True)
    sname = db.StringProperty(required=True)

class appOperators(db.Model):
    active = db.BooleanProperty(default=False)
    isweb = db.BooleanProperty(default=False)
    oname = db.StringProperty(required=True)
    login = db.StringProperty(required=True)
    password = db.StringProperty(default='zx')
    sname = db.StringProperty()
    jid = db.StringProperty()
  
class appOperatorsMsg(db.Model):
    read = db.BooleanProperty(default=False)
    sender = db.StringProperty(required=True)
    to = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    date = db.DateTimeProperty(required=True)

class appUserMsg(db.Model):
    read = db.BooleanProperty(default=False)
    sender = db.StringProperty(required=True)
    to = db.StringProperty(required=True)
    operator = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    date = db.DateTimeProperty(required=True)
    