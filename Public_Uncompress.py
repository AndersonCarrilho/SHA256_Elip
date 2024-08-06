import ecdsa
from ecdsa import SECP256k1
from ecdsa.util import string_to_number

def modular_sqrt(a, p):
    """Compute the modular square root of a modulo p."""
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    raise NotImplementedError("This implementation only supports p % 4 == 3")

def compressed_to_uncompressed(pub_key_comp):
    # Remove any non-hex characters from the input and check length
    pub_key_comp = pub_key_comp.strip().replace(' ', '')
    if len(pub_key_comp) != 66:
        raise ValueError("Invalid length for compressed public key.")
    
    try:
        pub_key_comp = bytes.fromhex(pub_key_comp)
    except ValueError as e:
        raise ValueError("Invalid hexadecimal characters in public key.") from e
    
    assert len(pub_key_comp) == 33
    
    prefix = pub_key_comp[0]
    x = pub_key_comp[1:]
    
    # Initialize the curve
    curve = SECP256k1.curve
    p = SECP256k1.curve.p()
    
    # Compute y^2 = x^3 + 7 (for secp256k1)
    x_num = string_to_number(x)
    y_squared = (x_num**3 + 7) % p
    
    # Compute y from y_squared (y = sqrt(y_squared) mod p)
    y = modular_sqrt(y_squared, p)
    
    # Adjust y based on the prefix of the compressed key
    if prefix == 0x03 and y % 2 == 0:
        y = p - y
    elif prefix == 0x02 and y % 2 == 1:
        y = p - y
    
    # Convert y to bytes
    y_bytes = y.to_bytes(32, 'big')
    
    # Combine x and y
    pub_key_uncomp = b'\x04' + x + y_bytes
    
    # Convert coordinates to hex for display
    x_hex = x.hex()
    y_hex = y_bytes.hex()
    
    # Convert coordinates to decimal for display
    x_dec = int(x_hex, 16)
    y_dec = int(y_hex, 16)
    
    return pub_key_uncomp.hex(), x_hex, y_hex, x_dec, y_dec

# Solicitar chave pública compactada do usuário
pub_key_comp = input("Insira a chave pública compactada (66 caracteres hexadecimais): ")

try:
    pub_key_uncomp, x_hex, y_hex, x_dec, y_dec = compressed_to_uncompressed(pub_key_comp)
    print(f"Chave Pública Completa (não compactada): {pub_key_uncomp}")
    print(f"Coordenada X (hexadecimal): {x_hex}")
    print(f"Coordenada Y (hexadecimal): {y_hex}")
    print(f"Coordenada X (decimal): {x_dec}")
    print(f"Coordenada Y (decimal): {y_dec}")
except ValueError as e:
    print(f"Erro: {e}")
