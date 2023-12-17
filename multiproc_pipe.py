from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
 


def run_x( n , conn  ):
    while True:
        for x in range( 1000000000 ):
            val = n * n * n
        conn.send( {'mes':' x sending' , 'val':val} )

def run_y(n , conn ):
    while True:
        for x in range( 100000000 ):
            val  = n * n 
        conn.send( { 'me':'y sending' , 'val':val} )



if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    
    procz = []
    procz.append(Process(target=f, args=(child_conn,)))
    procz.append(Process(target=run_x, args=(3343434333.333, child_conn,)))
    procz.append(Process(target=run_y, args=(4443434334.4444, child_conn,)))

    #map(lambda p: p.start(), procz)
    for p in procz:
        p.start()
    
 

    print(' try start ')
    while True:
        what_sent = parent_conn.recv()
        
        print( what_sent )
