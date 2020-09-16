import os
import pandas as pd
import numpy as np
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

MICROSECOND = 1000000

class Tracker(object):
    def __init__(self, axis, data):
        self.axis = axis
        self.data = data
    
    def add_plot(self, row):
        x = [row[0], row[0]]
        y = [row[1], row[2]]

    def run(self):
        pool = Pool(processes=cpu_count())
        return pool.map(self.add_plot, self.data)


labels={'map':'swap-in','fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'create':'allocation'}
colors={'map': 'mediumseagreen', 'out':'skyblue', 'fault':'lightpink', 'create': 'darkorange', 'layout':'lightslategrey', 'handle_mm':'lightslategrey' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}

def plot_out(dir_path, mean_time):
    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)

    #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
    #    hook = pd.read_csv(dir_path+"/hook.csv", usecols=['timestamp', 'address','size'])
    #    hook['mode'] = 'create'
    #    joined = pd.concat([hook[['timestamp', 'address', 'mode']], joined[['timestamp', 'address', 'mode']]])
    #joined['timestamp'] = joined['timestamp'].astype(int)
    #joined['address'] = joined['address'].astype(int)
               

    digits = len(str(rsyslog['address'].min()))-1
    min_range = int(str(rsyslog['address'].min())[:-1*digits])*pow(10, digits)
    max_range = (int(str(rsyslog['address'].max())[:-1*digits])+2)*pow(10, digits)
    POW = pow(10, digits-2)
    biny = [ y for y in range(min_range, max_range, POW)]
    rsyslog['labely'] = pd.cut(x=rsyslog['address'], bins=biny)  
    
    subyranges = [ [group.address.min(), group.address.max()] for name, group in rsyslog.groupby('labely') ]
    subyranges = pd.DataFrame(subyranges).replace([np.inf, -np.inf], np.nan).dropna().values.tolist()
    subyranges = [ y for y in subyranges if y != [] ]

    if os.path.isfile('{}/maps'.format(dir_path)) == True:
        maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None)
        maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
        maps['pathname'] = maps['pathname'].fillna('anon')
        
        maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('address'))
        maps = maps.drop('layout', 1)
        maps['address0'] = maps['address0'].apply(lambda x: int(x, 16)) 
        maps['address1'] = maps['address1'].apply(lambda x: int(x, 16)) 
        maps  = maps[['address0','address1','pathname']]
        maps = maps.drop_duplicates()
            

    GRIDS = len(subyranges)
    fig, axes = plt.subplots(nrows=GRIDS)
    if GRIDS==1:
        axes = [axes]

    # set spines false
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
    
    #fig.tight_layout()
    #fig.subplots_adjust(left=0.1)
    
    #layout = plt.twinx()
    #layout.spines["left"].set_position(('axes', 1.2))
    #make_patch_spines_invisible(layout)
    #layout.spines['left'].set_visible(True)

    rect_end = rsyslog['timestamp'].max()

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
        
    for idy in range(0, GRIDS):
        for name, group in rsyslog.groupby('mode'):
            axes[idy].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])

        #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
        #    for index, rows in hook.iterrows():
        #        axes[idy].add_patch(mpl.patches.Rectangle((rows['timestamp'], rows['address']), (rect_end - rows['timestamp']), rows['size'], color=colors['create'], label=labels['create'],zorder=0))

        converty = GRIDS-(idy+1)
        axes[idy].set_ylim(subyranges[converty][0], subyranges[converty][1])

        if idy == 0:
            axes[idy].spines['top'].set_visible(True)
            axes[idy].set_xticks([])
        elif idy == GRIDS -1:
            axes[idy].spines['bottom'].set_visible(True)
        else:
            axes[idy].set_xticks([])

        if idy == 0:
            axes[idy].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[idy].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
        else:
            kwargs.update(transform=axes[idy].transAxes)  # switch to the bottom axes
            axes[idy].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
            axes[idy].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
            axes[idy].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[idy].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
         
                        
    plt.legend()
    plt.rcParams["figure.figsize"] = (14, 14)
    plt.suptitle('Virtual Address by timeline')
    #axes[int(len(subyranges)/2)][0].set_xlabel('timestamp')
    #axes[len(subyranges)-1][int(grids[0]/2)].set_ylabel('Virtal Address')


    # output
    print "$ save plot"
    plt.savefig(dir_path+"/plot.png",format='png', dip=100)
    if os.environ.get('DISPLAY','') != '':
     	plt.show()

