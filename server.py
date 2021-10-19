from flask import Flask, render_template, request, jsonify, make_response
from model import model
server = Flask(__name__, template_folder="./", static_folder="static")
@server.route('/', methods=["GET", "POST"])
def index():
    if(request.method == "POST"):
        N = int(request.form["N"])
        I0 = int(request.form['I0'])
        R0 = int(request.form["R0"])
        betta = float(request.form["betta"])
        gamma = float(request.form["gamma"])
        block_size = int(request.form["block_size"])
        epsilon = float(request.form["epsilon"])
        max_iter = int(request.form["max_iter"])
        system = model(N, I0, R0, betta, gamma, 
                            block_size=block_size, epsilon=epsilon, 
                            max_iter=max_iter)
        system.solve()
        data = system.get_results()
        return make_response(jsonify(data))
    if(request.method == "GET"):
        return render_template("index.html")
if __name__ == '__main__':
   server.run(debug=True)