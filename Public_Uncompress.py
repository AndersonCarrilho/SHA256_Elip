import time
import ecdsa
from ecdsa import SECP256k1
from ecdsa.util import string_to_number

def modular_sqrt(a, p):
    """Compute the modular square root of a modulo p."""
    print(f"Calculando a raiz quadrada modular de {a} módulo {p}...")
    time.sleep(0.5)
    if p % 4 == 3:
        result = pow(a, (p + 1) // 4, p)
        print(f"Raiz quadrada modular resultante: {result}")
        time.sleep(0.5)
        return result
    raise NotImplementedError("Esta implementação suporta apenas p % 4 == 3")

def compressed_to_uncompressed(pub_key_comp):
    print("Recebendo chave pública compactada e removendo quaisquer caracteres não-hexadecimais...")
    time.sleep(0.5)
    pub_key_comp = pub_key_comp.strip().replace(' ', '')
    print(f"Chave pública compactada limpa: {pub_key_comp}")
    time.sleep(0.5)
    
    if len(pub_key_comp) != 66:
        raise ValueError("Comprimento inválido para chave pública compactada.")
    
    print("Convertendo chave pública compactada de hexadecimal para bytes...")
    time.sleep(0.5)
    try:
        pub_key_comp = bytes.fromhex(pub_key_comp)
        print(f"Chave pública compactada em bytes: {pub_key_comp}")
        time.sleep(0.5)
    except ValueError as e:
        raise ValueError("Caracteres hexadecimais inválidos na chave pública.") from e
    
    assert len(pub_key_comp) == 33
    
    print("Extraindo prefixo e coordenada X da chave pública compactada...")
    time.sleep(0.5)
    prefix = pub_key_comp[0]
    x = pub_key_comp[1:]
    print(f"Prefixo: {prefix}")
    print(f"Coordenada X (bytes): {x}")
    time.sleep(0.5)
    
    print("Inicializando a curva SECP256k1...")
    time.sleep(0.5)
    curve = SECP256k1.curve
    p = SECP256k1.curve.p()
    print(f"Parâmetro p da curva: {p}")
    time.sleep(0.5)
    
    print("Calculando y^2 = x^3 + 7 (para secp256k1)...")
    time.sleep(0.5)
    x_num = string_to_number(x)
    print(f"Coordenada X em número: {x_num}")
    y_squared = (x_num**3 + 7) % p
    print(f"y^2 calculado: {y_squared}")
    time.sleep(0.5)
    
    print("Calculando y a partir de y^2 (y = sqrt(y_squared) mod p)...")
    time.sleep(0.5)
    y = modular_sqrt(y_squared, p)
    print(f"Coordenada Y calculada: {y}")
    time.sleep(0.5)
    
    print("Ajustando y com base no prefixo da chave compactada...")
    time.sleep(0.5)
    if prefix == 0x03 and y % 2 == 0:
        y = p - y
    elif prefix == 0x02 and y % 2 == 1:
        y = p - y
    print(f"Coordenada Y ajustada: {y}")
    time.sleep(0.5)
    
    print("Convertendo y para bytes...")
    time.sleep(0.5)
    y_bytes = y.to_bytes(32, 'big')
    print(f"Coordenada Y em bytes: {y_bytes}")
    time.sleep(0.5)
    
    print("Combinando x e y para formar a chave pública completa...")
    time.sleep(0.5)
    pub_key_uncomp = b'\x04' + x + y_bytes
    print(f"Chave pública completa (bytes): {pub_key_uncomp}")
    time.sleep(0.5)
    
    print("Convertendo coordenadas para hexadecimal para exibição...")
    time.sleep(0.5)
    x_hex = x.hex()
    y_hex = y_bytes.hex()
    print(f"Coordenada X (hexadecimal): {x_hex}")
    print(f"Coordenada Y (hexadecimal): {y_hex}")
    time.sleep(0.5)
    
    print("Convertendo coordenadas para decimal para exibição...")
    time.sleep(0.5)
    x_dec = int(x_hex, 16)
    y_dec = int(y_hex, 16)
    print(f"Coordenada X (decimal): {x_dec}")
    print(f"Coordenada Y (decimal): {y_dec}")
    time.sleep(0.5)
    
    return pub_key_uncomp.hex(), x_hex, y_hex, x_dec, y_dec

# Solicitar chave pública compactada do usuário
pub_key_comp = input("Insira a chave pública compactada (66 caracteres hexadecimais): ")

try:
    print("Iniciando o processo de descompactação da chave pública...")
    time.sleep(0.5)
    pub_key_uncomp, x_hex, y_hex, x_dec, y_dec = compressed_to_uncompressed(pub_key_comp)
    print(f"Chave Pública Completa (não compactada): {pub_key_uncomp}")
    print(f"Coordenada X (hexadecimal): {x_hex}")
    print(f"Coordenada Y (hexadecimal): {y_hex}")
    print(f"Coordenada X (decimal): {x_dec}")
    print(f"Coordenada Y (decimal): {y_dec}")
except ValueError as e:
    print(f"Erro: {e}")
