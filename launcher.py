from model import model
from matplotlib import pyplot as plt
modelo = model()
# stim, stim_t1, stim_t2, tf
status = modelo.solve(k_ca = 0.05, a = 200, d = 1, k_kinase = 2, stim = 2, stim_t1=0.5, stim_t2=0.7, tf = 10)
if(status["status"] == "failed"):
    print("Bad parameters")
else:
    print("Good parameters")
    t, ca_r, p_j = modelo.get_solutions()
    plt.subplot(1, 2, 1)
    plt.plot(t, ca_r)
    plt.subplot(1, 2, 2)
    plt.plot(t, p_j)
    plt.show()