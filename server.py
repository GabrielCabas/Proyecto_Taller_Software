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
        g_cac_dyn = float(request.form["g_cac_dyn"])
        k_kinase = float(request.form["k_kinase"])
        stim = float(request.form["stim"])
        system.solve(k_ca=k_ca, a=a, d=d, g_cac_dyn=g_cac_dyn, k_kinase=k_kinase, stim=stim)
        t, ca_r, p_j = system.get_solutions()
        return make_response(jsonify({"state": "success", "values": {"t_f": list(t), "Ca_r": list(ca_r), "p_j": list(p_j)}}))
    if(request.method == "GET"):
        return render_template("index.html")
if __name__ == '__main__':
   server.run(debug=True)