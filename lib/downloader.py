#!/usr/bin/env python
import logging
from urllib import FancyURLopener
from multiprocessing import Pool, Manager, Process
from time import sleep
from itertools import repeat
import sys

class SpoofOpen(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) ' + \
            'Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'

def download_file(args):
    url_and_name, m_list = args
    log = logging.getLogger('dl_thread')
    url, filename = url_and_name
    
    spoof = SpoofOpen()
    try:
        with open(filename, 'wb') as dest:
            source = spoof.open(url)
            dest.write(source.read())
        log.debug('download complete: ' + filename)
        m_list.append(filename)
    except KeyboardInterrupt, e:
        pass
def update_progress(progress):
    barLength = 35 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...        \r\n"
    if progress >= 1:
        progress = 1
        status = "Done...        \r\n"
    block = int(round(barLength*progress))
    text = "\rDownloading:        [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def download_monitor(args):
    managed_list, total_items = args
    print ''
    while True:
        progress = float(len(managed_list))/float(total_items)
        update_progress(progress)
        if total_items == len(managed_list):
            return
        sleep(0.2)

def multi_download(url_and_name_list, num_threads=8):
    ''' accepts list of tuples, where t[0] = url and t[1] = filename '''
    manager = Manager()
    m_list = manager.list()

    monitor_thread  = Process(target=download_monitor, args=((m_list,len(url_and_name_list)),))

    monitor_thread.start()
    log = logging.getLogger('multi_dl')
    log.debug('starting pool with ' + str(num_threads) + ' workers')
    workers = Pool(processes=num_threads)
    work = workers.map_async(download_file, zip(url_and_name_list, repeat(m_list)))

    # this hack makes the async_map respond to ^C interrupts
    try:
        work.get(0xFFFF)
        monitor_thread.join()
        sys.stdout.write('\n\n')
    except KeyboardInterrupt:
        print 'parent received control-c'
        exit()
