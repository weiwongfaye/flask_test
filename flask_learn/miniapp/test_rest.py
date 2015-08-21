# heartbeat value before load
from threading import Thread
import requests

def post_request(url,data,verify):
    'simulated forwarder to FWD director request'
    r = requests.post(url=url,data=data,verify =verify)
    print r


# simulate load to fwd director
thread_list = []

for i in range(100):
    payload ={"task":"jacktest"}
    p = Thread(target=post_request,args=('http://127.0.0.1:5000/todos',payload,False))
    thread_list.append(p)

for p in thread_list:
    p.start()

for p in thread_list:
    p.join()
