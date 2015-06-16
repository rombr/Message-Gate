# -*- coding: utf-8 -*-
'''
Параметры приложения
'''
import os


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIR = os.path.join(PROJECT_PATH, 'templates')

CHOOSE_TIMEOUT = 60
TALK_TIMEOUT = 180
GET_MESSAGES_TIMEOUT = 25000
GET_MESSAGES_INTERVAL_NORMAL = 300
GET_MESSAGES_INTERVAL_ERROR = 15000

# Параметры адреса
ADR_DELIM = '/'
ADR_AREA = 'area'
ADR_OPERATORS = 'operators'
ADR_AJAX = 'ajax'
ADR_IFRAME = 'iframe'
