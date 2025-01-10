from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data to simulate a database
medicines = []

@app.route('/medicines', methods=['GET'])
def get_medicines():
    return jsonify(medicines)

@app.route('/medicines', methods=['POST'])
def add_medicine():
    medicine = request.json
    medicines.append(medicine)
    return jsonify(medicine), 201

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(port=5000)