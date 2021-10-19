import numpy as np
from scipy.integrate import odeint
class model:
    def __init__(self, Ca_int, V, Ycac, Yhca, stim, d, a, t_0 = 0, t_f = 1):
        self.Ca_ext = 1000#uM
        self.Eh = 80.63 #mV
        self.Ca_int = Ca_int#uM
        self.Eca =  12.5 * np.log(self.Ca_ext / self.Ca_int) #mV
        self.t_0 = t_0 #s
        self.t_f = t_f #s
        self.t = np.linspace(t_0, t_f, num = (t_f - t_0) * 10**3) #[s]
        self.V = V #mV
        self.Ycac = Ycac
        self.Yhca = Yhca
        self.stim = stim #uM/s
        self.d = d
        self.a = a

    def __system(self, y, t, Yhca, stim, d, a):
        euler = np.e #Euler's number
        Eh = self.Eh
        Eca = self.Eca
        stim = 0 #First we try without stimulous
        V, Ca_int, Ycac = y #Dependient variables
        #Auxiliar variables
        k1 = (1 - euler**(-(V + 100)/25))/(1 + euler**(-(V + 100)/25))
        k2 = (1 - euler**(-(V + 200)/25))/(1 + euler**(-(V + 200)/25))
        k3 = Yhca * (V - 3*Eh + 2*Eca)
        k4 = Ycac * (V - Eca)
        #EDOs system
        dV = - 5 * (k1 + 0.001 * (2 * k2 + k3 + k4))
        dCa_int = - 2.5 * (k2 - k3 + 0.5 * k4) + stim
        dYcac = - d * Ycac + a * (1 - Ycac)
        return dV, dCa_int, dYcac

    def solve(self):
        y = self.V, self.Ca_int, self.Ycac
        system = odeint(self.__system, y, self.t, args=(self.Yhca, self.stim, self.d, self.a)).T
        self.sol_V = system[0]
        self.sol_Ca = system[1]
        self.sol_Ycac = system[2]

    def get_solutions(self):
        return self.t, self.sol_V, self.sol_Ca, self.sol_Ycac

modelo = model(0.1, -100, 1, 1, 1, -1, 1, t_f=2)
modelo.solve()
t, V, Ca_int, Ycac = modelo.get_solutions()
print(list(Ca_int))