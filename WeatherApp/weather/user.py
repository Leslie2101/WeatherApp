from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from .models import Note
from .import db
import json

user = Blueprint("user", __name__)


@user.route("/", methods=["POST", "GET"])
def index():
    
    # Enter your API key here
    api_key = {YOUR API KEY}
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    convert = {'imperial' : 'F', 'metric': 'C'}
    unit = 'metric'
    if request.method == 'POST':
        # base_url variable to store url
        if request.form.get('action', False) == 'submit':
            city_name = request.form.get("cityinput") 

            complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=" + unit
            r = requests.get(complete_url).json()
            cod = r["cod"]
            if int(cod) == 200:
                newnote = Note(cityname = city_name)
                db.session.add(newnote)
                db.session.commit()
                flash("New data added!", category="success")
            else:
                flash("Data not found. Please try again!", category="error")
        elif request.form.get('action', False) == 'apply':
            unit = request.form.get("units") 
        else:
            unit = request.form.get("units") 
            print('hello')


    weather_data = []
    cities = Note.query.all()
    for city in cities:
        complete_url = base_url + "appid=" + api_key + "&q=" + city.cityname + "&units=" + unit
        r = requests.get(complete_url).json()
        weather = {
            "id": city.id,
            "city": r["name"],
            "country" : r['sys']['country'],
            "curtemp" : r['main']['temp'],
            "feellike" : r['main']['feels_like'],
            "maxtemp" : r['main']['temp_max'],
            "mintemp" : r['main']['temp_min'],
            "description": r['weather'][0]['description'],
            "icon" : r['weather'][0]['icon'],
            "unit" : convert[unit]
        }
        weather_data.append(weather)
    return render_template("index.html", cities_data = weather_data)

@user.route("/delete-note", methods = ["GET", "POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["note_id"]
    result = Note.query.get(note_id)
    db.session.delete(result)
    db.session.commit()
    return jsonify({'code': 200})
