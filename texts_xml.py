# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      user
#
# Created:     date
# Copyright:   (c) user year
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import os
from lxml import etree
import datetime as dt
import matplotlib.pyplot as plt
import re

wd = 'C:\\Users\\nickmc\\Documents\\texts_analysis'
data = 'texts_xml_data.xml'
os.chdir(wd)

######
# Remove Ordinal Character Function
def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) < 128)

######
# Read XML Data
text_tree = etree.parse(data)

sent_logical = []
body_text = []
contact_name = []
date_time = []


for df in text_tree.xpath('//sms'):
    for attrib in df.attrib:
        if attrib == 'type':
            sent_logical.append(df.attrib[attrib])
        if attrib == 'body':
            body_text.append(df.attrib[attrib])
        if attrib == 'contact_name':
            contact_name.append(df.attrib[attrib])
        if attrib == 'readable_date':
            date_time.append(df.attrib[attrib])
        # print('@' + attrib + '=' + df.attrib[attrib])

df_text = pd.DataFrame({'sent': sent_logical, 'body': body_text,
                        'contact': contact_name, 'datetime': date_time})

df_text['body'] = [remove_non_ascii(x) for x in df_text['body']]
df_text['datetime'] = pd.to_datetime(df_text['datetime'], format='%b %d, %Y %H:%M:%S %p')


min_date = min(df_text['datetime'])
max_date = max(df_text['datetime'])
length = 21
word_oi = 'zillow'
day_seq = pd.date_range(start=min_date, end=max_date-dt.timedelta(days=length), freq='D')

avg_z = []
for d in day_seq:
    text_array = df_text.loc[(df_text['datetime'] >= d) & (df_text['datetime'] < d + length),'body'].str.lower()
    text_concat = ' '.join(text_array)
    num_words = len(re.findall(r'\w+', text_concat))
    avg_z_temp = text_concat.count(word_oi)/float(num_words)
    avg_z.append(avg_z_temp)

plt.plot(avg_z)
plt.show()
######
# Define rolling window function average
def rolling_window(df, days, string):



    return 1