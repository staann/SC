def vigenere_criptografar(texto, chave):
    if not chave:
        return texto
        
    resultado = []
    chave = chave.upper()
    indice_chave = 0

    for char in texto:
        if char.isalpha():
            # Calcula o deslocamento com base na letra da chave atual
            deslocamento = ord(chave[indice_chave % len(chave)]) - ord('A')
            
            # Define a base ASCII (maiúscula ou minúscula) para manter a formatação original
            base = ord('A') if char.isupper() else ord('a')
            
            # Aplica o deslocamento e volta ao formato de caractere
            novo_char = chr((ord(char) - base + deslocamento) % 26 + base)
            resultado.append(novo_char)
            
            # Avança o índice da chave apenas se processamos uma letra
            indice_chave += 1
        else:
            # Mantém espaços, números e pontuações inalterados
            resultado.append(char)

    return "".join(resultado)

def vigenere_descriptografar(texto, chave):
    if not chave:
        return texto
        
    resultado = []
    chave = chave.upper()
    indice_chave = 0

    for char in texto:
        if char.isalpha():
            # Calcula o deslocamento com base na letra da chave atual
            deslocamento = ord(chave[indice_chave % len(chave)]) - ord('A')
            
            # Define a base ASCII (maiúscula ou minúscula)
            base = ord('A') if char.isupper() else ord('a')
            
            # Subtrai o deslocamento para reverter a criptografia
            novo_char = chr((ord(char) - base - deslocamento) % 26 + base)
            resultado.append(novo_char)
            
            indice_chave += 1
        else:
            resultado.append(char)

    return "".join(resultado)

# --- Exemplo de Uso ---
if __name__ == "__main__":
    mensagem_original = "Ola, mundo! Esta e uma mensagem secreta."
    chave_secreta = "PYTHON"

    print("--- Cifra de Vigenère ---")
    print(f"Mensagem Original: {mensagem_original}")
    print(f"Chave: {chave_secreta}\n")

    # Criptografando
    mensagem_criptografada = vigenere_criptografar(mensagem_original, chave_secreta)
    print(f"Criptografado: {mensagem_criptografada}")

    # Descriptografando
    mensagem_descriptografada = vigenere_descriptografar(mensagem_criptografada, chave_secreta)
    print(f"Descriptografado: {mensagem_descriptografada}")