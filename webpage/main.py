from flask import Flask, render_template, request, jsonify
import flask
from nltk.util import pr
from flask_cors import CORS, cross_origin
# from data_preprocess import preprocessed_synop
import requests
import time
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def hello_world():
    return render_template('movie-tags-page.html')

# check if application is running
@app.route("/api/check-status", methods=['GET'])
def check_status():
    return jsonify({"status": "success"})




@app.route('/', methods=['POST'])
def submit():
    my_data = request.form['plotinput']
    tags = get_synopsis(my_data)
    # tags = predicttags(plotdata)
    return render_template('movie-tags-page.html', tags=tags)

    # 'You entered: {}'.format(tags)

@app.route('/get-synopsis', methods=['POST'])
def synopsis():
    my_data = request.data
    tags = get_synopsis(my_data)
    return tags


def get_synopsis(my_data): 
    # run api request to get cleaned synops
    clean_res = requests.post('http://preprocessor:3111/api/preprocess-data/MOVIES', json={"data":my_data})
    plotdata = ''
    if clean_res.ok:
        plotdata = clean_res.json()['data']
    # plotdata = ''.join(str(cleaned_synopsis))

    # run api request to get predicted tags
    tags_res = requests.post('http://prediction:3211/api/predict-tags/tags', json={"data":plotdata})
    tags = ''
    if tags_res.ok:
        tags = tags_res.json()['data']
    
    return tags

if __name__ == "__main__":
    print("updating data")
    r = requests.get('http://preprocessor:3111/api/clean-data/MOVIES')
    print("data has been updated")
    app.run(host='0.0.0.0', port=3311,debug=True, threaded=True)
