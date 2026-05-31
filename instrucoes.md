Instruções de Execução 

Pré-requisitos: 

Python 3.10 ou superior (o código usa sintaxe tuple[int, int] nos type hints) 

Nenhuma dependência externa — apenas bibliotecas padrão do Python 

Execução padrão (modo interativo): 

python elgamal_sc.py 

O programa pedirá que você digite a mensagem a ser cifrada. Após a entrada, exibirá os parâmetros gerados, o texto cifrado e a mensagem decifrada por B. 

Execução não-interativa (stdin): 

echo "Minha mensagem secreta" | python elgamal_sc.py 

Quando o stdin não é um terminal (pipe ou redirecionamento), o programa usa automaticamente a mensagem padrão de teste definida no código. 

Observação sobre desempenho: 

A geração do primo seguro de 256 bits pode levar entre 1 e 30 segundos dependendo da máquina, pois depende de encontrar um par (q, p) onde ambos sejam primos. Esse comportamento é esperado e não indica erro. 