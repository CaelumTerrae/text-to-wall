from flask import Flask, request, redirect, render_template, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3 

app = Flask(__name__)

def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    sql_create_images_table = """ CREATE TABLE IF NOT EXISTS images (
                                    id integer PRIMARY KEY,
                                    url text
                                ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_images_table)
    except sqlite3.Error as e:
        print(e)

def add_image(conn, imageURL):
    sql = ''' INSERT INTO images(url)
              VALUES(?) '''
    c = conn.cursor()
    c.execute(sql, imageURL)
    conn.commit()
    return c.lastrowid

def get_recent(conn):
    sql = ''' SELECT *
              FROM images
              WHERE id=(SELECT MAX(id) FROM images)
            '''
    c = conn.cursor()
    c.execute(sql)
    row = c.fetchone()
    return row

conn = sqlite3.connect("images.db", check_same_thread=False)

if conn is not None:
    create_table(conn)



@app.route("/sms", methods=['GET', 'POST'])
def mms_reply():
    """Respond to incoming image texts"""
    imageURL = request.values.get('MediaUrl0', None)
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    if imageURL is None:
        resp.message("Please attach an image you want to see on Daran and Gavin's wall!")
    else:
        resp.message("Thank you for sending this image! It will promptly be displayed on Daran and Gavin's living room wall.")
        add_image(conn, [imageURL])
    return str(resp)

@app.route("/recent", methods=['GET'])
def recent():
    url = get_recent(conn)
    return jsonify(url="no url" if url is None else str(url[1]))

@app.route("/wall", methods=['GET'])
def wall():
    return render_template("wall.html")

if __name__ == "__main__":
    app.run(debug=True)
