import random
import time

# --- Tipos para organizar os dados da chave pública e do ciphertext ---

class PublicKey:
    # Estrutura que representa a chave pública composta por vetores A, B e o módulo Q
    def __init__(self, A, B, Q):
        self.A = A
        self.B = B
        self.Q = Q

class Ciphertext:
    # Estrutura que representa o texto cifrado como um par (U, V)
    def __init__(self, U, V):
        self.U = U
        self.V = V


def main():
    # Inicializa a semente aleatória com o tempo atual
    random.seed(time.time())

    # Mensagem introdutória sobre o LWE
    print("=====================================================")
    print("     LWE (Learning With Errors) - Cifra de 1 bit     ")
    print("=====================================================")
    print("Equcao base: b = (a * s + e) mod q")
    print("Onde:")
    print("  a -> valor aleatorio de Z_q")
    print("  s -> chave secreta")
    print("  e -> pequeno erro aleatorio (ruido)")
    print("  q -> numero primo (modulo)\n")

    # --- Definindo os parâmetros principais ---
    nvals = 20  # Número de pares (a, b) na chave pública
    q = 97      # Módulo primo
    s = 20      # Chave secreta
    message = random.randint(0, 1)  # Bit aleatório a ser cifrado

    # --- Geração de chaves ---
    print("\n--- Gerando chaves publicas e secretas ---")
    print("Requisitos: precisamos de pares (a, b) tais que b = a*s + e (mod q)\n")
    publicKey, secretKey, eList = KeyGen(nvals, q, s)

    # --- Exibindo os parâmetros e chaves geradas ---
    print("\n--- Parametros e chaves geradas ---")
    print("Bit a ser cifrado:\t", message)
    print("Chave Publica (A):\t", publicKey.A)
    print("Chave Publica (B):\t", publicKey.B)
    print("Erros usados (e):\t", eList)
    print("Chave Secreta (s):\t", secretKey)
    print("Numero primo (q):\t", q)

    # --- Cifrando a mensagem ---
    print("\n--- Cifrando a mensagem ---")
    cipher, sampleIndices, sampledPairs = Encrypt(message, publicKey)

    # --- Mostrando os pares amostrados usados na cifra ---
    print("\n--- Amostragem dos pares da chave publica ---")
    print("Indices sorteados:", sampleIndices)
    print("Pares amostrados:")
    for pair in sampledPairs:
        print(f"[a = {pair[0]}, b = {pair[1]}]")

    # --- Explicando o cálculo de u e v ---
    sampled_A = [pair[0] for pair in sampledPairs]
    sampled_B = [pair[1] for pair in sampledPairs]

    print("\n--- Calculo de u e v ---")
    print("u = (", " + ".join(map(str, sampled_A)), ") %", q)
    print("v = (", " + ".join(map(str, sampled_B)), f"+ ({q//2} * {message})) %", q)

    print("\nResultado:")
    print("u =\t", cipher.U)
    print("v =\t", cipher.V)

    # --- Decifrando a mensagem ---
    print("\n--- Decifrando o ciphertext ---")
    decryptedMsg, res = Decrypt(cipher, secretKey, q)

    # --- Mostrando os cálculos da operação de decodificação ---
    print("\n--- Calculo de 'res' (v - s*u mod q) ---")
    print(f"res = ({cipher.V} - {secretKey} * {cipher.U}) % {q}")
    intermediate = (cipher.V - secretKey * cipher.U)
    if intermediate < 0:
        fixed = intermediate % q
        print(f"    = ({intermediate}) % {q} = {fixed}  (ajustado para positivo)")
    else:
        print(f"    = {intermediate}  (valor positivo)")

    # --- Interpretando o resultado ---
    print("\n--- Interpretando resultado ---")
    comparison = ">" if res > q / 2 else "<="
    expected_bit = 1 if res > q / 2 else 0
    print(f"res = {res} {comparison} q/2 ({q/2}), portanto a MENSAGEM e: {expected_bit}")


# --------------------------------------
# Função para decifrar o bit cifrado
def Decrypt(cipher, secretKey, q):
    res = (cipher.V - secretKey * cipher.U) % q
    if res < 0:
        res += q

    # Se resultado for maior que q/2, interpretamos como bit 1, senão bit 0
    message = 1 if res > q / 2 else 0
    return message, res


# --------------------------------------
# Função de geração de chave: cria vetores A e B com erros
def KeyGen(nvals, q, s):
    Amap = set()         # Para evitar valores repetidos de 'a'
    A, B, eList = [], [], []

    print("\n--- Gerando pares (a, b) com erro ---")
    while len(A) < nvals:
        a = random.randint(0, q - 1)
        if a not in Amap:
            Amap.add(a)
            b, e = stepKeyGen(a, s, q)
            A.append(a)
            B.append(b)
            eList.append(e)
            print(f"a = {a}, e = {e}, b = (a*s + e) % q = {b}")

    return PublicKey(A, B, q), s, eList


# --------------------------------------
# Calcula b = a*s + e mod q, e retorna b e o erro usado
def stepKeyGen(a, s, q):
    e = random.randint(1, 4)  # Gera pequeno erro aleatório
    b = (a * s + e) % q
    return b, e


# --------------------------------------
# Realiza a cifra do bit, amostrando parte da chave pública
def Encrypt(message, pk):
    nvals = len(pk.A)
    sampleSize = nvals // 4  # Usa 1/4 da chave pública
    indices = uniqueSample(nvals - 1, sampleSize)

    u, v = 0, 0
    sampledPairs = []

    print("\n--- Processando cifra com amostragem ---")
    for idx, i in enumerate(indices):
        delta_u, delta_v, pair = stepEncrypt(i, pk)
        u += delta_u
        v += delta_v
        sampledPairs.append(pair)
        print(f"{idx + 1}) idx = {i} -> a = {pair[0]}, b = {pair[1]} | u += {delta_u}, v += {delta_v}")

    u %= pk.Q
    v = (v + (pk.Q // 2) * message) % pk.Q  # Adiciona o bit à mensagem de forma escondida

    return Ciphertext(u, v), indices, sampledPairs


# --------------------------------------
# Retorna os valores de A[i] e B[i] usados na cifra
def stepEncrypt(index, pk):
    a = pk.A[index]
    b = pk.B[index]
    return a, b, (a, b)


# --------------------------------------
# Amostragem aleatória sem repetição de índices
def uniqueSample(max_val, count):
    return random.sample(range(0, max_val + 1), count)


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
