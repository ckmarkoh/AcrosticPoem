#-*- coding:utf-8 -*-
from util import *
import json
import random
import argparse
import sys 
import math
import operator
import copy

class PoemGen(object):
    def __init__(self):
        self._gram = {} 
        self._gram1 = [] 
        self._gram1_backup = []
        self._dict = {}
        self._yun = {}
        self._length = 0
        self._vword_count = 200
        self._vocab_type_dict = {'simple':10,'medium':7,'hard':4}
        self._vocab_type = 10
        self._itval_backward = 0
        self._itval_slash = None
        self._pinje = {0:[],1:[]}
        self._pinje_shun = {u' ':0, u'ˊ':0 , u'ˇ':1, u'ˋ':1,u'˙':1}
        self._print_out = True
        self.load_dict_gram()

    def reset(self):
        self._gram1 = copy.deepcopy(self._gram1_backup)
        self._length = 0
        self._vocab_type = 10
        self._itval_backward = 0
        self._itval_slash = None


    def print_out(self, s):
        if self._print_out:
            print s


    def load_dict_gram(self):
        dic = json.loads("".join(open_and_read("word_dict.json")))
        i=0
        for key in dic.keys():
            self._dict[key] = dic[key]
            this_yun = dic[key]['yun'] + unicode(self._pinje_shun[self._dict[key]['shun']])
            self._dict[key]['yun']= this_yun 
            self._yun[self._dict[key]['yun']] = self._yun.get(self._dict[key]['yun'],[])+[key]
            self._pinje[self._pinje_shun[self._dict[key]['shun']]] += [key]

        gram = json.loads("".join(open_and_read("gram_select.json")))
        gram1 = []
        for key in gram['2'].keys():
            keys = key.split(' ')
            self._gram[key] = math.log(gram['2'][key])
        for key in gram['1'].keys():
            if key in self._dict.keys():
                gram1.append(( key, gram['1'][key] ))
        #self._gram1 = gram1
        self._gram1 = sorted(gram1 ,key=lambda x:x[1],reverse=True)
        self._gram1_backup = copy.deepcopy(self._gram1)

    def select_words(self, weight=1): ##TODO check all yun
        #temp_list = [x[0] for x in self._gram1]
        result_list = []
        for i in range (self._vword_count):
            #idx = int(math.pow(random.random(),10) *len(self._gram1)*weight)
            idx = int(random.random()*len(self._gram1)*weight)
            if idx > len(self._gram1)-1 :
                idx = len(self._gram1)-1
            #print len(self._gram1)
            #print 'idx1',idx
            temp_item = self._gram1[idx]
            self._gram1.remove(temp_item) 
            result_list.append(temp_item)
        for item in result_list:
            #idx = int(math.pow(random.random(),10)*len(self._gram1)*weight)
            idx = int(1-math.pow(random.random(),10)*len(self._gram1)*weight)
            #print 'idx2',idx
            if idx > len(self._gram1)-1 :
                idx = len(self._gram1)-1
            self._gram1.insert(idx,item) 
            #self._gram1.append(item) 
        return [x[0] for x in result_list]

        #self._gram1 = [w for w in self._gram1 if w[0] in self._dict.keys() ]

             
    def viterbi_sub_2(self, pre_ary,this_ary,default=0.5,offset=0.01,backward=False,ignore_this=False,position=1):
        #print this_ary
        for tw in this_ary.keys():
            max_prob = 0
            max_pw = [pre_ary.keys()[0]] 
            all_temp_prob =[] 
            for pw in pre_ary.keys():
                if backward:
                    gram_str = u"%s %s"%(tw,pw)
                else:
                    gram_str = u"%s %s"%(pw,tw)
                if ignore_this:
                    this_prob = 1
                else:
                    this_prob = self._gram.get( gram_str ,default)

                temp_prob_val = this_prob * pre_ary[pw]['prob']
                temp_prob = (pw,temp_prob_val)
                if tw not in pre_ary[pw]['word'] :#and tw != pw:
                    all_temp_prob.append(temp_prob)

            if len(all_temp_prob) ==0:
                all_temp_prob.append(temp_prob)

            all_temp_prob = sorted(all_temp_prob,key=operator.itemgetter(1),reverse=True)
            rand_pw = all_temp_prob[int(random.random()*len(all_temp_prob)*offset)]
            #print rand_pw 
            this_ary[tw]['prob'] = rand_pw[1]
            if backward:
                this_ary[tw]['word'] = [rand_pw[0]] + pre_ary[rand_pw[0]]['word'] 
            else:
                this_ary[tw]['word'] = pre_ary[rand_pw[0]]['word'] + [rand_pw[0]]
        #return this_ary

    def viterbi_sub_1(self, word_start,interval,offset=0.01,backward=False):
        pre_ary = {}
        #word_start=[u'馬',u'英',u'狗']
        pre_ary[word_start[-1]] = {'prob':1.0,'word':word_start[:-1]} 
        #update_bar()
        for i in range(interval): 
            if i == interval -1 and (not backward):
                word_list  = self.select_words(10) 
            else:
                word_list = self.select_words()
            ignore_this = False
            this_ary = {}
            for word in word_list:
                this_ary.update({word:{'prob':0.0,'word':[]}})
            self.viterbi_sub_2(pre_ary,this_ary,backward=backward,ignore_this=ignore_this,position=i)
            pre_ary = this_ary
            #update_bar()
        return pre_ary
        #MyPrinter(pre_ary).print_data()

    def viterbi(self, word_start_raw,itval_backward=0,offset=0.01):

        itval_all = self._length - 1
        itval_forward = itval_all - itval_backward
        word_start = [word_start_raw]

        if itval_backward >= 1:
            pre_ary_backward = self.viterbi_sub_1(word_start,itval_backward,backward=True)
            #MyPrinter(pre_ary_backward).print_data()
            pre_ary_backward = sorted(pre_ary_backward.items(),key=lambda x:x[1]['prob'] ,reverse=True)
            rand_pw = pre_ary_backward[int(random.random()*len(pre_ary_backward)*offset)]
            word_start = [rand_pw[0]]+rand_pw[1]['word']

        pre_ary_forward = self.viterbi_sub_1(word_start,itval_forward)

        #        print " ".join(pre_ary_forward[key]['word'])
        #print [rand_pw[0]]+rand_pw[1]['word']
        return pre_ary_forward


    def not_repeat_word(self, la,lb):
        for w in la:
            if w in lb:
                return False
        else:
            return True

    #def not_same_yin(self, wa,wb):
    #    return self._dict[wa]['chuyin'] != self._dict[wb]['chuyin']

    def gen_poem_yun(self, word_yun, itval_dict, offset=0.01):

        yun_ary = {}
        
        for y in self._yun.keys():
            yun_ary[y] = [] 
            for i in range(len(word_yun)):
                yun_ary[y].append({'prob':0,'word':[],'last_word':[]})
       
        for (i,w_start) in enumerate(word_yun):
            pre_ary = self.viterbi(w_start,itval_backward = itval_dict[i]) 
            for w in pre_ary:
                yun = self._dict[w]['yun']
                last_word_ary = reduce(operator.add,[yun_ary[yun][j]['word'][-1:] for j in range(i+1)])
                if pre_ary[w]['prob'] > yun_ary[yun][i]['prob'] and w not in last_word_ary:
                    yun_ary[yun][i]['prob'] = pre_ary[w]['prob'] 
                    yun_ary[yun][i]['word'] = pre_ary[w]['word'] +[w]
                    
        yun_key_ary=[]
        for yun in yun_ary.keys():
            yun_prob_product =reduce(operator.mul, map(lambda x: float(x['prob']),yun_ary[yun]) )
            yun_prob_notempty =reduce(operator.and_,map(lambda x : len(x['word']) != 0,yun_ary[yun]) )
            if yun_prob_notempty :
                yun_key_ary.append((yun,yun_prob_product))
        #if yun_key_ary
        
        yun_key_ary = sorted(yun_key_ary, key=lambda x:x[1] ,reverse=True)
        result_yun_key = yun_key_ary[int(random.random()*len(yun_key_ary)*offset)]
        result_raw = yun_ary[result_yun_key[0]]
        result_ary = []
        for (i,rsl) in enumerate(result_raw):
            result_ary.append( (i,rsl['word']) )
        return dict(result_ary )
        


    def gen_poem_nonyun(self, word_nonyun, itval_dict, offset=0.01):

        result_ary = []
        for (i,w_start) in enumerate(word_nonyun):
            pre_ary = self.viterbi(w_start,itval_backward = itval_dict[i]).items() 
            pre_ary = sorted(pre_ary,key=lambda x:x[1]['prob'] ,reverse=True)
            rand_pw = pre_ary[int(random.random()*len(pre_ary)*offset)]
            result_ary.append( (i, rand_pw[1]['word'] + [rand_pw[0]]) )
        return dict(result_ary)
        #MyPrinter(result_dict).print_data()
        #return result_dict
         

    def gen_poem(self, raw_str,slash=False):
        word_yun = [] 
        word_nonyun = []
        word_idx_list = []
        itval_dict_yun = {}
        itval_dict_nonyun = {}

        if not self._itval_slash:
            itval_val =[self._itval_backward for i in range(len(raw_str))]
        else:
            lenid  = self._length-1
            if self._itval_slash == 'lr':
                itval_val =[i%lenid for i in range(len(raw_str))]
            elif self._itval_slash == 'rl':
                itval_val =[(lenid-1)-i%lenid for i in range(len(raw_str))]
            else:
                assert 0

        #print itval_val
        for (i,word) in enumerate(raw_str):
            if i==0 or i%2 !=0:
                word_idx_list.append((len(word_yun),'yun'))
                itval_dict_yun.update({len(word_yun):itval_val[i]})
                word_yun.append(word)
            else:
                word_idx_list.append((len(word_nonyun),'nonyun'))
                itval_dict_nonyun.update({len(word_nonyun):itval_val[i]})
                word_nonyun.append(word)
        result_yun = self.gen_poem_yun(word_yun,itval_dict_yun) 
        result_nonyun = self.gen_poem_nonyun(word_nonyun,itval_dict_nonyun)
        result_list = []
        
        for (idx,typ) in word_idx_list:
            if typ == 'yun':
                result_list.append( result_yun[idx] )
            elif typ == 'nonyun':
                result_list.append( result_nonyun[idx] )

        #MyPrinter(result_list).print_data()
        #for s in result_list:
        #    print "".join(s)
        return result_list
                    
    def main(self, input_str, print_out=True):
        self._print_out = print_out
        position_range = [ str(x) for x in range(1,7) ]
        parser = argparse.ArgumentParser( prog='' )
        parser.add_argument('words', help='the hidden words of each sentence.' )
        parser.add_argument('-l','--length', type=int, default=5
                            ,choices=[5,7] , help='number of words per sentence. (default: %(default)s)')
        parser.add_argument('-s','--seed', type=int , default=random.randint(0, sys.maxint) ,help='seed of random. ')
        parser.add_argument('-v','--vocab',  default ='simple'
                            ,choices=self._vocab_type_dict.keys(), help='type of vocabulary. ')
        parser.add_argument('-p','--position', default = '1'
                            ,choices=position_range+['lr','rl'], help='position of target words. ')

        args = parser.parse_args(input_str) 
        can_run= True
        self.print_out( "seed = %s"%(args.seed) )
        

        self._length = args.length
        self._vocab_type = self._vocab_type_dict[args.vocab]
        #print args.position
        #print position_range
        if args.position in position_range :
            self._itval_backward = int(args.position)-1
            if self._itval_backward >= self._length-1:
                can_run = False
                print "PoemGen: error: argument -p/--position is too large."
        else:
            self._itval_slash = args.position
        #random.seed( )
        result2=[]
        if can_run :
            random.seed( args.seed )
            word_raw = [w for w in args.words.decode('utf-8')] 
            result = self.gen_poem(word_raw)
            self.reset()
            for x in result:
                if print_out:
                    self.print_out( "".join(x))
                result2.append("".join(x))
        return "\n".join(result2)

def main():
    m = PoemGen()

    while True:
        s=raw_input('> ')
        try:
            m.main(s.split())
        except SystemExit:
            pass

def show_gram1():
    m = PoemGen()
    for key in m._gram1:
        print key[0].encode('utf-8'),key[1]
    #MyPrinter(m._gram1).print_data()

if __name__ == "__main__":
    #show_gram1()
    main()
        #print("do something else")


