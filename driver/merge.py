from utility import *

TIME=0
TOP=1
BTM=2
FNAME=3
FUNC=4
VAR=5

<<<<<<< HEAD
=======
ALLOC='0'
SWP='1'
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3

def merge():
    print "$ record page info"
    with open(get_path('merge'), 'r') as merge:
         global page_table
         page_table = []
         for track in merge:
             item = [x.strip() for x in track.split(',')]
             if len(item) > 2 : 
                add_page_table(item)
             else:
                classify_area(item)
    merge.close()


<<<<<<< HEAD
def add_page_table(item):
    dump = [item[TIME], item[TOP], item[BTM], item[FNAME], item[FUNC], item[VAR]] 

    if dump in page_table:
        page_table.append(dump)
    else:
        page_table.append(dump)
=======
def write(line): 
    output=open(get_path('total'), 'a+')
    output.write(line)



def add_page_table(item):
    dump = [item[TIME], item[TOP], item[BTM], item[FNAME], item[FUNC], item[VAR]] 
    page_table.append(dump)
    item=dump[:2]+dump[3:]+[ALLOC]
    line = ','.join(item) + "\n"
    write(line)
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3


def classify_area(item): 
       # run key and find the key that fits most
<<<<<<< HEAD
       output=open(get_path('total'), 'a+')
=======
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
       page_table.sort(reverse=True)
       item[1]=item[1][:-2]
       if page_table is not None:
          for track in page_table:
              if track[TOP] <= item[TOP] and item[TOP] <= track[BTM] and track[TIME] <= item[TIME]: 
                 # remove endline
                 item.extend([track[FNAME], track[FUNC], track[VAR]])
                 break       
<<<<<<< HEAD
       line = ','.join(item) + "\n"
       output.write(line)
       #write_in_area(line, item[TOP])


borders = ['0x2000000', '0x40000000', '0x60000000',  '0xA0000000', '0xE0000000', '0xE0100000']
def write_in_area(line, vas):
    vpn = int(int(vas)/get_page_size())
    area_num = 1
    for border in borders:
        if vpn < int(border, 16):
           break
        area_num+=1
    with open(get_sub_path_by_id(area_num), 'a+') as sub:
         sub.write(line) 
=======
       item.append(SWP)
       line = ','.join(item) + "\n"
       write(line)
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
