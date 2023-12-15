


TIMEOUT = 5
CONNECTIONS = 100
from time import time
from datetime import datetime

import os
import time
import concurrent.futures
import subprocess
import math
import random


seconds = time.time()
years = seconds / 60 / 60 / 24 / 365.25




#   ShARED State Cache
#
#   'type' , 'uuid' , 'minute'
#   'type' , 'uuid' , 'time'
#
#

def worker_meta():
    try:
        worker_id = str( subprocess.check_output(['cat', '/etc/hostname']).decode() ).rstrip("\n\r")
    except Exception as e:
        worker_id = 'jetbrains'
    worker_type = os.environ.get('WORKER_TYPE' , default='imputer')
    try:
        print(' ENV ',os.environ )
        w  = int( os.environ.get('WORKER_NDX' ,  default=1 ) )
        worker_ndx = w
    except Exception as e:
        worker_ndx = 1
    worker_host= os.environ.get('HOSTNAME',default='unknown')

    if( worker_host in ['voldumont','gargamel'] ):
        worker_ndx=2
    else:
        worker_ndx=1

    #print(' Self Worker Host: ',worker_host )
    #print(' Self Worker   ID: ',worker_id)
    #print(' Self Worker TYPE: ',worker_type)
    #print(' Self Worker  NDX: ',worker_ndx )
    return { 'worker_id':worker_id , 'worker_type':worker_type , 'worker_ndx':worker_ndx , 'worker_host':worker_host}


result_array = []
def run( objects ):
    result_array=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        print('u')
        future_to_obj = (executor.submit(obj.sync, obj, TIMEOUT) for obj in objects )
        loaded_results  = concurrent.futures.as_completed(future_to_obj)
        for future in loaded_results:
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                result_array.append(data)


result_array = []
def runxl( objects , method_name ):
    TIMEOUT=5
    result_array=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_obj = (executor.submit( getattr( obj,method_name ) , obj, TIMEOUT) for obj in objects )
        loaded_results  = concurrent.futures.as_completed(future_to_obj)
        for future in loaded_results:
            try:
                data = future.result()
                print( data )
            except Exception as exc:
                data = str(type(exc))
            finally:
                result_array.append(data)


def runxlb( obj_arr_in , method_name ):
    result_array=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures_generator = ( executor.submit( getattr( obj,method_name ) ) for obj in obj_arr_in )
        completed_que  = concurrent.futures.as_completed( futures_generator )
        for future in completed_que:
            try:

                data = future.result()
                print( data )
            except Exception as exc:
                data = str(type(exc))
            finally:
                result_array.append(data)
    return result_array

def runxlb2( obj_arr_in , method_name ):
    result_array=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures_generator = ( executor.submit( getattr( obj,method_name ) ) for obj in obj_arr_in )
        completed_que  = concurrent.futures.as_completed( futures_generator )
        for future in completed_que:
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                result_array.append(data)
    return result_array



def runx( objects ):
    result_array=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_obj = (executor.submit(obj.run, obj, TIMEOUT) for obj in objects )
        loaded_results  = concurrent.futures.as_completed(future_to_obj)
        for future in loaded_results:
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                result_array.append(data)

def runp( objects  ):
    result_array=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_obj = (executor.submit(obj.patch, obj, TIMEOUT) for obj in objects )
        loaded_results  = concurrent.futures.as_completed(future_to_obj)
        for future in loaded_results:
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                result_array.append(data)

examps = [ i for i in range(1,100)]

# TIME BASED SLIDING WINDOW OFFSET
def select_segment_counts():
    workers_total = 2
    ndx = worker_meta()['worker_ndx']
    natural_offset = ndx-1
    now_second = datetime.now().second
    seconds_per_worker = 60 / workers_total
    magic_time_offset = math.floor( now_second/seconds_per_worker )
    print( 'WORKER ',ndx,'  Magic offset: ',magic_time_offset,'    SegSize: ',seconds_per_worker )

# TIME BASED SLIDING WINDOW OFFSET
def select_segment( all_arr ):
    workers_total = 2
    ndx = worker_meta()['worker_ndx']
    natural_offset = ndx-1
    now_second = datetime.now().second
    seconds_per_worker = 60 / workers_total
    magic_time_offset = math.floor( now_second/seconds_per_worker )
    items_per_segment = round(  len( all_arr ) / workers_total )
    start_point = ((natural_offset + magic_time_offset) * items_per_segment )%60
    end_point = start_point + items_per_segment
    return all_arr[start_point:end_point]


def select_random( all_arr ):
    return random.sample( all_arr , 60)