from flask import Flask, render_template, request, redirect, session
import psycopg2
from werkzeug.utils import secure_filename
import boto3

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'fsdjfgsdkfgsafjah'

# Access Key ID:
# AKIA4FOGJIMT6HHKLXRC
# Secret Access Key:
# 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

# PostGre - rdsforgutta
# Master User Name : postgres
# yguttasecuritygroupforrds
# Master Username : postgres
# Password for database : JSQQ5ZZOg0QNYfMSBgNM
# rdsforgutta.cbktdobfilfl.us-east-1.rds.amazonaws.com
# yguttatestingproject
# gutta_database

# Account
# 836323853095
# KMS key ID
# 9149420f-485f-42be-9c8d-d0a31bb741a1

# Tablename accounts


# INSERT INTO accounts (emailone, emailtwo, emailthree, emailfour, emailfive, filename) VALUES(
# 'gutta.yashna@gmail.com','gutta.yashna@gmail.com', 'gutta.yashna@gmail.com', 'gutta.yashna@gmail.com',
# 'gutta.yashna@gmail.com', '1.jpg');

conn = psycopg2.connect(
    host="rdsforgutta.cbktdobfilfl.us-east-1.rds.amazonaws.com",
    database="gutta_database",
    user="postgres",
    password="JSQQ5ZZOg0QNYfMSBgNM")


def get_s3():
    s3 = boto3.client('s3',
                      aws_access_key_id='AKIA4FOGJIMT6HHKLXRC',
                      aws_secret_access_key='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',
                      )
    return s3


@app.route('/', methods=['POST', 'GET'])
def logins():
    if request.method == 'POST':
        name = request.form.get('user')
        password = request.form.get('pass')
        if name == 'yashnagutta27@gmail.com' and password == 'gutta':
            session['user'] = 'yashnagutta27@gmail.com'
            return redirect('/home')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def homes():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        enteredemail = request.form.get('email')
        uploadedfile = request.files['thefile']

        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM accounts  ORDER BY user_id DESC LIMIT 1')
        end_index = cursor.fetchone()[0]
        conn.commit()

        cursor = conn.cursor()

        postgres_insert_query = """INSERT INTO accounts (user_id, emailone, emailtwo, emailthree, emailfour, emailfive, 
        filename) VALUES (%s,%s,%s, %s,%s,%s, %s) """
        record_to_insert = (
            end_index + 1, enteredemail, enteredemail, enteredemail, enteredemail, enteredemail,
            uploadedfile.filename)
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()

        s3 = get_s3()
        if uploadedfile:
            filename = secure_filename(uploadedfile.filename)
            uploadedfile.save(filename)
            s3.upload_file(
                Bucket='guttaprojectbucket',
                Filename=filename,
                Key=filename
            )

    return render_template('index.html')


@app.route('/logout')
def logouts():
    if 'user' in session:
        session.pop('user')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
