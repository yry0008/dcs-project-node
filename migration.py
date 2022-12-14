import configloader
import argparse
import logging
import sys
import tools
parsing = argparse.ArgumentParser(description="Migration")
parsing.add_argument("-c", "--config", help="Config file", default="config.json")
parsing.add_argument("-l", "--log", help="Log file", default=None)
parsing.add_argument("-y", "--yes", help="ignore problems", action="store_true")
args = parsing.parse_args()
c = configloader.config(filename=args.config)
c_new = configloader.config(filename="config.example.json")
logging.basicConfig(
    level=getattr(logging,"INFO"), format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s"
)
if args.log != "" and args.log is not None:
    file_log_handler = logging.handlers.FileHandler(args.log, mode="w", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s")
    file_log_handler.setFormatter(formatter)
    file_log_handler.setLevel(getattr(logging,"INFO"))
    logging.getLogger('').addHandler(file_log_handler)
for key in c_new.dic:
    if key not in c.dic:
        c.setkey(key,c_new.getkey(key))
        logging.info("Add Value "+key + ":" + str(c_new.getkey(key)))
c.save()
c.reload()
keys = set(c.dic.keys())
keys_new = set(c_new.dic.keys())
keys_need_del = keys - keys_new
for key in keys_need_del:
    if not args.yes:
        print("Value "+key + ":" + str(c.getkey(key)) + "is deprecated, do you want to remove it? (y/n)")
        if input().lower() == "y":
            c.delkey(key)
            logging.info("Remove Value "+key + ":" + str(c.getkey(key)))
    else:
        logging.info("Remove Value "+key + ":" + str(c.getkey(key)))
        c.delkey(key)
myip = tools.getip()
c.setkey("myhost","http://{myip}:8001".format(myip=myip))
c.save()
logging.info("Migration successful")