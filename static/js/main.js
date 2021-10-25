init_values = () => {
    K_ca.val(0.05)
    a.val(200)
    d.val(1)
    g_cac_dyn.val(0.02)
    Kkinase.val(2)
    stim.val(2)
}
actualize_labels = () => {
    $("#label_Kca").text(K_ca.val())
    $("#label_a").text(a.val())
    $("#label_d").text(d.val())
    $("#label_g_cac_dyn").text(g_cac_dyn.val())
    $("#label_Kkinase").text(Kkinase.val())
    $("#label_stim").text(stim.val())
}
var form = $(".formulario")
var K_ca = $("#K_ca")
var a = $("#a")
var d = $("#d")
var g_cac_dyn = $("#g_cac_dyn")
var Kkinase = $("#Kkinase")
var stim = $("#stim")

init_values()
actualize_labels()
form.on("change", () => {
    actualize_labels()
})