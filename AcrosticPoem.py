#-*- coding:utf-8 -*-
from util import *
import json
import random
import argparse
import sys 
import operator
import copy



class PoemGen(object):
    def __init__(self):
        self._gram2 = {} 
        self._gram1 = [] 
        self._gram1_backup = []
        self._dict = {}
        self._yun = {}
        self._length = 0
        self._vword_count = 400
        self._itval_backward = 0
        self._itval_slash = None
        self._pinje = {0:[],1:[]}
        self._pinje_shun = {u' ':0, u'ˊ':0 , u'ˇ':1, u'ˋ':1,u'˙':1}
        self._print_out = True
        self.load_dict_gram()

    def reset(self):
        self._gram1 = copy.deepcopy(self._gram1_backup)
        self._length = 0
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
        self._gram1 = json.loads("".join(open_and_read("gram1.json")))
        self._gram2 = json.loads("".join(open_and_read("gram2.json")))
        self._gram1_backup = copy.deepcopy(self._gram1)

    def select_words(self): 
        result_list = []
        for i in range (self._vword_count):
            idx = int(random.random()*len(self._gram1))
            temp_item = self._gram1[idx]
            result_list.append(temp_item[0])
        return result_list


             
    def viterbi_sub_2(self, pre_ary,this_ary,default=0.5,backward=False,position=1):
        for tw in this_ary.keys():
            max_prob = 0
            rand_pw = None             
            temp_prob_val = 0
            for pw in pre_ary.keys():
                if backward:
                    gram_str = u"%s %s"%(tw,pw)
                else:
                    gram_str = u"%s %s"%(pw,tw)
                this_prob = self._gram2.get( gram_str ,default)
                temp_prob_val = this_prob * pre_ary[pw]['prob']
                temp_prob = (pw,temp_prob_val)
                if temp_prob_val >= max_prob:
                    rand_pw = (pw, temp_prob_val)
                    max_prob = temp_prob_val
            this_ary[tw]['prob'] = rand_pw[1]
            if backward:
                this_ary[tw]['word'] = [rand_pw[0]] + pre_ary[rand_pw[0]]['word'] 
            else:
                this_ary[tw]['word'] = pre_ary[rand_pw[0]]['word'] + [rand_pw[0]]

    def viterbi_sub_1(self, word_start,interval,backward=False):
        pre_ary = {}
        pre_ary[word_start[-1]] = {'prob':1.0,'word':word_start[:-1]} 
        for i in range(interval): 
            word_list = self.select_words()
            this_ary = {}
            for word in word_list:
                this_ary.update({word:{'prob':0.0,'word':[]}})
            self.viterbi_sub_2(pre_ary,this_ary,backward=backward,position=i)
            pre_ary = this_ary
        return pre_ary

    def viterbi(self, word_start_raw,itval_backward=0):
        itval_all = self._length - 1
        itval_forward = itval_all - itval_backward
        word_start = [word_start_raw]
        if itval_backward >= 1:
            max_w = None;
            max_prob = 0;
            pre_ary_backward = self.viterbi_sub_1(word_start,itval_backward,backward=True)
            for w in pre_ary_backward:
                this_prob = pre_ary_backward[w]['prob'];
                if this_prob >= max_prob:
                    max_prob = this_prob;
                    max_w = w;
            word_start = [max_w] + pre_ary_backward[max_w]['word'];
        pre_ary_forward = self.viterbi_sub_1(word_start,itval_forward)
        return pre_ary_forward


    def not_repeat_word(self, la,lb):
        for w in la:
            if w in lb:
                return False
        else:
            return True


    def gen_poem_yun(self, word_yun, itval_dict):
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

        max_yun_product = 0;
        max_yun = None;
        for yun in yun_ary:
            yun_prob_product = 1;
            for i in range(len(yun_ary[yun])):
                yun_prob_product *= yun_ary[yun][i]['prob'];
                if len(yun_ary[yun][i]['word']) == 0:
                    continue;
            if yun_prob_product >= max_yun_product:
                max_yun_product = yun_prob_product;
                max_yun = yun;
        result_raw = yun_ary[max_yun];
        result_ary = {} 
        for (i,rsl) in enumerate(result_raw):
            result_ary[i] = rsl['word'];
        return result_ary
        


    def gen_poem_nonyun(self, word_nonyun, itval_dict ):
        result_ary = {} 
        for (i,w_start) in enumerate(word_nonyun):
            pre_ary = self.viterbi(w_start,itval_backward = itval_dict[i])
            max_prob = 0;
            max_pw = None;
            for w in pre_ary:
                if pre_ary[w]['prob'] >= max_prob:
                    max_prob = pre_ary[w]['prob'];
                    max_pw = w;
            result_ary[i] = pre_ary[max_pw]['word'] + [max_pw] ;
        return result_ary
         

    def gen_poem(self, raw_str,slash=False):
        word_yun = [] 
        word_nonyun = []
        word_idx_list = []
        itval_dict_yun = {}
        itval_dict_nonyun = {}

        if not self._itval_slash:
            itval_val =[self._itval_backward for i in range(len(raw_str))]
        else:
            lenid  = self._length
            if self._itval_slash == 'lr':
                itval_val =[i%lenid for i in range(len(raw_str))]
            elif self._itval_slash == 'rl':
                itval_val =[(lenid-1)-i%lenid for i in range(len(raw_str))]
            else:
                assert 0
        for (i,word) in enumerate(raw_str):
            if i%2 !=0 and (self._length -1) != itval_val[i] :
                word_idx_list.append((len(word_yun),'yun'))
                itval_dict_yun.update({len(word_yun):itval_val[i]})
                word_yun.append(word)
            else:
                word_idx_list.append((len(word_nonyun),'nonyun'))
                itval_dict_nonyun.update({len(word_nonyun):itval_val[i]})
                word_nonyun.append(word)
        if len(itval_dict_yun) > 0:
            result_yun = self.gen_poem_yun(word_yun,itval_dict_yun) 
        result_nonyun = self.gen_poem_nonyun(word_nonyun,itval_dict_nonyun)
        result_list = []
        
        for (idx,typ) in word_idx_list:
            if typ == 'yun':
                result_list.append( result_yun[idx] )
            elif typ == 'nonyun':
                result_list.append( result_nonyun[idx] )
        return result_list
                    
    def main(self, input_str, print_out=True):
        self._print_out = print_out
        position_range = [ str(x) for x in range(1,8) ]
        parser = argparse.ArgumentParser( prog='' )
        parser.add_argument('words', help='the hidden words of each sentence.' )
        parser.add_argument('-l','--length', type=int, default=5
                            ,choices=[5,7] , help='number of words per sentence. (default: %(default)s)')
        parser.add_argument('-s','--seed', type=int , default=random.randint(0, sys.maxint) ,help='seed of random. ')
        parser.add_argument('-p','--position', default = '1'
                            ,choices=position_range+['lr','rl'], help='position of target words. ')

        args = parser.parse_args(input_str) 
        can_run= True
        self.print_out( "seed = %s"%(args.seed) )
        

        self._length = args.length
        if args.position in position_range :
            self._itval_backward = int(args.position)-1
            if self._itval_backward >= self._length:
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


