#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, send_file
from flask import redirect
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def getInfoNaver():
    header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
    url = 'https://search.naver.com/search.naver'
    params = {'sm':'top_hty', 'fbm' : '0', 'ie' : 'utf-8', 'query':'라디오+편성표' }
    r = requests.get(url, headers=header, params = params)
    bs = BeautifulSoup(r.content,'lxml')
    return bs
def getFrequency(location, channel):
    with open('radio_frequency.json','r') as f:
        json_data = json.load(f)
        f_list = json_data[location];
        return f_list[channel]
@app.route('/getRadioProgram/<location>')
def getRadioInfo(location):
    bs = getInfoNaver()
    programs = bs.select('#main_pack > div.sc.cs_tvtime._cs_tvtime > div.tvtime_wrap._tvtime_wrap > div._contents_area > div > div.timeline_body > div.list_right > div > div > ul > li')
    channels = bs.select('#main_pack > div.sc.cs_tvtime._cs_tvtime > div.tvtime_wrap._tvtime_wrap > div._contents_area > div > div.timeline_body > div.list_left > ul > li')
    times = bs.select('#main_pack > div.sc.cs_tvtime._cs_tvtime > div.tvtime_wrap._tvtime_wrap > div._contents_area > div > div.timeline_head > div.title_right > div > ul > li > span')
    ret = dict()
    a = []
    for time in times:
        a.append(time.text)
    ret['time'] = a
    p_list = []
    for program in programs:
        p_names = program.find_all('div',class_='ind_program')
        a = []
        for p_name in p_names:
            a.append(p_name.text)
        p_list.append(a)
    b = []
    for i in range(len(p_list)):
        info = {channels[i].text + ' ' + getFrequency(location,channels[i].text) : p_list[i]}
        b.append(info)
        #ret[channels[i].text] = p_list[i]
    ret['programs'] = b
    return ret
if __name__ == '__main__':
    #app.run(host='127.0.0.1', port='2020', debug = True)
    app.run()


# In[ ]:




