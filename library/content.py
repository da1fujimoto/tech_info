from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def app_route():
    return render_template('sample_template.html')
