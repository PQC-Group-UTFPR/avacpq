# 🔐 Alkaline: Criptografia Pós-Quântica Passo a Passo (com Polinômios Binários)
# Este código apresenta uma implementação passo a passo da cifra Alkaline, voltada para ensino e visualização interativa com mensagens binárias.  
# 
# 🎯 Objetivo
# - Entender como funciona a cifra Alkaline
# - Visualizar cada etapa: geração de chave, cifragem, decifragem
# - Observar os efeitos do ruído
#
# 🔣 Representação com Polinômios
# 
# A criptografia Alkaline trabalha com polinômios de grau `n - 1`.  
# Cada mensagem, chave ou vetor é representado como um polinômio:
# - Por exemplo: `m(x) = 1 + x²` vira `[1, 0, 1, 0]`
# - Operações como soma, subtração e multiplicação de polinômios são feitas modulo q (aqui `q = 23`)


# Parâmetros iniciais
import random

n = 4      # Grau do polinômio
k = 2      # Dimensão do vetor
q = 23     # Módulo
eta = 1    # Parâmetro de ruído (binomial centrado)




# ⚙️ Funções auxiliares
# 
# Aqui definimos como criar:
# - Erros pequenos (simulando ruído)
# - Polinômios aleatórios
# - As operações básicas com polinômios:
#   - adição, subtração, multiplicação
#   - tudo feito mod q, com redução mod x⁴ + 1

def centered_binomial(eta):
    return sum(random.randint(0, 1) - random.randint(0, 1) for _ in range(eta))

def error_poly():
    return [centered_binomial(eta) for _ in range(n)]

def random_poly():
    return [random.randint(0, q - 1) for _ in range(n)]

def poly_add(a, b):
    return [(x + y) % q for x, y in zip(a, b)]

def poly_sub(a, b):
    return [(x - y) % q for x, y in zip(a, b)]

def poly_mul(a, b):
    res = [0] * (2 * n - 1)
    for i in range(n):
        for j in range(n):
            res[i + j] += a[i] * b[j]
    for i in range(n, 2 * n - 1):
        res[i - n] -= res[i]
    return [x % q for x in res[:n]]

# 🔑 Etapa 1: Geração de Chave
# 
# - Gera-se uma matriz `A` de polinômios aleatórios
# - O segredo `s` é um vetor com ruído (pequenos inteiros)
# - O erro `e` também é pequeno
# - A chave pública é: [t = A·s + e]
# 
# > `A` e `t` são públicos, `s` é o segredo privado

def keygen():
    A = [[random_poly() for _ in range(k)] for _ in range(k)]
    s = [error_poly() for _ in range(k)]
    e = [error_poly() for _ in range(k)]
    t = []
    for i in range(k):
        acc = [0] * n
        for j in range(k):
            acc = poly_add(acc, poly_mul(A[i][j], s[j]))
        t.append(poly_add(acc, e[i]))
    return (A, t), s

# ✉️ Etapa 2: Cifragem da Mensagem
# 
# Aretha quer cifrar `m(x)` usando a chave pública de Bernie.
# 
# Ela gera:
# - Um vetor `r` aleatório
# - Ruídos `e₁`, `e₂`
# 
# Calcula:
# - u = Aᵗ·r + e₁
# - v = tᵗ · r + e₂ + ⎣q/2⎦ · m
#
# Onde:
# - A: matriz pública de polinômios
# - t: chave pública
# - r: vetor aleatório (ruído)
# - e₁, e₂: ruídos adicionais pequenos
# - m: mensagem como vetor binário (coeficientes 0 ou 1)
#
# `u` e `v` são enviados para Bernie como o texto cifrado

def encrypt(pubkey, message_poly):
    A, t = pubkey
    r = [error_poly() for _ in range(k)]
    e1 = [error_poly() for _ in range(k)]
    e2 = error_poly()

    u = []
    for i in range(k):
        acc = [0] * n
        for j in range(k):
            acc = poly_add(acc, poly_mul(A[j][i], r[j]))
        u.append(poly_add(acc, e1[i]))

    acc = [0] * n
    for i in range(k):
        acc = poly_add(acc, poly_mul(t[i], r[i]))
    acc = poly_add(acc, e2)
    m_scaled = [(q // 2 * m) % q for m in message_poly]
    v = poly_add(acc, m_scaled)

    return u, v

# 🔓 Etapa 3: Decifragem da Mensagem
# 
# Bernie usa seu segredo `s` para calcular:
# 
# v-sᵗ·u ≈ ⎣q/2⎦·m
#
# Onde:
# - `sᵗ · u` estima a parte "secreta" da cifra
# - Se o ruído for pequeno, o resultado pode ser dividido por `⎣q/2⎦` e arredondado
#   para recuperar a mensagem original m.
#
# Isso só funciona se o ruído for pequeno o suficiente.

def decrypt(privkey, u, v):
    s = privkey
    acc = [0] * n
    for i in range(k):
        acc = poly_add(acc, poly_mul(s[i], u[i]))
    diff = poly_sub(v, acc)
    return [min(1, round(x / (q // 2))) for x in diff]

# ✅ Resultado
# 
# Aqui executamos a cifra completa e imprimimos:
# - Mensagem original
# - Vetores `u`, `v`
# - Produto secreto `s·u`
# - Diferença `v - s·u`
# - Mensagem decodificada final

m = [random.randint(0, 1) for _ in range(n)]
print("Mensagem binária original:", m)

pubkey, privkey = keygen()
u, v = encrypt(pubkey, m)
rec = decrypt(privkey, u, v)

print("\nu:")
for i, poly in enumerate(u):
    print(f"u[{i}] =", poly)

print("\nv =", v)
print("\nChave secreta s:")
for i, poly in enumerate(privkey):
    print(f"s[{i}] =", poly)

print("\nMensagem decodificada:", rec)
if m == rec:
    print("✅ A mensagem foi decodificada corretamente!")
else:
    print("❌ A mensagem NÃO foi decodificada corretamente.")


# ⚠️ Por que a decodificação pode falhar?
# 
# Mesmo quando a mensagem original é binária, o processo de decodificação pode não recuperar os mesmos valores. Isso ocorre por dois motivos principais:
# 
# 1. Ruído aleatório
# 
# Durante a cifragem, somamos erros `e₁`, `e₂` e `s·u`, todos gerados com a função `centered_binomial(η)`.
# 
# Embora sejam pequenos (por exemplo, entre -1 e 1), a soma deles pode empurrar o valor final de `v - s·u` para mais longe do que o esperado, levando o arredondamento a produzir:
# 
# - `round(10.8 / 11) = 1` (ok)
# - `round(21.9 / 11) = 2` (erro)
# - `round(-0.5 / 11) = 0` (ok)
# 
# 2. Modularidade (mod q)
# 
# Todos os valores estão em um sistema de aritmética modular (mod q). Isso significa que valores "dão a volta" ao ultrapassar `q`. Por exemplo:
# 
# - `m = 1 → 11`, mas se houver erro: `11 + 11 = 22 → round(22 / 11) = 2`
# 
# Esse comportamento é esperado e faz parte da natureza probabilística do Alkaline.
