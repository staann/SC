import secrets
import math
import sys


def exp_mod(base: int, expoente: int, modulo: int) -> int:
    result = 1
    base %= modulo
    while expoente > 0:
        if expoente & 1:
            result = (result * base) % modulo
        base = (base * base) % modulo
        expoente >>= 1
    return result


def eh_primo(n: int, dec: int = 10) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def triagem(a: int) -> bool:
        x = exp_mod(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    for _ in range(dec):
        a = secrets.randbelow(n - 3) + 2
        if not triagem(a):
            return False
    return True


def gerar_primo(bits: int) -> int:
    candidate = secrets.randbits(bits - 2)
    candidate |= (1 << (bits - 2)) | 1
    return candidate


def gerar_primo_deguro(bits: int) -> tuple[int, int]:
    while True:
        q = gerar_primo(bits - 1)
        if not eh_primo(q):
            continue
        p = 2 * q + 1
        if eh_primo(p):
            return p, q


def prime_factors(n: int) -> list[int]:
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def achar_raiz_primitiva(p: int, factors: list[int]) -> int:
    for g in range(2, p):
        valid = True
        for q in factors:
            if exp_mod(g, (p - 1) // q, p) == 1:
                valid = False
                break
        if valid:
            return g
    raise ValueError("Não foi possível encontrar raiz primitiva")


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def inverso_mod(a: int, m: int) -> int:
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("Inverso modular não existe")
    return x % m


def splitar_msg(message: bytes, max_block_size: int) -> list[int]:
    blocos = []
    for i in range(0, len(message), max_block_size):
        block = message[i : i + max_block_size]
        blocos.append(int.from_bytes(block, "big"))
    return blocos


def codificar_msg(message: str, modulo: int) -> tuple[list[int], int]:
    data = message.encode("utf-8")
    max_bytes = (modulo.bit_length() - 1) // 8
    if max_bytes < 1:
        raise ValueError("Módulo muito pequeno para codificar mensagem")
    blocos = splitar_msg(data, max_bytes)
    if any(block >= modulo for block in blocos):
        raise ValueError("Mensagem não cabe no módulo calculado")
    return blocos, max_bytes


def decodificar_msg(blocos: list[int], block_size: int) -> str:
    data = b"".join(b.to_bytes(block_size, "big") for b in blocos)
    return data.lstrip(b"\x00").decode("utf-8", errors="replace")


def gerar_chave(p: int, g: int) -> tuple[int, int]:
    private = secrets.randbelow(p - 3) + 2
    public = exp_mod(g, private, p)
    return private, public


def elgamal_encrypt(msg_em_bloco: list[int], p: int, g: int, y: int) -> tuple[int, list[int]]:
    k = secrets.randbelow(p - 3) + 2
    c1 = exp_mod(g, k, p)
    c2_blocos = [(block * exp_mod(y, k, p)) % p for block in msg_em_bloco]
    return c1, c2_blocos


def elgamal_decrypt(c1: int, c2_blocos: list[int], p: int, x: int) -> list[int]:
    s = exp_mod(c1, x, p)
    inv_s = inverso_mod(s, p)
    return [(c2 * inv_s) % p for c2 in c2_blocos]


def rodar(bits: int = 256) -> None:
    print(" Simulação Diffie-Hellman + ElGamal ")
    print(f"Gerando primo seguro de {bits} bits...")
    p, q = gerar_primo_deguro(bits)
    print("Primo p gerado")
    print(f"p = {p}")

    factors = [2, q]
    print(f"Fatores primos de p-1: {factors}")

    g = achar_raiz_primitiva(p, factors)
    print(f"Raiz primitiva g = {g}")

    print("\nSimulando o participante B gerando sua chave privada e pública")
    x, y = gerar_chave(p, g)
    print(f"Chave privada de B x = {x}")
    print(f"Chave pública de B y = {y}")

    if sys.stdin.isatty():
        message = input("Digite a mensagem a ser enviada de A para B: ")
    else:
        message = "Mensagem secreta de teste"
    print(f"Mensagem original: {message}")

    blocos, block_size = codificar_msg(message, p)
    print(f"Mensagem dividida em {len(blocos)} bloco(s)")

    c1, c2_blocos = elgamal_encrypt(blocos, p, g, y)
    print("\nTexto cifrado enviado de A para B:")
    print(f"c1 = {c1}")
    print(f"c2 blocos = {c2_blocos}")

    decrypted_blocos = elgamal_decrypt(c1, c2_blocos, p, x)
    decrypted = decodificar_msg(decrypted_blocos, block_size)
    print("\nB descriptografou a mensagem:")
    print(decrypted)

    print("\nVerificação:")
    print("Mensagem original e descriptografada correspondem?", decrypted == message)


if __name__ == "__main__":
    rodar(bits=256)
