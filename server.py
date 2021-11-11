from flask import Flask, render_template, request, jsonify, make_response
from model import model
import pandas as pd
from PIL import Image
from io import BytesIO
import re, base64
server = Flask(__name__, template_folder="./", static_folder="static")
system = model()
@server.route('/', methods=["GET", "POST"])
def index():
    if(request.method == "POST"):
        k_ca = float(request.form["k_ca"])
        a = int(request.form['a'])
        d = float(request.form["d"])
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
@server.route("/save_data", methods=["GET", "POST"])
def save_data():
    path = request.form["route"]
    #Parameters
    k_ca = float(request.form["k_ca"])
    a = int(request.form['a'])
    d = float(request.form["d"])
    k_kinase = float(request.form["k_kinase"])
    stim = float(request.form["stim"])
    stim_range = request.form["stim_range"].split(",")
    tf = int(request.form["t"])
    stim_t1 = float(stim_range[0])/1000
    stim_t2 = float(stim_range[1])/1000
    
    sufix = path.split(".")[-1]
    t, ca_r, pO = system.get_solutions()
    data = {"t": t, "Ca_r": ca_r, "pO" : pO}
    df = pd.DataFrame(data)
    if(sufix != "xlsx"):
        f = open(path, "w")
        f.write("#k_ca = {k_ca}\n".format(k_ca = k_ca))
        f.write("#a = {a}\n".format(a = a))
        f.write("#d = {d}\n".format(d = d))
        f.write("#k_kinase = {k_kinase}\n".format(k_kinase = k_kinase))
        f.write("#stim = {stim}\n".format(stim = stim))
        f.write("#stim_range = {stim_t1} - {stim_t2}\n".format(stim_t1 = stim_t1, stim_t2 = stim_t2))
        f.write("#tf = {tf}\n".format(tf = tf))

        if(sufix == "csv"):
            df.to_csv(f, index = False)
        if(sufix == "tsv"):
            df.to_csv(f, index = False, sep="\t")
        f.close()
    else:
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name="data")
        parameters_df = pd.DataFrame(columns=["k_ca", "a", "d", "k_kinase", "stim", "stim_t1", "stim_t2", "tf"])
        parameters_df = parameters_df.append({"k_ca": k_ca, "a": a, "d": d, "k_kinase": k_kinase, "stim": stim,
                            "stim_t1": stim_t1, "stim_t2": stim_t2, "tf": tf},ignore_index=True)
        parameters_df.to_excel(writer, sheet_name="parameters")
        writer.save()
    return make_response(jsonify({"state": "success"}))

@server.route("/send_image", methods=["GET", "POST"])
def send_image():
    url = request.form["url"]
    path = request.form["route"]
    base64_data = re.sub('^data:image/.+;base64,', '', url)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img.save(path, "PNG")
    return make_response(jsonify({"state": "success"}))

if __name__ == '__main__':
   server.run(debug = True)