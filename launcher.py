from model import model
modelo = model(0.1, -100, 1, 1, 1, -1, 1, t_f=2)
modelo.solve()
t, V, Ca_int, Ycac = modelo.get_solutions()
print(list(Ca_int))