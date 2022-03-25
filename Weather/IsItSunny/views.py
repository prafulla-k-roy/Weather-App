from django.shortcuts import render
from newsapi import NewsApiClient
import urllib.request
import json


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='
                                        + city + '&units=metric&appid=703dada22fb106981d1635efeee56995').read()
        list_of_data = json.loads(source)

        data = {
            "country_code" : str(list_of_data['sys']['country']),
            "coordinate" : str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temp" : str(list_of_data['main']['temp']) + '°C',
            "pressure" : str(list_of_data['main']['pressure']) + 'psi',
            "humidity" : str(list_of_data['main']['humidity']) + '%',
            "main" : str(list_of_data['weather'][0]['main']),
            "description" : str(list_of_data['weather'][0]['description']),
            "icon" : list_of_data['weather'][0]['icon']
        }


    else:
        data = {}

    return render(request, "IsItSunny/index.html", data)

def news(request):
    if request.method == 'POST':
        ctry = request.POST['Nation']
    else:
        ctry = 'in'
    newsApi = NewsApiClient(api_key='ab34a95470264d829023ed300c9575fa')
    headlines = newsApi.get_top_headlines(country = ctry)
    articles = headlines['articles']
    description = []
    news = []
    image = []
    url = []

    for i in range(len(articles)):
        article = articles[i]
        description.append(article['description'])
        news.append(article['title'])
        image.append(article['urlToImage'])
        url.append(article['url'])

    mylist = zip(news, description, image, url)

    return render(request, "IsItSunny/news.html", context={"mylist": mylist})
