from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./templates')

app.secret_key = "12345678"

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html'
    )

def take_photo():
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)