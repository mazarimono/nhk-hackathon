from flask import Flask
import geopandas as gpd
from geopy import distance

app = Flask(__name__)

@app.route('/')
def base_page():
    return '''NHK Hackthon 2022-10-23 \n
        we are group 11 !!!
'''


@app.route('/hinanjo/<float:lat>/<float:lon>')
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


if __name__ == "__main__":
    app.run(debug=True)