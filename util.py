# -*- coding: utf-8 -*
import codecs
import datetime
def open_and_write(fname,w):
    f=codecs.open(fname,'w','utf-8')
    f.write(w)
    f.close()

def open_and_read(fname,by_codecs=True):
    f=None
    if by_codecs: 
        f=codecs.open(fname,'r','utf-8')
    else :
        f=open(fname,'r')
    lines=f.readlines()
    f.close()
    return lines


class MyTimer(object):
  
  def __init__(self, name):
    self._total_time =  datetime.datetime.now() - datetime.datetime.now();
    self._start = 0;
    self._name = name

  def reset(self):
    self._total_time =  datetime.datetime.now() - datetime.datetime.now();
    self._start = 0;

  def start(self):
    self._start = datetime.datetime.now()

  def stop(self):
    self._total_time += datetime.datetime.now() - self._start

  def mprint(self):
    print "%s : %s"%(self._name, self._total_time)
    self.reset()

  
