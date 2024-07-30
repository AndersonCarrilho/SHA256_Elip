import time
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()

# Função utilitária de rotação à direita
def right_rotate(value, amount):
    return ((value >> amount) | (value << (32 - amount))) & 0xFFFFFFFF

# Implementação da função SHA-256
def sha256(message):
    # Constantes da especificação SHA-256
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    # Estados iniciais do SHA-256
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    logger.debug("1. Preprocessamento: Padding da mensagem.")
    original_length = len(message) * 8
    message = bytearray(message, 'ascii')
    message.append(0x80)  # Adiciona o bit '1'
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0)
    message += original_length.to_bytes(8, 'big')
    logger.debug(f"Mensagem após padding: {message.hex()}")
    time.sleep(1)

    logger.debug("2. Divisão da mensagem em blocos de 512 bits.")
    for i in range(0, len(message), 64):
        chunk = message[i:i + 64]
        logger.debug(f"Bloco {i//64 + 1}: {chunk.hex()}")
        time.sleep(1)

        w = [0] * 64
        for j in range(16):
            w[j] = int.from_bytes(chunk[j * 4:j * 4 + 4], 'big')
        logger.debug(f"Palavras iniciais: {[f'{word:08x}' for word in w[:16]]}")
        time.sleep(1)

        logger.debug("3. Expansão das palavras para 64 entradas.")
        for j in range(16, 64):
            s0 = right_rotate(w[j - 15], 7) ^ right_rotate(w[j - 15], 18) ^ (w[j - 15] >> 3)
            s1 = right_rotate(w[j - 2], 17) ^ right_rotate(w[j - 2], 19) ^ (w[j - 2] >> 10)
            w[j] = (w[j - 16] + s0 + w[j - 7] + s1) & 0xFFFFFFFF
        logger.debug(f"Palavras expandidas: {[f'{word:08x}' for word in w]}")
        time.sleep(1)

        logger.debug("4. Inicialização dos registradores de trabalho.")
        a, b, c, d, e, f, g, h = H
        logger.debug(f"Estados iniciais: a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}, e={e:08x}, f={f:08x}, g={g:08x}, h={h:08x}")
        time.sleep(1)

        logger.debug("5. Compressão principal.")
        for j in range(64):
            s1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + s1 + ch + K[j] + w[j]) & 0xFFFFFFFF
            s0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

            logger.debug(f"Iteração {j + 1}: a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}, e={e:08x}, f={f:08x}, g={g:08x}, h={h:08x}")
            time.sleep(1)

        logger.debug("6. Atualização dos estados.")
        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

        logger.debug(f"Estados atualizados: {H}")
        time.sleep(1)

    # Produz o hash final concatenando os valores de H
    final_hash = ''.join(f'{h:08x}' for h in H)
    logger.debug(f"7. Hash final: {final_hash}")
    return final_hash

if __name__ == "__main__":
    message = input("Digite a mensagem para hash: ")
    print(f"SHA-256: {sha256(message)}")
