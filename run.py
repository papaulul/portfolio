import os 
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap 
from config import config 
from flask_moment import Moment
from datetime import datetime 
import pandas as pd 
import numpy as np
import pickle


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") 
bootstrap = Bootstrap(app)
moment= Moment()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/airbnb')
def airbnb():
    return render_template('airbnb_about.html')

@app.route('/airbnb/about')
def airbnb_about():
    return render_template('airbnb_about.html')

@app.route('/airbnb/analysis')
def airbnb_analysis():
    return render_template('airbnb_analysis.html')

@app.route('/airbnb/demo')
def airbnb_demo():
    # Dataframe setup
    df = pd.read_csv("static/Airbnb/demo.csv",index_col=0)
    num_of_Plus = np.random.randint(1,5)
    demo_index_non_plus = np.random.choice(df[df['isPlus']==False].index,5-num_of_Plus,replace=False)
    demo_index_plus = np.random.choice(df[df['isPlus']==True].index,num_of_Plus,replace=False)
    session["index"] = list(map(lambda x: int(x),sorted(np.concatenate([demo_index_non_plus,demo_index_plus]))))
    index = list(map(lambda x: int(x),sorted(np.concatenate([demo_index_non_plus,demo_index_plus]))))
    df['amenities'] = df['amenities'].apply(lambda x: str(x)[1:-1])
    df = df.loc[sorted(np.concatenate([demo_index_non_plus,demo_index_plus]))]
    df['answers'] = df['isPlus'] == df['Plus_pred']
        
    # Variables 
    model_answer = df['answers'].to_list()
    reveal = [False for _ in range(5)]
    right_wrong = [False for _ in range(5)]
    session["reveal"] = reveal
    session["num_right"] = right_wrong
    df = df.to_dict()

    return render_template('airbnb_demo.html', data = df, index = index, reveal = reveal, right_wrong = right_wrong,
                            model_answer = model_answer)

@app.route('/airbnb/demo1', methods=["POST"])
def airbnb_process():
    # Dataframe Setup
    df = pd.read_csv("static/Airbnb/demo.csv",index_col=0)
    index = session.get("index",None)
    df['amenities'] = df['amenities'].apply(lambda x: str(x)[1:-1])
    df = df.loc[index]
    df['answers'] = df['isPlus'] == df['Plus_pred']
    # Variables
    model_answer = df['answers'].to_list()
    reveal = session.get("reveal",None)
    right_wrong = session.get("num_right",None)
    for answers in range(5):
        try: 
            if request.form['submit_button_'+str(answers)] == "Plus Listing" or request.form['submit_button_'+str(answers)] == "Not Plus Listing":
                reveal[answers] = True
                try:
                    if df['isPlus'].loc[index[answers]] and request.form['submit_button_'+str(answers)] == "Plus Listing": 
                        right_wrong[answers] = True
                    elif df['isPlus'].loc[index[answers]] == False and request.form['submit_button_'+str(answers)] == "Not Plus Listing":
                        right_wrong[answers] = True
                except: 
                    pass
        except: 
                pass
    try:
        if request.form['show'] == 'show':
            reveal = [True for _ in range(5)]
    except:
        pass

    # Setting final variables
    df = df.to_dict()
    session['num_right'] = right_wrong
    session["reveal"] = reveal
    return render_template('airbnb_demo.html', data = df, index = index, reveal = reveal, right_wrong = right_wrong,
        model_answer = model_answer)
@app.route('/tripadvisor')
def tripadvisor():
    return render_template('tripadvisor_about.html')

@app.route('/tripadvisor/about')
def tripadvisor_about():
    return render_template('tripadvisor_about.html')

@app.route('/tripadvisor/analysis')
def tripadvisor_analysis():
    return render_template('tripadvisor_analysis.html')

@app.route('/tripadvisor/demo')
def tripadvisor_demo():
    amenities =  ['Banquet Room', 'Bar/Lounge', 'Breakfast Available','Breakfast included','Conference Facilities', 
    'Family Rooms', 'Free parking', 'Microwave', 'Outdoor pool', 'Pets Allowed ( Dog / Pet Friendly )', 'Pool', 
    'Public Wifi','Refrigerator in room', 'Restaurant', 'Room service', 'Self-Serve Laundry']
    return render_template('tripadvisor_demo.html', amenities = amenities, results={})

@app.route('/tripadvisor/demo1', methods=["POST"])
def tripadvisor_process():
    if request.method == 'POST':
        #Read in files
        review = pickle.load(open('static/files/review.sav','rb'))
        vectorizer = pickle.load(open('static/files/vectorizer.pkl','rb'))
        df = pd.read_pickle('static/files/review_final.pkl')
        hotel_info = pd.read_pickle('static/files/hotel_info.pkl')
        hotel = pickle.load(open('static/files/hotel.sav','rb'))
        ss = pickle.load(open('static/files/quant_scaled.sav','rb'))

        amenities =  ['Banquet Room', 'Bar/Lounge', 'Breakfast Available','Breakfast included','Conference Facilities',
         'Family Rooms', 'Free parking', 'Microwave', 'Outdoor pool', 'Pets Allowed ( Dog / Pet Friendly )', 'Pool',
          'Public Wifi','Refrigerator in room', 'Restaurant', 'Room service', 'Self-Serve Laundry']

        amenities_all =  ['Accessible rooms','Air conditioning', 'Airport transportation', 'Babysitting','Banquet Room',
         'Bar/Lounge', 'Breakfast Available','Breakfast included', 'Business Center with Internet Access',
         'Children Activities (Kid / Family Friendly)', 'Concierge','Conference Facilities', 'Dry Cleaning',
         'Electric vehicle charging station', 'Family Rooms','Fitness Center with Gym / Workout Room',
         'Free High Speed Internet (WiFi)', 'Free Internet', 'Free parking','Golf course', 'Heated pool', 
         'Hot Tub', 'Indoor pool', 'Kitchenette','Laundry Service', 'Meeting rooms', 'Microwave', 'Minibar',
         'Multilingual Staff', 'Non-smoking hotel', 'Non-smoking rooms','Outdoor pool', 'Paid Internet', 'Paid Wifi',
         'Pets Allowed ( Dog / Pet Friendly )', 'Pool', 'Public Wifi','Refrigerator in room', 'Restaurant', 
         'Room service', 'Sauna','Self-Serve Laundry', 'Shuttle Bus Service', 'Smoking rooms available','Spa', 
         'Suites', 'Tennis Court', 'Wheelchair access']
        # Read inputs
        demo = {}
        for amen in amenities_all:
            x = request.form.get(amen)
            if x != None:
                demo[amen] = True
            else:
                if int(sum(hotel_info[amen])/len(hotel_info)*100) >= 70:
                    demo[amen] = True
                elif int(sum(hotel_info[amen])/len(hotel_info)*100) <= 30:
                    demo[amen] = False
                else:
                    demo[amen] = False
        demo['num_amenities'] = sum(demo.values())
        review_input = request.form['rawtext']
        try:
            size_choice = request.form['Size']
            if size_choice.lower() == 'large':
                size_choice = 243.50
            elif size_choice.lower() == 'medium':
                size_choice = 147.70
            elif size_choice.lower() == 'small':
                size_choice = 100.00
        except: 
            size_choice = -1
        demo['num_rooms']  = size_choice        

        try:
            quality_choice = request.form['Quality']
            if quality_choice.lower() == 'great':
                quality_choice = 5
            elif quality_choice.lower() == 'good':
                quality_choice = 4 
            elif quality_choice.lower() == 'ok': 
                quality_choice = 3.5
        except: 
            quality_choice = -1

        demo['hotel_rating_hotel'] = quality_choice
        if quality_choice == -1 or size_choice == -1:
            results = {}
            results['No Hotels Exist'] = ["$0","$0",'/tripadvisor/demo']
        else:
            # Calculations  
            df_quant_cols = ['num_amenities', 'num_rooms', 'hotel_rating_hotel', 'Accessible rooms','Air conditioning', 'Airport transportation', 'Babysitting','Banquet Room', 'Bar/Lounge', 'Breakfast Available','Breakfast included', 'Business Center with Internet Access','Children Activities (Kid / Family Friendly)', 'Concierge','Conference Facilities', 'Dry Cleaning','Electric vehicle charging station', 'Family Rooms','Fitness Center with Gym / Workout Room','Free High Speed Internet (WiFi)', 'Free Internet', 'Free parking','Golf course', 'Heated pool', 'Hot Tub', 'Indoor pool', 'Kitchenette','Laundry Service', 'Meeting rooms', 'Microwave', 'Minibar','Multilingual Staff', 'Non-smoking hotel', 'Non-smoking rooms','Outdoor pool', 'Paid Internet', 'Paid Wifi','Pets Allowed ( Dog / Pet Friendly )', 'Pool', 'Public Wifi','Refrigerator in room', 'Restaurant', 'Room service', 'Sauna','Self-Serve Laundry', 'Shuttle Bus Service', 'Smoking rooms available','Spa', 'Suites', 'Tennis Court', 'Wheelchair access']
            to_pred = pd.DataFrame.from_dict(demo, orient= 'index').transpose()[df_quant_cols]
            to_pred = pd.DataFrame(ss.transform(to_pred),index = to_pred.index, columns = to_pred.columns)
            hotel_predict = hotel.predict(to_pred)[0]
            review_predict = review.predict(vectorizer.transform([review_input]).todense())[0]
            results = {}
            for x in df[(df['hotel_pred'] == hotel_predict) & (df['review_preds'] == review_predict)]['hotel_name'].unique():
                url = hotel_info[hotel_info['hotel_name'] == x]['url'].values[0]
                low =  "$"+str(hotel_info[hotel_info['hotel_name'] == x]['low_price'].values[0])[:-2]
                high =  "$"+str(hotel_info[hotel_info['hotel_name'] == x]['high_price'].values[0])[:-2]
                results[x] = [low, high, url]
                if len(results) > 10:
                    break
            if len(results) == 0:
                results['No Hotels Exist'] = ["$0","$0",'/tripadvisor/demo']
        return render_template('tripadvisor_demo.html', results=results, amenities = amenities, demo = demo)
    else:
        return render_template('tripadvisor_demo.html')

@app.route('/aboutme')
def aboutme():
    return render_template(('aboutme.html'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ =='__main__':
    app.run(host="0.0.0.0", port=80)