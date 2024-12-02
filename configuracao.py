from utils import clear_terminal

class Configuracao:
    def __init__(self):
        self.saldo_inicial = 0
        self.salario = 0
        self.max_rodadas = 0

    def configurar(self):
        print("\n--- Configurações Iniciais ---")

        while True:
            try:
                self.saldo_inicial = int(input("Digite o saldo inicial dos jogadores: "))
                if self.saldo_inicial > 0:
                    break
                else:
                    print("O saldo inicial deve ser maior que zero.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        while True:
            try:
                self.salario = int(input("Digite o salário dos jogadores: "))
                if self.salario > 0:
                    break
                else:
                    print("O salário deve ser maior que zero.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        while True:
            try:
                self.max_rodadas = int(input("Digite o número máximo de rodadas: "))
                if self.max_rodadas > 0:
                    break
                else:
                    print("O número de rodadas deve ser maior que zero.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
        clear_terminal()
        print("Configurações definidas com sucesso!")