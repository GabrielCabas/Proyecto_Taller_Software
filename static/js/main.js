actualize_labels = () => {
    $("#label_Kca").text(K_ca.val())
    $("#label_a").text(a.val())
    $("#label_d").text(d.val())
    $("#label_Kkinase").text(Kkinase.val())
    $("#label_stim").text(stim.val())
    $("#label_stim_range").text(stim_slider.val().replace(",", " - "))
    $("#label_t").text(t.val())
}

create_plot = () => {
    $.ajax({
        url: "/",
        type: "POST",
        data: {
            k_ca: K_ca.val(),
            a: a.val(),
            d: d.val(),
            k_kinase: Kkinase.val(),
            stim: stim.val(),
            stim_range: stim_slider.val(),
            t: t.val()
        }
    }).done((data) => {
        let layout1 = {
            autosize: true,
            height: 500,
            width: 1050,
            yaxis: { title: '$[Ca^{+2}]_{cyt}\\;(\\mu M)$' },
            xaxis: { title: '$time\\;(s)$' }
        };
        let layout2 = {
            autosize: true,
            height: 500,
            width: 1050,
            yaxis: { title: '$P(Open)$' },
            xaxis: { title: '$time\\;(s)$' }
        };
        let config = {
            //displayModeBar: false,
        };
        var trace1 = {};
        if (data.state == "success") {
            var trace1 = {
                x: data.values.t_f,
                y: data.values.Ca_r,
                type: 'line',
                name: "Ca int",
                hovertemplate: `Calcium concentration: %{y:.4f} uM <br>Time: %{x:.3f} s <extra></extra>`,
            }
        }
        var trace2 = {};
        if (data.state == "success") {
            var trace2 = {
                x: data.values.t_f,
                y: data.values.p_j,
                type: 'line',
                name: "Open Probability",
                hovertemplate: `Probability: %{y:.4f} <br>Time: %{x:.3f} s <extra></extra>`
            }
        }
        Plotly.react('plot', {
            data: [trace1],
            layout: layout1,
            config: config
        })
        Plotly.react('plot2', {
            data: [trace2],
            layout: layout2,
            config: config
        })
    })
}

$("#info_button").on("click", () => {
    if ($("#info").css("display") == "none") {
        $("#info").show()
        $("#label_button").text("Hide ")
    }
    else {
        $("#info").hide()
        $("#label_button").text("Show ")
    }
})

$("#parameters_button").on("click", () => {
    if ($("#fixed_parameters").css("display") == "none") {
        $("#fixed_parameters").show()
        $("#label_button_parameters").text("Hide fixed parameters")
    }
    else {
        $("#fixed_parameters").hide()
        $("#label_button_parameters").text("Show fixed parameters")
    }
})

$("#info").hide()
$("#fixed_parameters").hide()

var form = $(".formulario")
var K_ca = $("#K_ca").slider({
    id: "slider",
    min: 0.02,
    max: 0.2,
    step: 0.01,
    value: 0.05
})
var a = $("#a").slider({
    id: "slider",
    min: 50,
    max: 500,
    step: 1,
    value: 200
})
var d = $("#d").slider({
    class: "slider",
    min: 0.5,
    max: 5,
    step: 0.1,
    value: 1
})
var Kkinase = $("#Kkinase").slider({
    class: "slider",
    min: 0.5,
    max: 5,
    step: 0.01,
    value: 2
})
var stim = $("#stim").slider({
    class: "slider",
    min: 0.5,
    max: 5,
    step: 0.01,
    value: 2
})
var stim_slider = $("#stim_slider").slider({
    class: "slider_range",
    min: 50,
    max: 1000,
    step: 10,
    range: true,
    value: [500, 700]
})
var t = $("#t").slider({
    class: "slider_range",
    min: 1,
    max: 15,
    step: 1,
    value: 10
})

actualize_labels()
create_plot()
form.on("input change", () => {
    actualize_labels()
})
form.on("mouseup", () => {
    create_plot()
})
document.addEventListener("contextmenu", function (e) { e.preventDefault(); });
$("#inicial").on("click", () => {
    K_ca.slider("setValue", 0.05)
    a.slider("setValue", 200)
    d.slider("setValue", 1)
    Kkinase.slider("setValue", 2)
    stim.slider("setValue", 2)
    stim_slider.slider("setValue", [500, 700])
    t.slider("setValue", 10)
    actualize_labels()
    create_plot()
})

$("#save_data").on("change", () => {
    let value = $("#save_data option:selected").text()
    if (value != "Save data as") {
        pywebview.api.save_dialog(value).then((path) => {
            $.ajax({
                url: "/save_data",
                type: "POST",
                data: {
                    route: path,
                    k_ca: K_ca.val(),
                    a: a.val(),
                    d: d.val(),
                    k_kinase: Kkinase.val(),
                    stim: stim.val(),
                    stim_range: stim_slider.val(),
                    t: t.val()
                }
            }).then((res) => {
                if (res.state == "success") {
                    Swal.fire('Data saved!', "You saved your data in\n" + path, 'success')
                }
            })
        })
    }
})