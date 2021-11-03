from flask import Flask, render_template, request, jsonify, make_response
from model import model
server = Flask(__name__, template_folder="./", static_folder="static")
system = model()
@server.route('/', methods=["GET", "POST"])
def index():
    if(request.method == "POST"):
        k_ca = float(request.form["k_ca"])
        a = int(request.form['a'])
        d = float(request.form["d"])
        """ g_Co = float(request.form["g_Co"]) """
        k_kinase = float(request.form["k_kinase"])
        stim = float(request.form["stim"])
        stim_range = request.form["stim_range"].split(",")
        tf = int(request.form["t"])
        stim_t1 = float(stim_range[0])/1000
        stim_t2 = float(stim_range[1])/1000
        system.solve(k_ca, a, d, k_kinase, stim, stim_t1, stim_t2, tf)
        t, ca_r, p_j = system.get_solutions()
        return make_response(jsonify({"state": "success", "values": {"t_f": list(t), "Ca_r": list(ca_r), "p_j": list(p_j)}}))
    if(request.method == "GET"):
        return render_template("index.html")
if __name__ == '__main__':
   server.run(debug=True)