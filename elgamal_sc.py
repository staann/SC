import secrets
import math
import sys


def pow_mod(base: int, exponent: int, modulus: int) -> int:
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result


def is_prime(n: int, witnesses: int = 10) -> bool:
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

    def trial(a: int) -> bool:
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    for _ in range(witnesses):
        a = secrets.randbelow(n - 3) + 2
        if not trial(a):
            return False
    return True


def generate_prime_candidate(bits: int) -> int:
    candidate = secrets.randbits(bits - 2)
    candidate |= (1 << (bits - 2)) | 1
    return candidate


def generate_safe_prime(bits: int) -> tuple[int, int]:
    while True:
        q = generate_prime_candidate(bits - 1)
        if not is_prime(q):
            continue
        p = 2 * q + 1
        if is_prime(p):
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


def find_primitive_root(p: int, factors: list[int]) -> int:
    for g in range(2, p):
        valid = True
        for q in factors:
            if pow_mod(g, (p - 1) // q, p) == 1:
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


def mod_inverse(a: int, m: int) -> int:
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("Inverso modular não existe")
    return x % m


def split_message(message: bytes, max_block_size: int) -> list[int]:
    blocks = []
    for i in range(0, len(message), max_block_size):
        block = message[i : i + max_block_size]
        blocks.append(int.from_bytes(block, "big"))
    return blocks


def encode_message(message: str, modulus: int) -> tuple[list[int], int]:
    data = message.encode("utf-8")
    max_bytes = (modulus.bit_length() - 1) // 8
    if max_bytes < 1:
        raise ValueError("Módulo muito pequeno para codificar mensagem")
    blocks = split_message(data, max_bytes)
    if any(block >= modulus for block in blocks):
        raise ValueError("Mensagem não cabe no módulo calculado")
    return blocks, max_bytes


def decode_message(blocks: list[int], block_size: int) -> str:
    data = b"".join(b.to_bytes(block_size, "big") for b in blocks)
    return data.lstrip(b"\x00").decode("utf-8", errors="replace")


def generate_keys(p: int, g: int) -> tuple[int, int]:
    private = secrets.randbelow(p - 3) + 2
    public = pow_mod(g, private, p)
    return private, public


def elgamal_encrypt(message_blocks: list[int], p: int, g: int, y: int) -> tuple[int, list[int]]:
    k = secrets.randbelow(p - 3) + 2
    c1 = pow_mod(g, k, p)
    c2_blocks = [(block * pow_mod(y, k, p)) % p for block in message_blocks]
    return c1, c2_blocks


def elgamal_decrypt(c1: int, c2_blocks: list[int], p: int, x: int) -> list[int]:
    s = pow_mod(c1, x, p)
    inv_s = mod_inverse(s, p)
    return [(c2 * inv_s) % p for c2 in c2_blocks]


def run_demo(bits: int = 256) -> None:
    print("*** Simulação Diffie-Hellman + ElGamal ***")
    print(f"Gerando primo seguro de {bits} bits...")
    p, q = generate_safe_prime(bits)
    print("Primo p gerado")
    print(f"p = {p}")

    factors = [2, q]
    print(f"Fatores primos de p-1: {factors}")

    g = find_primitive_root(p, factors)
    print(f"Raiz primitiva g = {g}")

    print("\nSimulando o participante B gerando sua chave privada e pública...")
    x, y = generate_keys(p, g)
    print(f"Chave privada de B x = {x}")
    print(f"Chave pública de B y = {y}")

    if sys.stdin.isatty():
        message = input("Digite a mensagem a ser enviada de A para B: ")
    else:
        message = "Mensagem secreta de teste"
    print(f"Mensagem original: {message}")

    blocks, block_size = encode_message(message, p)
    print(f"Mensagem dividida em {len(blocks)} bloco(s)")

    c1, c2_blocks = elgamal_encrypt(blocks, p, g, y)
    print("\nTexto cifrado enviado de A para B:")
    print(f"c1 = {c1}")
    print(f"c2 blocks = {c2_blocks}")

    decrypted_blocks = elgamal_decrypt(c1, c2_blocks, p, x)
    decrypted = decode_message(decrypted_blocks, block_size)
    print("\nB descriptografou a mensagem:")
    print(decrypted)

    print("\nVerificação:")
    print("Mensagem original e descriptografada correspondem?", decrypted == message)


if __name__ == "__main__":
    run_demo(bits=256)
