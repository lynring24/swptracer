#from utility import *
import os, sys, platform
import re, traceback
import time, calendar
import shutil
from uptime import uptime
from datetime import datetime, timedelta
import json
import resource
import csv
import pandas as pd
import numpy as np
from math import ceil, isnan

MICROSECOND = 1000000
DELIMETER ='\s+'

configure = dict()
configure['PATTERN'] = dict() 
configure['PATTERN']['rsyslog']='%Y-%m-%dT%H:%M:%S.%f'
configure['PATTERN']['dmesg']='%Y-%m-%dT%H:%M:%S,%f'
configure['PATTERN']['date']='%Y-%m-%dT%H:%M:%S[,.]%f'
configure['PATTERN']['block']='(\d+.\d{6}) (.+)'
configure['PATTERN']['MICROSEC']='(\d+:\d{2}:\d{2}[,\.]\d{6}) (.+)'



def get_pattern(x):
    return configure['PATTERN'].get(x)


def string_to_date(timestamp):
    try: 
        timestamp = datetime.strptime(timestamp, get_pattern('rsyslog'))
    except ValueError:
        timestamp = datetime.strptime(timestamp, get_pattern('dmesg')) 
    return timestamp
 

def extract(FAULT):
    print "$ extract ryslog log"
    CURRENT = os.getcwd()
    def get_path(x):
        return os.path.join(CURRENT, x)
    configure["TIME"] = string_to_date(os.path.basename(CURRENT))
    columns = pd.read_csv(get_path('awk.csv'), header=None, delimiter=DELIMETER, nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv(get_path('awk.csv'), header=None, delimiter=DELIMETER, usecols=[0, max_column-3, max_column-2, max_column-1])
    rsyslog.columns = ['timestamp', 'mode', 'swpentry', 'address']
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x[:-7]) - configure["TIME"]).total_seconds() * MICROSECOND)
    rsyslog = rsyslog[rsyslog.timestamp>= 0.0] 
    if FAULT !=True:
        rsyslog = rsyslog[rsyslog['mode']!='fault']

    print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
    rsyslog.to_csv(get_path('rsyslog.csv'), index=False) 
    print "\n[ Summary ]"
    print "> memory swap in# : {}".format(len(rsyslog[rsyslog['mode']=='map'].index))
    print "> memory page out # : {}".format(len(rsyslog[rsyslog['mode']=='out'].index))
    if FAULT== True:
        print "> memory page fault # : {}".format(len(rsyslog[rsyslog['mode']=='fault'].index))

if __name__ == "__main__":
    extract(False)
