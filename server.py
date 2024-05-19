import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json', 'r') as comps:
        data = json.load(comps)
        for competition in data['competitions']:
            competition['date'] = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        return data['competitions']


def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    if config:
        app.config.update(config)
    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        club = next((club for club in clubs if club['email'] == request.form['email']), None)
        if club is None:
            flash("Sorry, that email wasn't found.")
            return redirect(url_for('index'))
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs, current_datetime=datetime.now())

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            if foundCompetition['date'] < datetime.now():
                flash("This competition has already taken place.")
                return redirect(url_for('index'))
            return render_template('booking.html', club=foundClub, competition=foundCompetition,
                                   current_datetime=datetime.now())
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=foundClub, competitions=competitions, clubs=clubs,
                                   current_datetime=datetime.now())

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
        club = next((c for c in clubs if c['name'] == request.form['club']), None)
        placesRequired = int(request.form['places'])

        if competition and club:
            if not (1 <= placesRequired <= 12):
                flash('You can only reserve between 1 and 12 places.')
            elif placesRequired > int(club['points']):
                flash("You cannot book more places than your available points.")
            else:
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                club['points'] = int(club['points']) - placesRequired
                flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs, current_datetime=datetime.now())
        else:
            flash("Something went wrong-please try again.")
            return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs, current_datetime=datetime.now())

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app