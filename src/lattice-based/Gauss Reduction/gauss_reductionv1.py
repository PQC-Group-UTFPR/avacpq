import numpy as np
import matplotlib.pyplot as plt 

def gaussian_lattice_reduction(v1, v2):
    i = 1
    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    # pegando valores da base original para comparar no grafico
    base_ruinV1 = np.array(v1, dtype=float) 
    base_ruinV2 = np.array(v2, dtype=float)  
    while True:
        # verifica: ||v1|| <= ||v2||
        if np.linalg.norm(v2) < np.linalg.norm(v1):
            v1, v2 = v2, v1

        # calculo do m
        m = int(round(np.dot(v1, v2) / np.dot(v1, v1)))
        print("Step: ", i)
        print(f"V1: {v1.astype(int)}\nV2: {v2.astype(int)}\nm = {m}\n\n")
        
        # se m == 0, não podemos mais reduzir
        if m == 0:
            break

        # atualize v2
        v2 = v2 - m * v1
        
        base_b1 = np.array(v1, dtype=float)
        base_b2 = np.array(v2, dtype=float)
        
    
        # plotar a base ruin
        plt.quiver(0, 0, base_ruinV1[0], base_ruinV1[1], angles='xy', scale_units='xy', scale=1, color='r', label='Base Ruim(v1)', width=0.005)
        plt.quiver(0, 0, base_ruinV2[0], base_ruinV2[1], angles='xy', scale_units='xy', scale=1, color='orange', label='Base Ruim(v2)', width=0.005)

        # plot da base boa
        plt.quiver(0, 0, base_b1[0], base_b1[1], angles='xy', scale_units='xy', scale=1, color='blue', label='Base Boa(v1)', width=0.005)
        plt.quiver(0, 0, base_b2[0], base_b2[1], angles='xy', scale_units='xy', scale=1, color='cyan',  label='Base Boa(v2)', width=0.005)

    
        plt.xlim(-10000, 10000)
        plt.ylim(-10000, 10000)
        plt.grid(linestyle='--', alpha=0.7)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.legend()
        plt.title(f'Comparação: Base Ruim vs. Base Boa (Passo {i})')
        plt.show()
        i+=1
    return [v1.astype(int), v2.astype(int)]

# mesmo exemplo do livro "Hoffstein2015 Introduction to Mathematical Cryptography"
v1 = [66586820, 65354729]
v2 = [6513996, 6393464]

base_reduzida = gaussian_lattice_reduction(v1, v2)