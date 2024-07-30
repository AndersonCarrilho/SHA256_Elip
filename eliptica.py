def mod_add(a, b, p):
    """ Adiciona dois números no campo finito definido por p """
    result = (a + b) % p
    print(f"mod_add: ({a} + {b}) % {p} = {result}")
    return result

def mod_sub(a, b, p):
    """ Subtrai dois números no campo finito definido por p """
    result = (a - b) % p
    print(f"mod_sub: ({a} - {b}) % {p} = {result}")
    return result

def mod_mul(a, b, p):
    """ Multiplica dois números no campo finito definido por p """
    result = (a * b) % p
    print(f"mod_mul: ({a} * {b}) % {p} = {result}")
    return result

def mod_inv(a, p):
    """ Calcula o inverso modular de a no campo finito definido por p """
    result = pow(a, p - 2, p)
    print(f"mod_inv: inverso modular de {a} no campo {p} = {result}")
    return result

def mod_div(a, b, p):
    """ Divide dois números no campo finito definido por p """
    b_inv = mod_inv(b, p)
    result = mod_mul(a, b_inv, p)
    print(f"mod_div: ({a} / {b}) % {p} = {result}")
    return result

# Parâmetros da curva secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (Gx, Gy)

def point_addition(P, Q):
    """ Soma dois pontos na curva elíptica secp256k1 """
    Px, Py = P
    Qx, Qy = Q
    
    print(f"point_addition: P = {P}, Q = {Q}")
    
    if P == (0, 0):
        print(f"P é o ponto no infinito, retorno Q = {Q}")
        return Q
    if Q == (0, 0):
        print(f"Q é o ponto no infinito, retorno P = {P}")
        return P
    if P == Q:
        return point_doubling(P)
    
    if Px == Qx and Py == -Qy % p:
        print(f"P e Q são opostos, retorno ponto no infinito")
        return (0, 0)
    
    m = mod_div(mod_sub(Qy, Py, p), mod_sub(Qx, Px, p), p)
    Rx = mod_sub(mod_sub(mod_mul(m, m, p), Px, p), Qx, p)
    Ry = mod_sub(mod_mul(m, mod_sub(Px, Rx, p), p), Py, p)
    
    print(f"m = {m}")
    print(f"Rx = {Rx}, Ry = {Ry}")
    
    return (Rx, Ry)

def point_doubling(P):
    """ Duplicação de um ponto na curva elíptica secp256k1 """
    Px, Py = P
    print(f"point_doubling: P = {P}")
    
    m = mod_div(mod_add(mod_mul(3, mod_mul(Px, Px, p), p), a, p), mod_mul(2, Py, p), p)
    Rx = mod_sub(mod_mul(m, m, p), mod_mul(2, Px, p), p)
    Ry = mod_sub(mod_mul(m, mod_sub(Px, Rx, p), p), Py, p)
    
    print(f"m = {m}")
    print(f"Rx = {Rx}, Ry = {Ry}")
    
    return (Rx, Ry)

def scalar_multiplication(k, P):
    """ Multiplicação escalar de um ponto na curva elíptica secp256k1 """
    Q = (0, 0)
    print(f"scalar_multiplication: k = {k}, P = {P}")
    
    while k:
        if k & 1:
            print(f"Adicionando {Q} e {P}")
            Q = point_addition(Q, P)
        print(f"Dobrando ponto {P}")
        P = point_doubling(P)
        k >>= 1
    
    print(f"Resultado da multiplicação escalar: {Q}")
    return Q

def private_key_to_public_key(private_key):
    """ Gera a chave pública a partir da chave privada usando secp256k1 """
    print(f"Gerando chave pública a partir da chave privada {private_key}")
    public_key = scalar_multiplication(private_key, G)
    return public_key

def main():
    # Solicita a chave privada ao usuário
    private_key_input = input("Digite a chave privada em hexadecimal (ex: 1E99423A4ED27608A15A2616DFA21C16C2345D7E38FD9C76A7EFD470F2E6B815): ")
    
    try:
        # Converte a entrada do usuário para um inteiro
        private_key = int(private_key_input, 16)
        
        # Gera a chave pública
        public_key = private_key_to_public_key(private_key)
        
        # Exibe a chave pública
        print(f"Chave Pública: {public_key}")
    
    except ValueError:
        print("Entrada inválida. Certifique-se de fornecer a chave privada como um número hexadecimal.")

if __name__ == "__main__":
    main()
