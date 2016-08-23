import requests
from django.conf import settings
import json
from datetime import datetime

def sendMessage(number_string_list, message_content):
    # number_list = [ num1, num2, ...]
    # message_content <= 160 car
    # discussion_id : for log
    date = str(datetime.now())
    corrected_list = set_as_valid_list(number_string_list)
    data_string = '{"numbers":[%s],"message":"%s . sent %s"}' %(corrected_list['string'], message_content, date)
    headers = {'user-agent': "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)",
               'Content-Type': 'application/json',
               'Content-Length' : len(data_string)}
    ssl_verify = False
    response = requests.post(settings.DW_SMS_API_URL,
                             headers=headers,
                             verify=ssl_verify,
                             data=data_string)
    #save_log_outbound(response, corrected_list['list'], message_content, date, "")
    return response

def set_as_valid_list(number_string_list):
    # number_string_list may be like 261xxxx, 261xxx
    # hard correct to "261xxxx", "261xxx" 
    number_list = [n.strip() for n in number_string_list.split(",")] #remove "spaces" 
    cl =  '", "'.join(map(str, number_list))
    return {'string' : '"' + cl + '"',
        'list' : number_list}

