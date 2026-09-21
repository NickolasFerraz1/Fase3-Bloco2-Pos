import sys


def main():
    print("Iniciando validação de ambiente")

    version = sys.version_info
    print(f"Versão do Python: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Erro: A versão do Python deve ser 3.8 ou superior.")
        sys.exit(1)
    print("Validação de ambiente concluída com sucesso.")
    sys.exit(0)

if __name__ == "__main__":
    main()