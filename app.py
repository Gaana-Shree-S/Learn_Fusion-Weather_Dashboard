from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from configparser import ConfigParser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = "cd88defdadc4239d6d8d893b04c99b08"  
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        sample = result.json()
        city = sample['name']
        country = sample['sys']['country']
        temp_kelvin = sample['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        weather_desc = sample['weather'][0]['main']
        return {'city': city, 'country': country, 'temp_celsius': temp_celsius, 'weather_desc': weather_desc}
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        weather = get_weather(city)
        if weather:
            return render_template('index.html', weather=weather)
        else:
            flash("Cannot find the city {}".format(city))
            return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
