# -*- coding: utf-8 -*
import codecs
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
