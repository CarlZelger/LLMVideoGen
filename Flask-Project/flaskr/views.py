from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .main import addQuestion, addTitleToVideo, getOptTitle, getSuggestion, getTopic, generateVideo, applySuggestion

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return redirect(url_for('main.input'))

 # a simple page that says hello
@bp.route('/hello')
def hello():
    # return render_template('page.html')
    return 'Hello, World!'

@bp.route('/test')
def test():
    return "test"

@bp.route('/html')
def html():
    return render_template('page.html')

@bp.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    # Process the data here (store it, send it, manipulate it, etc.)
    return redirect(url_for('thank_you'))

@bp.route('/thank_you')
def thank_you():
    return 'Thank you for submitting the form!'

@bp.route('/adder')
def adder():
    print('adder')
    return render_template('adder.html')

@bp.route('/add', methods=['POST'])
def add():
    number = request.json['number']
    new_number = number + 1
    return jsonify(new_number=new_number)

@bp.route('/sub', methods=['POST'])
def sub():
    number = request.json['number']
    new_number = number - 1
    return jsonify(new_number=new_number)

@bp.route('/input')
def input():
    return render_template('input.html')

@bp.route('/api', methods=['POST'])
def api():
    topic = request.form['q']
    # print(f"The topic is: {topic}")
    generateVideo(topic, 2)
    return redirect(url_for('main.video'))

# @bp.route('/video', methods=['GET'])
# def video():
#     video_url = request.args.get('video_url')
#     return render_template('videoPlayer.html', video_url=video_url)

@bp.route('/video')
def video():
    video_url = url_for('static',filename='videos/video.mp4')
    optTitle = getOptTitle()
    topic = getTopic()
    sug = getSuggestion()
    return render_template('videoPlayer.html', video_url=video_url, topic=topic,optTitle = optTitle, suggestion= sug )

@bp.route('/addQuestiones', methods=['POST'])
def addQuestiones():
    video_url = "new URL"
    addQuestion()
    return jsonify(new_url=video_url)

@bp.route('/addTitle', methods=['POST'])
def addTitle():
    addTitleToVideo()
    return jsonify()

@bp.route('/addSug', methods=['POST'])
def addSug():
    applySuggestion()
    sug = getSuggestion()
    return jsonify(new_sug=sug)