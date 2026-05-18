import string

alfabeto = string.ascii_lowercase

textoClaro = input("Digite o Texto Claro: ").lower()
chave = int(input("Digite a Chave: "))

textoCifrado = ''
textoDecifrado = ''

# Codificação
for letra in textoClaro:
    if letra in alfabeto:
        indice = alfabeto.index(letra)
        novo_indice = (indice + chave) % 26
        textoCifrado += alfabeto[novo_indice]
    else:
        textoCifrado += letra

# Decodificação
for letra in textoCifrado:
    if letra in alfabeto:
        indice = alfabeto.index(letra)
        novo_indice = (indice - chave) % 26
        textoDecifrado += alfabeto[novo_indice]
    else:
        textoDecifrado += letra

# Resultados
print("Texto Claro:", textoClaro)
print("Texto Cifrado:", textoCifrado)
print("Texto Decodificado:", textoDecifrado)