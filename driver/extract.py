from utility import *
import csv
import pandas as pd

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def extract_swap():
    global area_subs
    try:
	print "$ extract ryslog log"
        columns = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', nrows=1)
        max_column = columns.shape[1]
        rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', usecols=[0, max_column-4, max_column-3, max_column-2, max_column-1])

        rsyslog.columns = ['timestamp', 'cmd', 'mode', 'swpentry', 'address']
        rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds())
        rsyslog = rsyslog[rsyslog.timestamp>= 0.0]
        rsyslog['address'] = rsyslog['address'].apply(lambda x : str(int(x, 16)/get_size('block'))) 
        
        print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
        rsyslog.to_csv(get_path('merge'))
        # for map.timestamp faster than in.timestamp && map.swpentry == in.swpentry in[anchor] = map.timestamp
        print "$ extract duplicated entries"
        group = rsyslog.groupby('swpentry')['timestamp'].unique()
        group = group[group.apply(lambda x: len(x)>1)]
        group.to_frame().to_csv(get_path('head')+'/duplicated_entries.csv')
        # anchor the related timestamp
        print "$ extract duplicated address"
        group = rsyslog.groupby('address')['timestamp'].unique()
        group = group[group.apply(lambda x: len(x)>1)]
        group.to_frame().to_csv(get_path('head')+'/duplicated_address.csv')
        
        if is_false_generated(get_path('merge')):
            raise FileNotFoundError 
    except FileNotFoundError:
           print "False generate 'merge.csv'"
          # clean_up_and_exit(get_path('merge'), 'extract')
          


def extract_malloc():
    print "$ extract memory allocation"
    alloclog = pd.read_csv(get_path('hook'), header=None,  delimiter='\s+')
    alloclog.columns['timestamp', 'file','line','func','var', 'address', 'size']
    alloclog['timestamp'] = alloclog['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds())
    alloclog = alloclog[alloclog.timestamp>= 0.0]
    alloclog['address'] = alloclog['address'].apply(lambda x : str(int(x, 16)/get_size('block'))) 
    if is_false_generated(get_path('hook')):
       print "Allocation Hook False Generated"
       clean_up_and_exit(get_path('merge'),'extract allocation')



