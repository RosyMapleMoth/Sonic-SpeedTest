import os
import time 
from time import gmtime, strftime
from flask import Flask, flash, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
import psycopg2
import requests
import json

UPLOAD_FOLDER = '/home/dev/DisControl/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

MEGABYTE = (2 ** 10) ** 2




app = Flask(__name__)
app.config["UPLOAD_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["UPLOAD_PATH"] = "image_uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = None
# Max number of fields in a multi part form (I don't send more than one file)
# app.config['MAX_FORM_PARTS'] = ...
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * MEGABYTE

with open("secreats.json") as f:
    secrets_json = json.load(f)
    app.config['MAX_CONTENT_LENGTH'] = None
    
    app.config["DATABASE_HOST"] = secrets_json["database_host"]
    app.config["DATABASE_NAME"] = secrets_json["database_name"]
    app.config["DATABASE_USER"] = secrets_json["database_user"]
    app.config["DATABASE_PASSWORD"] = secrets_json["database_password"]
    app.config["DISCORD_TOKEN"] = secrets_json["discord_token"]




def get_db_connection():
    conn = psycopg2.connect(
        host=app.config["DATABASE_HOST"],
        database=app.config["DATABASE_NAME"],
        user=app.config["DATABASE_USER"],
        password=app.config["DATABASE_PASSWORD"])
    return conn


@app.route("/init_session", methods=['GET'])
def init_session():
    if(request.method == 'GET'): 
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('Select * FROM users WHERE name = \'' + request.form["username"] + '\';')
        user = cur.fetchone()
        message_sent = False
        if (user == None):
            cur.close()
            conn.close()
            return "User not found", 400
        try:
            send_discord_message(msg=f"Speed test initaitated for " + user[3])
            message_sent = True
        except Exception as e:
            print(e)
            return "Error sending message", 500
            
        data = { 
            "message_sent" : message_sent, 
        } 
        cur.close()
        conn.close()
        return jsonify(data) 


@app.route("/error_with_test", methods=["POST"])
def error_with_test():
    if(request.method == 'POST'): 
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('Select * FROM users WHERE name = \'' + request.form["username"] + '\';')
        user = cur.fetchone()
        message_sent = False

        if (user == None):
            cur.close()
            conn.close()
            return "User not found", 400

        try:
            send_discord_message(msg=f"Error with speed test app, please check laptop " + user[3])
            message_sent = True
        except Exception as e:
            print(e)
            
        data = { 
            "message_sent" : message_sent, 
        } 

        cur.close()
        conn.close()
        return  


@app.route("/", methods=["GET"])
def home():
    return 'Index Page'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["UPLOAD_EXTENSIONS"]

# TODO allow for uploads that do not include all 3 images
# TODO migrate from userID to APIKey 
@app.route("/upload_speeds", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        conn = get_db_connection()
        
        # check if all images exist
        if 'img_1' not in request.files:
            conn.close()
            return "missing first image", 400
        if 'img_2' not in request.files:
            conn.close()
            return "missing secound image", 400
        if 'img_3' not in request.files:
            conn.close()
            return "missing third image", 400
        
        # if user doesn't exist return error
        

        cur = conn.cursor()
        cur.execute('Select * FROM users WHERE name = \'' + request.form["username"] + '\';')
        user = cur.fetchone()
        
        file_one = request.files['img_1']
        file_two = request.files['img_2']
        file_three = request.files['img_3']

        if (user == None):
            conn.close()
            return "User not found", 400


        if file_one and file_two and file_three and allowed_file(file_one.filename) and allowed_file(file_two.filename) and allowed_file(file_three.filename):
            file_name_one = secure_filename(file_one.filename)
            file_name_two = secure_filename(file_two.filename)
            file_name_three = secure_filename(file_three.filename)

            file_name_prfix = request.form["username"] + ' ' + strftime("%d %b %Y %H:%M:%S", gmtime()) 

            print
            file_one.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name_prfix + ' ' + file_name_one))
            file_two.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name_prfix + ' ' + file_name_two))
            file_three.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name_prfix + ' ' + file_name_three))

            cur.execute('INSERT INTO sessions(user_id, image_One, image_Two, image_Three, speed)'
                        'VALUES (%s,%s,%s,%s,%s);' % 
                        (user[2],
                         '\'' + file_name_prfix + " sonic.png\'",
                         '\'' + file_name_prfix + " broadband.png\'",
                         '\'' + file_name_prfix + " pcmag.png\'",
                         request.form["speed"]))
            send_discord_message(msg=f"Speed test results {request.form["speed"]}" + user[3], 
                                 file1=app.config['UPLOAD_FOLDER']+'/'+file_name_prfix + " pcmag.png",
                                 file2=app.config['UPLOAD_FOLDER']+'/'+file_name_prfix + " broadband.png",
                                 file3=app.config['UPLOAD_FOLDER']+'/'+file_name_prfix + " sonic.png")

            conn.commit()
            cur.close()
            conn.close()

            return "Speed Test uploaded", 200


# stolen from https://stackoverflow.com/questions/68499998/how-can-i-send-a-picture-with-the-discord-api-and-python-requests
def send_discord_message(msg: str, file1: str = "", file2: str = "", file3: str = "", channel_id: str = '805364550755942422'):
    """
    :param msg: the message you want to send
    :param channel_id: channel id where you want to send your message to
    :return: None
    """

    # set all the required headers to make a request to discord end point api
    headers = {
        'Authorization': f'Bot {app.config["DISCORD_TOKEN"]}',
    }

    files = {}
    if (file1 != ""):
        files['FileOne'] = (file1, open(file1, 'rb'))
    if (file2 != ""):
        files['FileTwo'] = (file2, open(file2, 'rb'))
    if (file3 != ""):
        files['FileThree'] = (file3, open(file3, 'rb'))
    payload = {
        "content":"%s" % msg
    }
    # convert this dict in to json object
    message = json.dumps({'content': msg})

    # make a post request to discord end point api with all the data we've set up above
    r = requests.post(f'https://discordapp.com/api/channels/{channel_id}/messages', headers=headers, data=payload, files=files)

    if r.status_code != 200:
        print(f'Failed to send message, returned status code: {r.status_code}')
