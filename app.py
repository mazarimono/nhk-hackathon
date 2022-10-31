from flask import Flask
import geopandas as gpd
from geopy import distance
import pandas as pd
import random

app = Flask(__name__)

@app.route('/')
def base_page():
    return '''NHK Hackthon 2022-10-23:  \n
        we are group 11 !!!
'''

# /api/version/やること
# route　を明確にAPIと分かるようにしておく

@app.route('/api/v0/geodata/hinanjo/<float:lat>/<float:lon>')
def search_hinanjo_and_return(lat, lon):
    '''
    lat: float
        緯度: y
    lon: float
        経度: x
    '''
    position_now = tuple([lat, lon])
    hinanjo_path = 'data/all_hinanjo.geojson'
    df = gpd.read_file(hinanjo_path)
    df['distance'] = df['geometry'].map(lambda x: distance.distance(([x.y, x.x]), position_now))
    df = df.sort_values('distance')
    nearest_data = df.iloc[:5, :] # 5個にする
    nearest_geometry = [str(pos) for pos in nearest_data['geometry'].values]
    nearest_meisho = list(nearest_data['名称'].values)
    nearest_distance = [k.km for k in nearest_data['distance'].values]
    nearest_dict = {
        'geometry': nearest_geometry,
        'meisho': nearest_meisho,
        'distance': nearest_distance
    }
    return nearest_dict


@app.route('/api/v0/news/random_news')
def return_randomnews():
    df = pd.read_csv('data/nhk-news.csv')
    random_int = random.randrange(0, len(df))
    rand_df = df.iloc[random_int, :]
    news_title = rand_df.loc['タイトル']
    news_url = rand_df.loc['URL']
    return {
        'news_title': news_title,
        'news_url': news_url
    }


if __name__ == "__main__":
    app.run(debug=True)
