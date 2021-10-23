import numpy as np
from scipy.integrate import odeint

class model:
    def __init__(self):
        #Initial values
        self.alfa = 2.5 #uM/s
        self.V = -50 #mV
        self.Ca_ext = 1000 #uM
        self.Ca_r = 0.1 #uM
        self.delta_r = 165.13 #mV
        self.t = np.linspace(0, 20, 1000) #s
        self.p_j = 0 #p_j = p*
        self.p_i = 0

    def __system(self, y, t, k_ca = 0.05, a = 200, d = 1, g_cac_dyn = 0.02, k_kinase = 2, stim = 2):
        #EDO system
        if(t <= 0.5):
            stim = 0
        if(t > 0.7):
            stim = 0
        ca_int, p_j, p_i = y
        g_cac_0 = ca_int**2 / (self.delta_r * (k_ca**2 + ca_int**2))
        k1 = ca_int**2 / (k_ca**2 + ca_int**2)
        k2 = g_cac_0 + p_j * g_cac_dyn
        k3 = self.V - 12.5 * np.log(self.Ca_ext / ca_int)
        d_ca_int = stim - self.alfa*(k1 + k2 * k3)
        k4 = ca_int**4 / (k_kinase**4 + ca_int**4)
        k5 = 1 - p_j - p_i
        d_p_j = a * k4 * k5 - d * p_j
        d_p_i = d * p_j

        return d_ca_int, d_p_j, d_p_i

    def solve(self, k_ca, a, d, g_cac_dyn, k_kinase, stim):
        if(not self.__validate_parameters(k_ca, a, d, g_cac_dyn, k_kinase, stim)):
            return {"status": "failed"}
        else:
            y = self.Ca_r, 0, 0
            system = odeint(self.__system, y, self.t, args=(k_ca, a, d, g_cac_dyn, k_kinase, stim)).T
            self.sol_Ca_r = system[0]
            self.sol_p_j = system[1]
            self.sol_p_i = system[2]
            return {"status": "success"}
    def __validate_parameters(self, k_ca, a, d, g_cac_dyn, k_kinase, stim):
        if(type(k_ca) != float or k_ca < 0.02 or k_ca > 0.2):
            return False
        elif(type(a) != int or a < 50 or a > 500):
            return False
        elif(type(d) != float or d < 0.5 or d > 5):
            return False
        elif(type(g_cac_dyn) != float or g_cac_dyn < 0.01 or g_cac_dyn > 0.05):
            return False
        elif(type(k_kinase) != float or k_kinase < 0.5 or k_kinase > 5):
            return False
        elif(type(stim) != float or stim < 0.5 or stim > 5):
            return False
        else:
            return True

    def get_solutions(self):
        return self.t, self.sol_Ca_r, self.sol_p_j