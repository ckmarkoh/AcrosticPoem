#-*- coding:utf-8 -*-
from AcrosticPoem import PoemGen
from sys import argv
import datetime
from random import random
import logging

logid = random()
logging.basicConfig(filename='log_file.log',level=logging.INFO)

logging.info('id:%s, args:%s',logid," ".join(argv[1:]))
logging.info('id:%s, start:%s',logid,datetime.datetime.now())
 
m = PoemGen()
#print argv
#print argv
#argv[1] = argv[1].decode('big5')
result = m.main(argv[1:],print_out = False)
print result.encode('utf-8')
logging.info('id:%s, end:%s',logid, datetime.datetime.now())
