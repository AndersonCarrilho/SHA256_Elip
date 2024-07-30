import time
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()

# Constantes RIPEMD-160
K1 = [
    0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E
]

K2 = [
    0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000
]

# Funções de rotação à esquerda
def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

# Funções de compressão F, G, H, I, J
def F(x, y, z):
    return x ^ y ^ z

def G(x, y, z):
    return (x & y) | (~x & z)

def H(x, y, z):
    return (x | ~y) ^ z

def I(x, y, z):
    return (x & z) | (y & ~z)

def J(x, y, z):
    return x ^ (y | ~z)

# Implementação da função RIPEMD-160
def ripemd160(message):
    # Estados iniciais
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    logger.debug("1. Preprocessamento: Padding da mensagem.")
    original_length = len(message) * 8
    message = bytearray(message, 'ascii')
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0)
    message += original_length.to_bytes(8, 'little')
    logger.debug(f"Mensagem após padding: {message.hex()}")
    time.sleep(1)

    logger.debug("2. Divisão da mensagem em blocos de 512 bits.")
    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        logger.debug(f"Bloco {i//64 + 1}: {block.hex()}")
        time.sleep(1)

        x = [int.from_bytes(block[j * 4:j * 4 + 4], 'little') for j in range(16)]
        logger.debug(f"Palavras do bloco: {[f'{word:08x}' for word in x]}")
        time.sleep(1)

        logger.debug("3. Inicialização dos valores de trabalho.")
        a, b, c, d, e = h0, h1, h2, h3, h4
        aa, bb, cc, dd, ee = h0, h1, h2, h3, h4
        logger.debug(f"Valores de trabalho: a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}, e={e:08x}")
        time.sleep(1)

        logger.debug("4. Transformação principal.")
        for j in range(80):
            if 0 <= j <= 15:
                round_func = F
                s = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8][j]
                k = K1[0]
                ki = K2[4 - (j // 16)]
            elif 16 <= j <= 31:
                round_func = G
                s = [7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12][j - 16]
                k = K1[1]
                ki = K2[3 - ((j - 16) // 16)]
            elif 32 <= j <= 47:
                round_func = H
                s = [11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5][j - 32]
                k = K1[2]
                ki = K2[2 - ((j - 32) // 16)]
            elif 48 <= j <= 63:
                round_func = I
                s = [9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6][j - 48]
                k = K1[3]
                ki = K2[1 - ((j - 48) // 16)]
            elif 64 <= j <= 79:
                round_func = J
                s = [8, 6, 4, 1, 3, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8, 5][j - 64]
                k = K1[4]
                ki = K2[0]

            t = (left_rotate(a + round_func(b, c, d) + x[j % 16] + k, s) + e) & 0xFFFFFFFF
            a, b, c, d, e = e, a, left_rotate(b, 10), c, d

            tt = (left_rotate(aa + round_func(bb, cc, dd) + x[(j * 7) % 16] + ki, s) + ee) & 0xFFFFFFFF
            aa, bb, cc, dd, ee = ee, aa, left_rotate(bb, 10), cc, dd

            logger.debug(f"Iteração {j + 1}: a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}, e={e:08x}")
            logger.debug(f"Iteração {j + 1}: aa={aa:08x}, bb={bb:08x}, cc={cc:08x}, dd={dd:08x}, ee={ee:08x}")
            time.sleep(1)

        logger.debug("5. Atualização dos estados.")
        t = (h1 + c + dd) & 0xFFFFFFFF
        h1 = (h2 + d + ee) & 0xFFFFFFFF
        h2 = (h3 + e + aa) & 0xFFFFFFFF
        h3 = (h4 + a + bb) & 0xFFFFFFFF
        h4 = (h0 + b + cc) & 0xFFFFFFFF
        h0 = t

        logger.debug(f"Estados atualizados: h0={h0:08x}, h1={h1:08x}, h2={h2:08x}, h3={h3:08x}, h4={h4:08x}")
        time.sleep(1)

    # Produz o hash final concatenando os valores de H
    final_hash = ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4])
    logger.debug(f"6. Hash final: {final_hash}")
    return final_hash

if __name__ == "__main__":
    message = input("Digite a mensagem para hash: ")
    print(f"RIPEMD-160: {ripemd160(message)}")
