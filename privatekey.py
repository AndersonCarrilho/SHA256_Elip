import time
import logging
import random

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()

# Alfabeto Base58
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def int_to_base58(n):
    logger.debug("4. Iniciando a conversão para Base58.")
    result = ''
    while n > 0:
        n, remainder = divmod(n, 58)
        result = BASE58_ALPHABET[remainder] + result
        logger.debug(f"Resto: {remainder}, Quociente: {n}, Resultado Parcial: {result}")
        time.sleep(1)
    return result

def big_integer_to_representations(big_int):
    logger.debug(f"1. Número inteiro grande: {big_int}")
    time.sleep(1)
    
    # Convertendo para hexadecimal
    hex_rep = hex(big_int)[2:].zfill(64)  # Remove o '0x' e garante 64 caracteres
    logger.debug(f"2. Representação hexadecimal: {hex_rep}")
    time.sleep(1)

    # Convertendo para Base58
    base58_rep = int_to_base58(big_int)
    logger.debug(f"5. Representação Base58: {base58_rep}")
    time.sleep(1)
    
    return big_int, hex_rep, base58_rep

if __name__ == "__main__":
    # Gerando uma chave privada de 256 bits
    private_key = random.getrandbits(256)
    
    decimal_rep, hex_rep, base58_rep = big_integer_to_representations(private_key)
    print(f"Decimal: {decimal_rep}")
    print(f"Hexadecimal: {hex_rep}")
    print(f"Base58: {base58_rep}")
