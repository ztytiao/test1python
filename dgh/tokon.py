import pandas as pd
import os
import jieba
import jieba.posseg as pseg
import thulac

def getfilename(url):
    '''获取文件夹下所有文件名list'''
    a=[]
    for root, dirs, files in os.walk(url):
        #print(root) # 当前目录路径  
        #print(dirs) # 当前路径下所有子目录  
        a.append(files)#print(files)#
    return a[0]

def readexcel(url,filename):
    '''读取所有文件，并进行合并'''
    df_all=pd.DataFrame()
    for i in filename:
        df=pd.read_excel(url+i,sheetname=0,header=0)
        df_all=pd.concat([df_all,df],axis=0)
    df_all.index = range(df_all.shape[0])
    return df_all
    pass

def combine(df_all):
    '''对于相同行业属性的，进行titles的合并'''
    df_new=pd.DataFrame(data=None,index=df_all['行业'].unique().tolist(),columns=['titles'])
    df_new['titles']=''
    for i in df_all.index:
        df_new.loc[df_all.loc[i,'行业'],'titles']=df_new.loc[df_all.loc[i,'行业'],'titles']+df_all.loc[i,'标题']
    return df_new
    pass

def jiebasplit(df_new):
    '''结巴分词，并输出词频'''
    df_re=pd.DataFrame()
    for i in df_new.index:
        b=jieba.cut(df_new.loc[i,'titles'])
        subcor = []
        for j in b:
            subcor.append(j)
        df1 = pd.DataFrame(subcor, columns=['No.'])
        s1=df1.groupby('No.')['No.'].count()
        df_temp=pd.DataFrame(s1)
        df_temp['Cat']=i
        df_re=pd.concat([df_re,df_temp],axis=0)
    df_re['Term']=df_re.index
    df_re.index=range(df_re.shape[0])
    return df_re
    pass

def thulacsplit(df_new):
    '''清华thulac分词'''
    thu1=thulac.thulac(seg_only=True)
    df_re = pd.DataFrame()
    for i in df_new.index:
        b=thu1.cut(df_new.loc[i,'titles'],text=True).split(' ')
        df1=pd.DataFrame(b,columns=['No.'])
        s1 = df1.groupby('No.')['No.'].count()
        df_temp = pd.DataFrame(s1)
        df_temp['Cat'] = i
        df_re = pd.concat([df_re, df_temp], axis=0)
    df_re['Term']=df_re.index
    df_re.index=range(df_re.shape[0])
    return df_re
    pass

def writeexcel(df,url,index=True):
    #
    write = pd.ExcelWriter(url)
    df.to_excel(write, 'split_sheet',index=index)
    write.save()

def delstopkey(list_stop,df):
    list_raw=df['Term'].tolist()
    list_deleted=list(set(list_raw)-set(list_stop))
    return df[df['Term'].isin(list_deleted)]

def readstopkey(url):
    list_stop = pd.read_csv(url2, header=None)
    list_stop.columns=['key']
    return list_stop['key'].tolist()

def addnewdict(urldict,dictname):
    for i in dictname:
        jieba.load_userdict(urldict+i)
    pass


if __name__=="__main__":
    url='C:/Users/zhongtengyue/Desktop/PYTHON/nlp/dgh/t2/行业研究报告/'
    url2 = 'C:/Users/zhongtengyue/Desktop/PYTHON/nlp/share/stopkey.txt'#stop key
    #urldict='C:/Users/zhongtengyue/Desktop/PYTHON/nlp/share/THUOCL/'
    #dictname=getfilename(urldict)
    #addnewdict(urldict,dictname)

    filename=getfilename(url+'content/')

    df_all=readexcel(url+'content/',filename)
    df_new=combine(df_all)
    df_re=jiebasplit(df_new)
    df_re2=thulacsplit(df_new)
    list_stop=readstopkey(url2)

    df_nostop=delstopkey(list_stop,df_re2)

    writeexcel(df_re,url+'re.xlsx',False)

    pass