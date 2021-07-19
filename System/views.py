from django.shortcuts import render
import pandas as pd
# Create your views here.



def index(request):
    return render(request,'System/cards.html')

def pbr(request):

    data = pd.read_csv("electronics.csv")

    data1 = data.head(10)

    rating = data1['rating']

    df_rating=pd.DataFrame({'Number of Rating':data.groupby('item_id').count()['rating'], 'Mean Rating':data.groupby('item_id').mean()['rating']})

    df_filtered=df_rating[df_rating['Number of Rating']>df_rating['Number of Rating'].quantile(q=0.9)]

    def product_score(x):
        v=x['Number of Rating']
        m=df_rating['Number of Rating'].quantile(q=0.9)
        R=x['Mean Rating']
        C=df_rating['Mean Rating'].mean()
        return ((R*v)/(v+m))+((C*m)/(v+m))

    df_filtered['score']=df_filtered.apply(product_score, axis=1)

    df_highscore=df_filtered.sort_values(by='score', ascending=False).head(10)

    items  = df_highscore.index

    nrating = df_highscore["Number of Rating"].apply(lambda x: round(x,2))
    mrating = df_highscore["Mean Rating"].apply(lambda x: round(x,2))
    score = df_highscore["score"].apply(lambda x: round(x,2))

    l = []
    for i in df_highscore.index:
        a  = data[data['item_id']==i]['category'].head(1)
        s  = str(a)
        s=s.split('  ')
        s=s[2].split('\n')
        l.append(s[0])

    t = zip(items,nrating,mrating,score,l)

    return render(request,'System/pbr.html',{"top10" : t})