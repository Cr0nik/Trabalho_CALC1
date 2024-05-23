import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Título da aplicação
st.title('Calculadora de Derivadas Polinomiais com Gráfico')

# Campo de entrada para a quantidade
quantidade = st.number_input('Digite a quantidade de polinômios:', min_value=1, step=1)

polinomios = []

# Listas para armazenar os campos de entrada
multp = []
expoente = []
derivada = []

def calcular_derivada(multiplicadores, potencias):
    derivadas = []
    for multiplicador, potencia in zip(multiplicadores, potencias):
        if potencia == 0:
            derivadas.append(0)
        else:
            derivadas.append(multiplicador * potencia)
    return derivadas

# Geração dos campos com base na quantidade fornecida
for i in range(quantidade):
    st.write(f'Campos para o polinômio {i + 1}')
    multp.append(st.number_input(f'Digite o multiplicador do polinômio {i + 1} aqui:', step=1.0, key=f'mult{i}'))
    expoente.append(st.number_input(f'Digite a potência do polinômio {i + 1} aqui:', step=1.0, key=f'exp{i}'))
    polinomios.append((multp, expoente))

# Ponto onde a reta tangente será calculada
ponto_tangente = st.number_input('Digite o ponto onde a reta tangente será calculada:', step=1.0)

# Calcular a derivada dos polinômios
if st.button('Calcular Derivadas'):
    derivada = calcular_derivada(multp, expoente)
    for i in range(quantidade):
        st.write(f'A derivada do polinômio {i + 1} é: {derivada[i]}')

    for multiplicador, potencia in polinomios:
        # Função polinomial e sua derivada
        def polinomio(x):
            return sum(m * x**e for m, e in zip(multp, expoente))

        def derivada_polinomio(x):
            return sum(d * x**(e-1) for d, e in zip(derivada, expoente) if e != 0)

        # Ponto específico para a reta tangente
        x0 = ponto_tangente
        y0 = polinomio(x0)
        dy_dx = derivada_polinomio(x0)
        
        # Função da reta tangente
        def reta_tangente(x):
            return dy_dx * (x - x0) + y0

        # Plotar o gráfico do polinômio e da reta tangente
        x_vals = np.linspace(x0 - 10, x0 + 10, 400)
        y_vals = polinomio(x_vals)
        y_tan_vals = reta_tangente(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label='Polinômio')
    plt.plot(x_vals, y_tan_vals, '--', label='Reta Tangente')
    plt.scatter([x0], [y0], color='red')  # Marca o ponto de tangência
    plt.text(x0, y0, f'({x0}, {y0})', fontsize=12, verticalalignment='bottom')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Gráfico do Polinômio e da Reta Tangente')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
