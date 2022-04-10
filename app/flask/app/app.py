from flask import Flask,render_template,request,send_file
import requests,json,os,functions

totemo_username=os.environ['TOTEMO_USERNAME']
totemo_password=os.environ['TOTEMO_PASSWORD']
totemo_baseurl=os.environ['TOTEMO_BASEURL']

###########################################################################################################################
#WebServer & Local Settings
###########################################################################################################################

app = Flask(__name__)


#Login Page
@app.route('/')
def index():
    return render_template('index.html', title="Public Key Query")


@app.route('/pubkey', methods=["POST"])
def pubkey():
    if request.method=='POST':
        if request.form:
            local_email = request.form['email']
            key_type = (request.form['keytype'].lower())
            print(f"E-Mail: {local_email} KeyType: {key_type}")
            filename=functions.get_pubkey(key_type,local_email,totemo_username,totemo_password,totemo_baseurl)
            print(f"Filename: {filename}")
            return send_file(f"./cert/{filename}", as_attachment=True)

if __name__ == "__main__":
    app.run()
