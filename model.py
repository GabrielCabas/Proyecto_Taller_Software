import numpy as np
from scipy.integrate import odeint
class model:
    def __init__(self):
        #Initial values
        self.alfa = 2.5 #uM/s
        self.V = -50 #mV
        self.Ca_ext = 1000 #uM
        self.Ca_0 = 0.1 #uM
        self.delta_r = 165.13 #mV
        self.pI = 0
        self.pO = 0
        self.scale = 0.02
        self.g_Co = 0.004844689705

    def __system(self, y, t, k_ca, a, d, k_kinase, stim):
        ca_int, pO, pI = y
        g_C = self.g_Co + pO * self.scale
        d_Ca_int = stim - self.alfa * (ca_int**2 / (ca_int**2 + k_ca**2) + g_C*(self.V - 12.5* np.log(self.Ca_ext / ca_int)))
        dPO = a * ca_int**4 / (k_kinase**4 + ca_int**4) * (1 - pO - pI) - d * pO
        dPI = d * pO
        return d_Ca_int, dPO, dPI

    def solve(self, k_ca, a, d, k_kinase, stim, stim_t1, stim_t2, tf):

        t1 = np.linspace(start = 0, stop = stim_t1, num = 1000) #s
        y = self.Ca_0, self.pO, self.pI
        system = odeint(self.__system, y, t1, args=(k_ca, a, d, k_kinase, 0)).T
        self.sol_Ca_r = system[0]
        self.sol_pO = system[1]
        self.sol_pI = system[2]
        y = self.sol_Ca_r[-1], self.sol_pO[-1], self.sol_pI[-1]
        t2 = np.linspace(start = stim_t1, stop = stim_t2, num = 1000)
        system = odeint(self.__system, y, t2, args=(k_ca, a, d, k_kinase, stim)).T
        self.sol_Ca_r = np.concatenate((self.sol_Ca_r,system[0]), axis=None)
        self.sol_pO = np.concatenate((self.sol_pO,system[1]), axis=None)
        self.sol_pI = np.concatenate((self.sol_pI,system[2]), axis=None)
        y = self.sol_Ca_r[-1], self.sol_pO[-1], self.sol_pI[-1]
        t3 = np.linspace(start = stim_t2, stop = tf, num = 1000)
        system = odeint(self.__system, y, t3, args=(k_ca, a, d, k_kinase, 0)).T
        self.sol_Ca_r = np.concatenate((self.sol_Ca_r,system[0]), axis=None)
        self.sol_pO = np.concatenate((self.sol_pO,system[1]), axis=None)
        self.sol_pI = np.concatenate((self.sol_pI,system[2]), axis=None)

        self.t = np.concatenate((t1,t2, t3), axis=None)
        return {"status": "success"}

    def __validate_parameters(self, k_ca, a, d, g_cac_dyn, k_kinase, stim, stim_t1, stim_t2):
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
        elif(type(stim_t1) != float or stim_t1 < 0.05 or stim_t1 > 1):
            return False
        elif(type(stim_t2) != float or stim_t2 < 0.05 or stim_t2 > 1):
            return False
        else:
            return True
    def get_solutions(self):
        return self.t, self.sol_Ca_r, self.sol_pO