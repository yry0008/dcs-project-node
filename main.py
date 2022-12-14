import fastapi
from threading import Thread,Event
import configloader
import logging
import random
import uvicorn
import json
import tools
logging.basicConfig(
    level=getattr(logging,"INFO"), format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s"
)
class healthcheck(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.c = configloader.config()
        self.has_stop = False
        self.event = Event()
        nodeid = self.c.getkey("nodeid")
        if nodeid is None or nodeid == "":
            self.getnewid()
            nodeid = self.c.getkey("nodeid")

    def getnewid(self):
        import requests
        import json
        try:
            data = {
                "myhost":self.c.getkey("myhost"),
                "myip":tools.getip()
            }
            r = requests.post(self.c.getkey("midhost")+"/newserver",data=data,timeout=10)
            if r.status_code == 200 and json.loads(r.text)["ret"] == 0:
                self.c.setkey("nodeid",json.loads(r.text)["id"])
                self.c.reload()
            else:
                raise ValueError("No Node ID")
        except:
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError("No Node ID")

    def run(self):
        import requests
        import time
        
        while not self.has_stop:
            try:
                data = {
                    "nodeid":self.c.getkey("nodeid"),
                    "myhost":self.c.getkey("myhost"),
                    "myip":tools.getip()
                }
                r = requests.post(self.c.getkey("midhost")+"/healcheck",data=data,timeout=10)
                if r.status_code != 200 or json.loads(r.text)["ret"] != 0:
                    logging.error("Healthcheck failed")
            except:
                import traceback
                logging.error(traceback.format_exc())
            self.event.wait(10)

    def stop(self):
        self.has_stop = True
        self.event.set()

app = fastapi.FastAPI()
c = configloader.config()
@app.get("/getnum")
async def getnum():
    newnum = random.randint(c.getkey("minnum"),c.getkey("maxnum"))
    return {"ret":0,"num":newnum}

if __name__ == "__main__":
    h = healthcheck()
    h.start()
    uvicorn.run(app,host=c.getkey("bind"),port=c.getkey("port"))
    h.stop()