import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Título da aplicação
st.title('Calculadora de Derivadas Polinomiais com Gráfico e Método de Newton-Raphson')

# Funções auxiliares
def format_polynomial(terms):
    term_str = []
    for multp, potencia in terms:
        if multp == 0:
            continue
        if potencia == 0:
            term_str.append(f"{multp}")
        elif potencia == 1:
            term_str.append(f"{multp if multp != 1 else ''}x")
        else:
            term_str.append(f"{multp if multp != 1 else ''}x^{potencia}")
    return ' + '.join(term_str).replace(' + -', ' - ')

def calculate_derivative(terms):
    derivative_terms = []
    for multp, potencia in terms:
        if potencia != 0:
            derivative_terms.append((multp * potencia, potencia - 1))
    return derivative_terms

def evaluate_polynomial(terms, x):
    return sum(multp * x**potencia for multp, potencia in terms)

def newton_raphson(terms, x0, tolerance=1e-7, max_iterations=100):
    for _ in range(max_iterations):
        fx = evaluate_polynomial(terms, x0)
        f_prime_terms = calculate_derivative(terms)
        f_prime_x = evaluate_polynomial(f_prime_terms, x0)
        if f_prime_x == 0:
            return None  # Derivada zero, não é possível continuar
        x1 = x0 - fx / f_prime_x
        if abs(x1 - x0) < tolerance:
            return x1
        x0 = x1
    return None  # Não convergiu

# Interface do Streamlit
tab1, tab2 = st.tabs(["Calculadora de Derivadas", "Método de Newton-Raphson"])

with tab1:
    st.header("Calculadora de Derivadas")
    num_terms = st.number_input('Digite a quantidade de termos do polinômio:', min_value=1, value=1, step=1)

    terms = []
    for i in range(num_terms):
        multp = st.number_input(f'Digite o multiplicador do termo {i+1}:', key=f'multp_{i}', step=1, value=1)
        potencia = st.number_input(f'Digite a potência do termo {i+1}:', min_value=0, key=f'potencia_{i}', step=1)
        terms.append((multp, potencia))

    if st.button('Calcular Derivada'):
        try:
            # Exibir função f(x)
            f_x = format_polynomial(terms)
            st.write(f"f(x) = {f_x}")

            # Calcular e exibir a derivada f'(x)
            derivative_terms = calculate_derivative(terms)
            f_prime_x = format_polynomial(derivative_terms)
            st.write(f"f'(x) = {f_prime_x}")

            # Guardar os termos e a derivada calculada na sessão
            st.session_state['terms'] = terms
            st.session_state['derivative_terms'] = derivative_terms
            st.session_state['f_x'] = f_x
            st.session_state['f_prime_x'] = f_prime_x
        except Exception as e:
            st.write(f'Erro ao calcular a derivada: {e}')

    if 'terms' in st.session_state and st.checkbox("Deseja calcular valor funcional?"):
        try:
            a = st.number_input("Qual o valor de a?", value=0, step=1)
            f_a = evaluate_polynomial(st.session_state['terms'], a)
            f_prime_a = evaluate_polynomial(st.session_state['derivative_terms'], a)
            st.write(f"f({a}) = {f_a}")
            st.write(f"f'(a) = {f_prime_a}")
            st.write(f"P({a}, {f_a})")

            if st.checkbox("Deseja calcular equação da reta tangente ao gráfico de f no ponto P(a, f(a))?"):
                x = np.linspace(a - 10, a + 10, 1000)
                tangent_line = f_prime_a * (x - a) + f_a
                fig, ax = plt.subplots()
                y = np.array([evaluate_polynomial(st.session_state['terms'], xi) for xi in x])
                ax.plot(x, y, label=f'f(x) = {st.session_state["f_x"]}')
                ax.plot(x, tangent_line, label=f'Tangente em P({a}, {f_a})')
                ax.scatter([a], [f_a], color='red')  # Ponto P(a, f(a))
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

                st.write(f"A equação da reta tangente ao gráfico de f no ponto P({a}, {f_a}) é y = {f_prime_a} * (x - {a}) + {f_a}")
        except Exception as e:
            st.write(f'Erro ao calcular o valor funcional ou a equação da reta tangente: {e}')

with tab2:
    st.header("Método de Newton-Raphson")
    num_terms = st.number_input('Digite a quantidade de termos do polinômio:', min_value=1, value=1, step=1, key='nr_num_terms')

    terms = []
    for i in range(num_terms):
        multp = st.number_input(f'Digite o multiplicador do termo {i+1}:', key=f'nr_multp_{i}', min_value=1, step=1, value=1)
        potencia = st.number_input(f'Digite a potência do termo {i+1}:', min_value=0, key=f'nr_potencia_{i}', step=1)
        terms.append((multp, potencia))

    x0 = st.number_input("Digite o valor inicial x0:", value=0.0)
    tolerance = st.number_input("Digite a tolerância:", value=1e-7, format="%e")
    max_iterations = st.number_input("Digite o número máximo de iterações:", min_value=1, value=100, step=1)

    if st.button('Calcular Raiz'):
        try:
            root = newton_raphson(terms, x0, tolerance, max_iterations)
            if root is not None:
                st.write(f"A raiz encontrada é: {root}")
            else:
                st.write("O método não convergiu.")
        except Exception as e:
            st.write(f'Erro ao calcular a raiz: {e}')
