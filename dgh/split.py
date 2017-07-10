import pandas as pd

def readexcel(url):
    df=pd.read_excel(url,sheetname=0,header=2)
    df=df.dropna(axis=0,how='any')
    df.columns = ['id', 'company_name', 'num', 'listed', 'others', 'sub_name', 'cat1', 'cat2']
    return df
    pass

def split(df):
    df_split=pd.DataFrame(data=None,columns=['id','name','subname','cat1','cat2'])
    for i in df.index:
        subname=df.loc[i,'sub_name']
        subname_set=subname.split(',')
        print(i)
        for j in subname_set:
            new={'id':df.loc[i,'id'],
                 'name':df.loc[i,'company_name'],
                 'subname':j,
                 'cat1':df.loc[i,'cat1'],
                 'cat2':df.loc[i,'cat2']
                 }
            df_split=df_split.append(new,ignore_index=True)
    return df_split
    pass

def writeexcel(df,url):
    df.columns=['代码',	'名称','子公司','证监会行业(2012)','东财行业']
    write = pd.ExcelWriter(url)
    df.to_excel(write, 'splite_sheet', index=False)
    write.save()

if __name__=="__main__":
    url='C:/Users/zhongtengyue/Desktop/PYTHON/nlp/dgh/t1/'
    filename='work2.xlsx'
    filename2='result2.xlsx'

    df=readexcel(url+filename)

    df_split=split(df)

    writeexcel(df_split,url+filename2)

    pass