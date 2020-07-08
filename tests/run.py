from threading import Thread
import requests
import time

nth_req = 1
old_req = 0

def run_parallel(threadid):
    global nth_req
    global old_req

    while True:
        try:
            resp = requests.get("http://127.0.0.1:1453/metrics/input/temperature")
        except:    
            print("ERROR RAISED!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:    
            print(f"Thread-{threadid}, response: {resp.text}, {nth_req}th request")
            nth_req += 1
            
            if old_req:
                print("diff between old req: ", time.time()-old_req)

            old_req = time.time()

        time.sleep(.1)


# for _ in range(1, 10):
#     Thread(target= run_parallel, args=(_+1,)).start()

run_parallel("0")
