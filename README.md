## 簡介

本程式可以自動產生藏頭詩。

本程式以Ngram為語言模型，先從兩萬首全唐詩中算出Ngram的統計數值，再用Viterbi演算法拼湊出藏頭詩中的每個字，
得出的藏頭詩，看起來很像詩詞但語意未必通順。

##用法：

執行本程式需安裝python 2.7版本。

到終端機輸入以下指令啟動本程式：

```
> python AcrosticPoem.py
```

接著，輸入想要藏頭的字，例如：

```
> 藏頭詩自動產生器
```

則會產生出藏頭詩：

```
藏衱戎河泯 
頭夜浮梁買 
詩贈汨羅幃 
自將奈何之
動盈虛無邊
產遺鴛坡訇
生不重問客
器動如衫絹
```

## 參數設定：

```
> words [-h] [-l {5,7}] [-s SEED] [-v {simple,medium,hard}]
        [-p {1,2,3,4,5,6,lr,rl}]
```

###必要參數:
    
  words                 想要藏頭的字  

###其他參數 :

  -h, --help               顯示help 

  -l {5,7},                每句幾個字（五言或七言）  

  -s SEED,                 隨機種子

  -v {simple,medium,hard}, 用詞深淺度（若選擇hard則會出現罕見字）

  -p {1,2,3,4,5,6,lr,rl},  藏字的位置（第幾個字，或左右斜下）  


##範例：

例如，要產生七言的藏頭詩，藏在第三句，方法如下：

```
> 藏頭詩自動產生器 -l 7 -p 3

中行藏海山人人
時人頭花已自奔
君來詩酒聲入天
歸不自朝日無恩
鐘聲動日應不似
山陰產海月沉沉
竟不生欲何事空
禹廟器道今何紛
```

##後續工作：

本程式所使用的演算法極為簡單，但產生出的藏頭詩語意不通順，
若要產生語意通順的藏頭詩，可參考以下兩篇研究論文，用統計式機器翻譯的演算法。但此演算法較為複雜，目前小弟還在研究當中。

Ming Zhou, Long Jiang, Jing He: Generating Chinese Couplets and Quatrain Using a Statistical Approach. PACLIC 2009: 43-52

Long Jiang, Ming Zhou: Generating Chinese Couplets using a Statistical MT Approach. COLING 2008: 377-384


另外，為了讓一般人也可以使用，藏頭詩產生器目前還需要做成網頁版的。
