#llamamos al framework (lo tenemos que tener instalado en nuestro sistema operativo)
#render_template es el medoto que nos ayuda a llamar a los html's del proyecto
from flask import Flask, render_template, request
from geopy.geocoders import Nominatim

#inicializamos Flask (le decimos a Flask que este es el archivo principal. este archivo arranca la app)
#esta variable se utiliza para crear las rutas del servidor, las URL's
app = Flask(__name__)

#para crear rutas se utilizan decoradores. para la pagina principal seria asi:
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/result', methods=['POST'])
def result():

    geo = Nominatim(user_agent="MyApp")

    nombreLugar = request.form["nombreLugar"]
    loc = geo.geocode(nombreLugar)

    return render_template('result.html', address=loc.address, lat=loc.latitude, long=loc.longitude)



@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':    
    app.run(debug=True)


