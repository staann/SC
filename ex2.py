import string

alfabeto = string.ascii_lowercase

textoCifrado = input("Digite o Texto Cifrado: ").lower()

textoDecifrado = ''

#Codificação
for i in range(len(alfabeto)):
    for letra in textoCifrado:
        if letra in alfabeto:
            indice = alfabeto.index(letra)
            novo_indice = (indice - i) % 26
            textoDecifrado += alfabeto[novo_indice]
        else:
            textoDecifrado += letra

    print(f"Tentativa {i}: ", textoDecifrado)
    textoDecifrado = ''





#Resultados
print("Texto Cifrado:", textoCifrado)
#print("Texto Decodificado:", textoDecifrado)