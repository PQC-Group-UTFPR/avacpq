import random
import time


# --- Tipos para organizar ---
class PublicKey:
    def __init__(self, A, B, Q):
        self.A = A
        self.B = B
        self.Q = Q


class Ciphertext:
    def __init__(self, U, V):
        self.U = U
        self.V = V


def main():
    random.seed(time.time())

    # --- Parâmetros principais ---
    nvals = 20
    q = 97
    s = 20
    message = 1  # bit a ser cifrado (0 ou 1)

    # --- Geração de chaves ---
    publicKey, secretKey, eList = KeyGen(nvals, q, s)

    # --- Display dos parâmetros ---
    print("\n------Parameters and keys-------")
    print("Message to send:\t", message)
    print("Public Key (A):\t", publicKey.A)
    print("Public Key (B):\t", publicKey.B)
    print("Errors (e):\t\t", eList)
    print("Secret key:\t\t", secretKey)
    print("Prime number:\t\t", q)

    # --- Amostragem e criptografia ---
    cipher, sampleIndices, sampledPairs = Encrypt(message, publicKey)

    print("\n------Sampling Process from public key-------")
    print("Sampling", sampleIndices)
    print("Sampled pairs: ", end="")
    for pair in sampledPairs:
        print(f"[{pair[0]} {pair[1]}] ", end="")
    print()

    # Mostrar como u e v foram calculados
    sampled_A = [pair[0] for pair in sampledPairs]
    sampled_B = [pair[1] for pair in sampledPairs]

    print("\n------Calculation breakdown ------------------------")
    print("u = (", " + ".join(map(str, sampled_A)), ") %", q)
    print("v = (", " + ".join(map(str, sampled_B)), f"+ ({q//2} * {message})) %", q)

    # --- Exibição do cálculo ---
    print("\n------Calculation of 'u' and 'v' -----------------")
    print("u:\t\t", cipher.U)
    print("v:\t\t", cipher.V)

    # --- Decifrar e mostrar resultado ---
    decryptedMsg, res = Decrypt(cipher, secretKey, q)

    print("\n------Calculation of 'res' (v - s*u mod q) ---------")
    print(f"res = (v - s * u) % q")
    print(f"    = ({cipher.V} - {secretKey} * {cipher.U}) % {q}")
    print(f"    = ({cipher.V} - {secretKey * cipher.U}) % {q}")
    print(f"    = ({cipher.V - secretKey * cipher.U}) % {q}")

    # Ajusta se for negativo, como acontece dentro da função
    intermediate = (cipher.V - secretKey * cipher.U)
    if intermediate < 0:
        fixed = intermediate % q
        print(f"    = ({intermediate}) % {q} = {fixed}  (positive value)")
    else:
        print(f"    = {intermediate}  (positive value)")


    print("\n------Interpreting 'res' to get the message --------")
    comparison = ">" if res > q / 2 else "<="
    expected_bit = 1 if res > q / 2 else 0

    print(f"Result is: {res} {comparison} q/2 ({q/2}),\nso the MESSAGE IS : {expected_bit}")



# --------------------------------------
# Decrypt: Decifra o bit a partir do texto cifrado
# --------------------------------------
def Decrypt(cipher, secretKey, q):
    res = (cipher.V - secretKey * cipher.U) % q
    if res < 0:
        res += q

    if res > q / 2:
        message = 1
    else:
        message = 0

    return message, res


# --------------------------------------
# KeyGen: Gera A, B e erro, usando stepKeyGen para cada par
# --------------------------------------
def KeyGen(nvals, q, s):
    Amap = set()
    A, B, eList = [], [], []

    print("\n------Step-by-step Key Generation and error (stepKeyGen)------")
    
    while len(A) < nvals:
        a = random.randint(0, q - 1)
        if a not in Amap:
            Amap.add(a)
            b, e = stepKeyGen(a, s, q)  
            A.append(a)
            B.append(b)
            eList.append(e)
            print(f"stepKeyGen -> a = {a}, e = {e}, b = (a*s+e)%q = {b}")

    return PublicKey(A, B, q), s, eList


# --------------------------------------
# stepKeyGen: Gera b = a*s + e mod q e retorna b e e
# --------------------------------------
def stepKeyGen(a, s, q):
    e = random.randint(1, 4)  # Pequeno ruído aleatório
    b = (a * s + e) % q
    return b, e


# --------------------------------------
# Encrypt: Cifra um bit (0 ou 1) usando stepEncrypt
# --------------------------------------
def Encrypt(message, pk):
    nvals = len(pk.A)
    sampleSize = nvals // 4
    indices = uniqueSample(nvals - 1, sampleSize)

    u, v = 0, 0
    sampledPairs = []

    print("\n------Step-by-step Encryption (stepEncrypt)------")

    for idx, i in enumerate(indices):
        delta_u, delta_v, pair = stepEncrypt(i, pk)
        u += delta_u
        v += delta_v
        sampledPairs.append(pair)
        print(f"stepEncrypt {idx + 1} -> index = {i}, A[i] = {pair[0]}, B[i] = {pair[1]}, u += {delta_u}, v += {delta_v}")

    u %= pk.Q
    v = (v + (pk.Q // 2) * message) % pk.Q

    return Ciphertext(u, v), indices, sampledPairs

# --------------------------------------
# stepEncrypt: Retorna os valores de A[i] e B[i] para um índice i
# --------------------------------------
def stepEncrypt(index, pk):
    a = pk.A[index]
    b = pk.B[index]
    return a, b, (a, b)



# --------------------------------------
# Amostragem aleatória sem repetição
# --------------------------------------
def uniqueSample(max_val, count):
    return random.sample(range(0, max_val + 1), count)


# Roda o programa
if __name__ == "__main__":
    main()
