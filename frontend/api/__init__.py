from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('../templates/testtavo.html')


@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello world1"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
