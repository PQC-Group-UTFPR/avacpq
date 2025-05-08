import numpy as np
from dash import html, dcc
import plotly.graph_objects as go
from numpy.linalg import inv
import secrets
from datetime import datetime

# Print debug messages?
debug = True


def debug_print(message, variable=None):
    """
    Prints debug messages with a timestamp if debug mode is enabled.

    Args:
        message (str): The debug message to print.
        variable (optional): Additional variable to print alongside the message.
    """
    if debug:
        current_time = datetime.now().strftime("%H:%M")
        print(f"[DEBUG-{current_time}] {message}")
        if variable is not None:
            print(variable)


def get_user_choice():
    """
    Prompts the user to choose between using a hardcoded plaintext or a random one.

    Returns:
        bool: True if the user chooses random plaintext, False otherwise.
    """
    choice = (
        input("Do you want to use the hardcoded plaintext or a random one? (h/r): ")
        .strip()
        .lower()
    )
    return choice == "r"


def get_dimensions():
    """
    Prompts the user to enter the number of dimensions for the plaintext vector.

    Returns:
        int: The number of dimensions.
    """
    return int(input("Enter the number of dimensions: ").strip())


def generate_random_plaintext(n, r):
    """
    Generates a random plaintext vector of specified dimensions and range.

    Args:
        n (int): The number of dimensions for the plaintext vector.
        r (int): The range for the random values in the plaintext vector.

    Returns:
        numpy.ndarray: The generated random plaintext vector.
    """
    plaintext = np.array([secrets.randbelow(r) - (r / 2) for _ in range(n)])
    return plaintext


class GGH:
    """
    Goldreich-Goldwasser-Halevi (GGH) encryption system implementation.

    The GGH class provides functionalities for generating keys, encrypting and
    decrypting messages using the GGH encryption system. It operates on vectors
    in a lattice-based cryptosystem.
    """

    def __init__(self, n):
        """
        Initializes the GGH encryption system with the specified dimensionality.

        Args:
            n (int): The number of dimensions for the lattice vectors.
        """
        self.n = n
        self.rand = 20

    def generate_keys(self):
        """
        Generates the lattice basis B' and computes the public key U.

        Returns:
            tuple: A tuple containing the desired lattice basis B' (numpy.ndarray)
                   and the public key U (numpy.ndarray).
        """
        # Choose r automatically within a reasonable range
        r = secrets.randbelow(self.rand) + 1
        debug_print(f"Chosen r: {r}")

        # Given lattice basis
        B = np.array(
            [
                [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                for _ in range(self.n)
            ]
        )
        while np.linalg.matrix_rank(B) != self.n:
            B = np.array(
                [
                    [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                    for _ in range(self.n)
                ]
            )
        debug_print("Lattice basis B:", B)

        # Desired lattice basis
        B_prime = np.array(
            [
                [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                for _ in range(self.n)
            ]
        )
        while np.linalg.matrix_rank(B_prime) != self.n:
            B_prime = np.array(
                [
                    [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                    for _ in range(self.n)
                ]
            )
        debug_print("Desired lattice basis B_prime:", B_prime)

        # Compute the public key U
        U = np.dot(B_prime, inv(B))
        debug_print("Public key U:", U)
        
        public_key_inverse = inv(U)
        return B,B_prime, U, public_key_inverse

    def generate_error(self, e):
        """
        Generate an error vector with values from -e to e (inclusive).

        Args:
            e (int): The range of values for the error vector.

        Returns:
            np.array: The generated error vector.
        """
        error = np.array([secrets.randbelow(2 * e + 1) - e for _ in range(self.n)])
        debug_print("Error vector:", error)

        return error

    def encrypt(self, public_key, plaintext, error):
        """
        Encrypt the plaintext by multiplying it with the public key and adding error.

        Args:
            public_key (np.array): The public key used for encryption.
            plaintext (np.array): The plaintext message to be encrypted.
            error (np.array): The error vector to add to the encrypted message.

        Returns:
            np.array: The ciphertext resulting from the encryption process.
        """
        ciphertext = np.dot(plaintext, public_key) + error
        debug_print("Ciphertext:", ciphertext)

        return ciphertext

    def decrypt(self, public_key_inverse, ciphertext):
        """
        Decrypt the ciphertext using the public key inverse.

        Args:
            public_key_inverse (np.array): The inverse of the public key used for decryption.
            ciphertext (np.array): The encrypted message to be decrypted.

        Returns:
            np.array: The decrypted plaintext (before Babai rounding).
        """
        decrypted_plaintext = np.dot(ciphertext, public_key_inverse)
        debug_print("Decrypted plaintext (before Babai rounding):", decrypted_plaintext)

        return decrypted_plaintext

    def babai_rounding(self, decrypted_plaintext, error, inverse_basis):
        """
        Apply Babai rounding to remove the error term if it's small enough.

        Args:
            decrypted_plaintext (np.array): The decrypted plaintext.
            error (np.array): The error vector.
            inverse_basis (np.array): The inverse of the lattice basis used for rounding.

        Returns:
            np.array: The rounded decrypted plaintext.
        """
        rounded_decrypted_plaintext = decrypted_plaintext - np.dot(error, inverse_basis)
        debug_print("Rounded decrypted plaintext:", rounded_decrypted_plaintext)

        return rounded_decrypted_plaintext

    def recover_plaintext(self, rounded_decrypted_plaintext, public_key):
        """
        Recover the plaintext message by multiplying rounded decrypted plaintext
        with U-inverse.

        Args:
            rounded_decrypted_plaintext (np.array): The rounded decrypted plaintext.
            public_key (np.array): The public key used for encryption.

        Returns:
            np.array: The recovered plaintext message.
        """
        plaintext = np.dot(rounded_decrypted_plaintext, inv(public_key))
        plaintext = np.dot(plaintext, public_key)
        plaintext = np.round(plaintext).astype(int)

        return plaintext
        

def initGGH(ggh_data, dimension):
    ggh = GGH(dimension)
    B, B_prime, U, public_key_inverse = ggh.generate_keys()
    error = ggh.generate_error(e=1)
    plaintext = generate_random_plaintext(dimension, ggh.rand)
    ciphertext = ggh.encrypt(U, plaintext, error) 
    decrypt = ggh.decrypt(public_key_inverse, ciphertext)

    ggh_data = {
        'dimension': dimension,
        'B': B.tolist(),
        'B_prime': B_prime.tolist(),
        'U': U.tolist(),
        'public_key_inverse': public_key_inverse.tolist(),
        'plaintext': plaintext.tolist(),
        'error': error.tolist(),
        'ciphertext': ciphertext.tolist(),
        'decrypt': decrypt.tolist(),
        'algorithm': 'GGH'
    }
    return ggh_data

def generate_keygen_steps_content(B, B_prime, U, step):
        
        
        content = []

        if step >= 1:
            content.append(html.Div([
                html.H5("Passo 1: Base Aleatória B"),
                html.P(
                    f"""
                    B = {np.array2string(B, precision=2, suppress_small=True)}
                    """,
                    style={'fontFamily': 'monospace', 'text-align': 'left'}
                )
            ], className='step-box'))

        if step >= 2:
            content.append(html.Div([
                html.H5("Passo 2: Base Privada B'"),
                html.P(
                    f"""
                    B' = {np.array2string(B_prime, precision=2, suppress_small=True)}
                    """,
                    style={'fontFamily': 'monospace','text-align': 'left'}
                )
            ], className='step-box'))

        if step >= 3:
            B_inv = np.linalg.inv(B)
            content.append(html.Div([
                html.H5("Passo 3: Cálculo da Chave Pública U = B' × B⁻¹"),
                html.P([
                    "U = B' × B⁻¹ =",html.Br(), 
                    f"{np.array2string(B_prime, precision=2)} × " 
                    f"{np.array2string(B_inv, precision=2)}",html.Br(), 
                    f"= {np.array2string(U, precision=2)}"
                    ],
                    style={'fontFamily': 'monospace','text-align': 'center'}
                )
            ], className='step-box'))

        return html.Div([
            html.H4("Passo a Passo", className="steps-title"),
            html.H4("Geração de Chaves"),
            *content 
        ], style={'marginTop': '5px'})
    
def get_ggh_data(step, ggh_data):

        B = np.array(ggh_data['B'])
        B_prime = np.array(ggh_data['B_prime'])
        U = np.array(ggh_data['U'])
        public_key_inverse = np.array(ggh_data['public_key_inverse'])
        dimension = np.array(ggh_data['dimension'])
        
        fig = go.Figure()

        step_vector_mapping = {
        1: [{'matrix': B, 'color': 'gray', 'dash': None, 'prefix': 'Base Ruim'}],
        2: [{'matrix': B_prime, 'color': 'blue', 'dash': None, 'prefix': 'Base Boa'}],
        3: [{'matrix': U, 'color': 'red', 'dash': None, 'prefix': 'Chave Pública'}],
        4: [
            {'matrix': B, 'color': 'gray', 'dash': None, 'prefix': 'Base Ruim'},
            {'matrix': B_prime, 'color': 'blue', 'dash': None, 'prefix': 'Base Boa'},
            {'matrix': U, 'color': 'red', 'dash': None, 'prefix': 'Chave Pública'}
        ]
    }
        vector_configs = step_vector_mapping.get(step, [])

        for config in vector_configs:
            for i in range(dimension):
                fig.add_trace(go.Scatter(
                    x=[0, config['matrix'][i, 0]],
                    y=[0, config['matrix'][i, 1]],
                    mode='lines+markers',
                    line=dict(color=config['color'], dash=config['dash']),
                    marker=dict(color=config['color']),
                    name=config['prefix'],
                    showlegend=(i == 0)
                ))

        fig.update_layout(
            title='Visualização das Bases e Chaves GGH',
            xaxis_title='X',
            yaxis_title='Y',
            template="plotly_dark"
        )
        steps_content = generate_keygen_steps_content(B, B_prime, U, step)

        return fig, steps_content

def encrypt_step(ggh_data, step):
    plaintext = np.array(ggh_data['plaintext'])
    error = np.array(ggh_data['error'])
    U = np.array(ggh_data['U'])
    ciphertext = np.array(ggh_data['ciphertext'])

    content = []

    if step >= 5:
        content.append(html.Div([
            html.H5("Passo 1: Geração da Mensagem Secreta (Plaintext)"),
            html.P(
                f"""
                plaintext = {np.array2string(plaintext, precision=2, suppress_small=True)}
                """,
                style={'fontFamily': 'monospace','text-align': 'left'}
            )
        ], className='step-box'))

    if step >= 6:
        content.append(html.Div([
            html.H5("Passo 2: Geração do Erro Pequeno (Error)"),
            html.P(
                f"""
                error = {np.array2string(error, precision=2, suppress_small=True)}
                """,
                style={'fontFamily': 'monospace','text-align': 'left'}
            )
        ], className='step-box'))

    if step >= 7:
        content.append(html.Div([
            html.H5("Passo 3: Cálculo do Ciphertext"),
            html.P([
                "ciphertext = plaintext × U + error = ",html.Br(),  
                             f"{np.array2string(plaintext, precision=2)}× " 
                             f"{np.array2string(U, precision=2)} + " 
                             f"{np.array2string(error, precision=2)}",html.Br(),   
                             f"= {np.array2string(ciphertext, precision=2)}"
            ],
                style={'fontFamily': 'monospace','text-align': 'center'}
            )
        ], className='step-box'))
        
    return html.Div([
        
        html.H4("Passo a Passo", className="steps-title"),
        html.H4("Criptografia GGH"),
        *content], style={'marginTop': '5px'})


def ggh_encrypt(ggh_data, step):
     fig = go.Figure()
     
     step_vector_mapping = {
    5: [
        {'vector': np.dot(ggh_data['plaintext'], ggh_data['U']), 'color': 'green', 'dash': None, 'prefix': 'plaintext × U'},
    ],
    6: [
        {'vector': np.dot(ggh_data['plaintext'], ggh_data['U']), 'color': 'green', 'dash': None, 'prefix': 'plaintext × U'},
        {'vector': ggh_data['error'], 'color': 'orange', 'dash': None, 'prefix': 'Erro'},
    ],
    7: [
        {'vector': np.dot(ggh_data['plaintext'], ggh_data['U']), 'color': 'green', 'dash': None, 'prefix': 'plaintext × U'},
        {'vector': ggh_data['error'], 'color': 'orange', 'dash': None, 'prefix': 'Erro'},
        {'vector': ggh_data['ciphertext'], 'color': 'yellow', 'dash': None, 'prefix': 'Ciphertext'},
    ]

}
     vector_configs = step_vector_mapping.get(step, [])

     for config in vector_configs:
            vec = config['vector']
            fig.add_trace(go.Scatter(
                x=[0, vec[0]],
                y=[0, vec[1]],
                mode='lines+markers',
                line=dict(color=config['color'], dash=config['dash']),
                marker=dict(color=config['color']),
                name=config['prefix']
            ))       
     step_content = encrypt_step(ggh_data, step)

     return fig, step_content


def decrypt_step(ggh_data, step):
    ciphertext = np.array(ggh_data['ciphertext'])
    error = np.array(ggh_data['error'])
    U = np.array(ggh_data['U'])
    public_key_inverse = inv(U)
    
    content = []
    
    if step >= 8:
        content.append(html.Div([
            html.H5("Passo 1: Inversa da Chave Pública (U⁻¹)"),
                html.P([
                     html.H5("Public Key Inverse"),
                    f"U⁻¹ = {np.array2string(public_key_inverse, precision=2, suppress_small=True)}"]
                ,style={'fontFamily': 'monospace','textAlign': 'left'})
    ], className='step-box'))

    if step >= 9:
        decrypted_plaintext = np.dot(ciphertext, public_key_inverse)
        content.append(html.Div([
                            html.H5("Passo 2: Multiplicação do ciphertext pela inversa da chave pública"),
                            html.P([
                                
                                    f"ciphertext = {np.array2string(ciphertext, precision=2)}",html.Br(),
                                    f"U⁻¹ = {np.array2string(public_key_inverse, precision=2)}",html.Br(),
                                    html.H5("Decrypted Plaintext"),
                                    f"ciphertext × U⁻¹ = {np.array2string(decrypted_plaintext, precision=2)}"
                                    ],style={'fontFamily': 'monospace','textAlign': 'left'}
                            )
                        ], className="step-box"))

    if step >= 10:
        rounded_decrypted_plaintext = decrypted_plaintext - np.dot(error, public_key_inverse)
        content.append(html.Div([
            html.H5("Passo 3: Arredondamento de Babai (Remoção do Erro)"),

            html.Div([
                html.H6("Multiplicação do erro pela inversa da chave pública"),
                html.Pre(
                    f"error × U⁻¹ = {np.array2string(error, precision=2)} ×\n"
                    f"             {np.array2string(public_key_inverse, precision=2)}"
                )
            ], className="substep-box"),

            html.Div([
                html.H6("Subtração do erro decodificado do plaintext inicial"),
                html.P(
                    f"rounded_decrypted_plaintext = decrypted_plaintext - (error × U⁻¹)\n"
                    f"                           = {np.array2string(decrypted_plaintext, precision=2)} -\n"
                    f"                             <resultado acima>\n"
                    f"                           = {np.array2string(rounded_decrypted_plaintext, precision=2)}"
                )
            ], className="substep-box")

        ], className='step-box'))

    if step >= 11:
        temp = np.dot(rounded_decrypted_plaintext, public_key_inverse)
        recovered_plaintext = np.dot(temp, U)
        recovered_plaintext = np.round(recovered_plaintext).astype(int)

        content.append(html.Div([
            html.H5("Passo 4: Recuperação da Mensagem Original"),

            html.Div([
                html.H6("4.1 Multiplicar pela inversa da chave pública"),
                html.P(
                    f"temp = rounded_decrypted_plaintext × U⁻¹\n"
                    f"     = {np.array2string(rounded_decrypted_plaintext, precision=2)} ×\n"
                    f"       {np.array2string(public_key_inverse, precision=2)}\n"
                    f"     = {np.array2string(temp, precision=2)}"
                )
            ], className="substep-box"),

            html.Div([
                html.H6("4.2 Multiplicar por U e arredondar"),
                html.P(
                    f"plaintext = round(temp × U)\n"
                    f"         = round({np.array2string(temp, precision=2)} ×\n"
                    f"                 {np.array2string(U, precision=2)})\n"
                    f"         = {np.array2string(recovered_plaintext, precision=2)}"
                )
            ], className="substep-box")

        ], className='step-box'))

    return html.Div([
        html.H4("Passo a Passo", className="steps-title"),
        html.H4("Decriptografia GGH"),
        *content], style={'marginTop': '5px'})


def ggh_decrypt(ggh_data, step):
    fig = go.Figure()

    U = np.array(ggh_data['U'])
    public_key_inverse = inv(U)
    decrypted_plaintext = np.dot(ggh_data['ciphertext'], public_key_inverse)
    rounded_decrypted_plaintext = decrypted_plaintext - np.dot(ggh_data['error'], public_key_inverse)
    temp = np.dot(rounded_decrypted_plaintext, public_key_inverse)
    recovered_plaintext = np.round(np.dot(temp, U)).astype(int)
    
    step_vector_mapping = {
        8: [
            {'vector': ggh_data['ciphertext'], 'color': 'yellow', 'dash': None, 'prefix': 'Ciphertext'},
        ],
        9: [
            {'vector': ggh_data['ciphertext'], 'color': 'yellow', 'dash': None, 'prefix': 'Ciphertext'},
            {'vector': decrypted_plaintext, 'color': 'purple', 'dash': None, 'prefix': 'Decrypted'},
        ],
        10: [
            {'vector': ggh_data['ciphertext'], 'color': 'yellow', 'dash': None, 'prefix': 'Ciphertext'},
            {'vector': decrypted_plaintext, 'color': 'purple', 'dash': None, 'prefix': 'Decrypted'},
            {'vector': rounded_decrypted_plaintext, 'color': 'blue', 'dash': None, 'prefix': 'Rounded'},
        ],
        11: [
            {'vector': ggh_data['ciphertext'], 'color': 'yellow', 'dash': None, 'prefix': 'Ciphertext'},
            {'vector': recovered_plaintext, 'color': 'green', 'dash': None, 'prefix': 'Recovered'},
            {'vector': ggh_data['plaintext'], 'color': 'red', 'dash': None, 'prefix': 'Original'},
        ]
    }
    
    vector_configs = step_vector_mapping.get(step, [])
    
    for config in vector_configs:
        vec = config['vector']
        fig.add_trace(go.Scatter(
            x=[0, vec[0]],
            y=[0, vec[1]],
            mode='lines+markers',
            line=dict(color=config['color'], dash=config['dash']),
            marker=dict(color=config['color']),
            name=config['prefix']
        ))
    
    
    fig.update_layout(
        title="Visualização da Decriptografia GGH",
        xaxis_title="X",
        yaxis_title="Y",
        template = "plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    step_content = decrypt_step(ggh_data, step)
    
    return fig, step_content
   

