from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./templates')

app.secret_key = "12345678"

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html'
    )

@app.route('/transfer_data')
def transfer_data():
    # Get the query parameters from the request
    ppm = request.args.get('ppm')
    sound = request.args.get('sound')
    acc = request.args.get('acc')

    # Print the values to the console
    print("PPM:", ppm)
    print("Sound:", sound)
    print("Acceleration:", acc)

    return render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)