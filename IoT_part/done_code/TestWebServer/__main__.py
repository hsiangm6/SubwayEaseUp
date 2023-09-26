from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./templates')

app.secret_key = "12345678"

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html'
    )

@app.route('/data')
def air_sound_data():
    receive_data = request.args.get('arg')
    # data = receive_data.split(',')

    print(f'air/sound: {receive_data}')
    return render_template(
        'index.html'
    )

@app.route('/acc')
def acc_data():
    receive_data = request.args.get('arg')
    # data = receive_data.split(',')

    print(f'acc: {receive_data}')
    return render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)