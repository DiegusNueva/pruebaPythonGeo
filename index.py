from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
import geopy.distance

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/result', methods=['POST'])
def result():
    geo = Nominatim(user_agent="MyApp")

    # Información relativa a los lugares
    nombreLugar = request.form["nombreLugar"]
    nombreLugar2 = request.form["nombreLugar2"]
    loc = geo.geocode(nombreLugar)
    loc2 = geo.geocode(nombreLugar2)

    # Cálculo de la distancia entre dos ciudades empleando su latitud y su longitud

    ## Necesito sus coordenadas para calcular su distancia

    coord_loc = (loc.latitude, loc.longitude)
    coord_loc2 = (loc2.latitude, loc2.longitude)

    distancia = geopy.distance.distance(coord_loc, coord_loc2)

    return render_template('result.html', address=loc.address, lat=loc.latitude, long=loc.longitude, address2=loc2.address, lat2=loc2.latitude, long2=loc2.longitude, distancia=distancia)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombreLugar = request.form["nombreLugar"]
        geo = Nominatim(user_agent="MyApp")
        loc = geo.geocode(nombreLugar)

        return render_template('result.html', address=loc.address, lat=loc.latitude, long=loc.longitude)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
