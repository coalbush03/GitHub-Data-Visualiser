import requests
from plotly.graph_objs import bar
from plotly import offline
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_language_plot(lang):
    url=f'https://api.github.com/search/repositories?q=language:{lang}&sort=stars' #URL python repositories data
    #posortowane iloscia gwiazdek
    headers={'Accept': 'application/vnd.github.v3+json'}
    r=requests.get(url, headers=headers) #wywolanie
    if r.status_code!=200: #sprawdzenie czy dane sie wczytaly
      print(f"error while loading {lang} data")
    response=r.json() #response z danych json jako slownik

    ##klucze
    #for data in response.keys():
    #    print(data)

    repositories=response['items'] 

    ##klucze
    # for data in repositories[0].keys():
    #     print(data)
    links,stars,labels= [],[],[] #tablice zapisujace interesujace nas dane

    i=1
    for item in repositories:
      name=i
      url=item['html_url']
      link=f"<a href='{url}'>{name}</a>"  #link w nazwie - wyswietlany na osi x jako pozycje w top 30
      links.append(link) #dodanie nazwy ktora odsyala nas do repo
      i+=1
      stars.append(item['stargazers_count']) #gwiazdki
      name='Name: '+item['name']
      owner='Owner: '+item['owner']['login']
      description='Description: '+item['description']
      if len(description)>70:
        description=description[:70]+'...' #zapobiegniecie zbyt dlugiemu opisowi
      label=f"{name}<br />{owner}<br />{description}" #label do hovera
      labels.append(label) #opis repo

    #WIZUALIZACJA 
    #kolory dla konkretnych jezykow
    if lang == 'python':
      colors=['#4584B6','#FFDE57']
    elif lang == 'php':
      colors=['#4F5D95','#8993BE']
    elif lang == 'javascript':
      colors=['#F0DB4F','#323330']
    elif lang == 'c++':
      colors=['#00599C','#004482']
    else:
      colors=['#FFFFFF','#000000']

    data= [{'type':'bar','x':links,'y':stars,
            'hovertext':labels,'marker':{'color':colors[0],'line':{'width':2,'color':colors[1]}},
            'hoverinfo': 'x,y,text',
            'marker':{'color':colors[0],'line':{'width':1,'color':colors[1]}}, #kolory wg jezykow
            'opacity':0.9}]
    layout={#'title':f'Most popular {lang} repositories on GitHub','titlefont':{'size':20},
            #'xaxis':{'title':'REPOSITORY NAME','titlefont':{'size':14},
            #'yaxis':{'title':'STARS','titlefont':{'size':14}},
            #}}
            #layout konkretnych subplotow nie jest koniecznyy - pozostalosc po wersji z pojedynczym wykresem
    }
    figure={'data':data,'layout':layout}

    return figure

#utworzenie wykresow
py_fig=generate_language_plot('python')
php_fig=generate_language_plot('php')
js_fig=generate_language_plot('javascript')
cpp_fig=generate_language_plot('c++')

#okno 2x2
fig=make_subplots(rows=2,cols=2,subplot_titles=('Python','PHP','JavaScript','C++'))

#dodanie wykresow do okna w odpowiednie pozycje
fig.add_trace(py_fig['data'][0],row=1,col=1)
fig.add_trace(php_fig['data'][0],row=1,col=2)
fig.add_trace(js_fig['data'][0],row=2,col=1)
fig.add_trace(cpp_fig['data'][0],row=2,col=2)

#layout calego okna
fig.update_layout(title_text='30 Most popular repositories on GitHub for these 4 languages (based on number of stars)',titlefont={'size':25},showlegend=False,
                  hoverlabel={'bgcolor':'#FFF','font':{'size':15}})
fig.update_layout(paper_bgcolor="#D9E5D6",plot_bgcolor="#828E82")

offline.plot(fig,filename='languages.html')