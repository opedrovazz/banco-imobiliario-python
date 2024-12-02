import random
from utils import clear_terminal
from sorte_reves import SorteReves
sr = SorteReves()
import re


class Jogador:
    def __init__(self, nome, saldo_inicial, salario):
        self.nome = nome
        self.saldo = saldo_inicial
        self.salario = salario
        self.posicao = None
        self.propriedades = []
        self.rodadas_preso = 0

    def __str__(self):
        propriedades = [casa.nome for casa in self.propriedades] if self.propriedades else "Nenhuma"
        return (f"Nome: {self.nome}, Saldo: R${self.saldo}, "
                f"Posição: {self.posicao.tipo if self.posicao else 'Não iniciado'}, "
                f"Propriedades: {propriedades}")
    
    def mover(self, dado):
        if self.rodadas_preso > 0:
            self.rodadas_preso -= 1
            print(f"{self.nome} está preso e não pode se mover. Faltam {self.rodadas_preso} rodadas.")
            return

        print(f"{self.nome} rolou o dado e tirou {dado}. Está na casa '{self.posicao.nome}'.")

        self.posicao.jogadores_presentes.remove(self)

        for _ in range(dado):
            self.posicao = self.posicao.proxima

            if self.posicao.tipo == "Início":
                self.saldo += self.salario
                print(f"{self.nome} passou pela casa 'Início' e recebeu R${self.salario} de salário.")

        self.posicao.jogadores_presentes.append(self)

        print(f"{self.nome} agora está na casa '{self.posicao.nome}' ({self.posicao.tipo}).")

    def verificar_bonus_grupo(self, grupo, proprietario):
        atual = self.posicao
        inicio = atual
        while True:
            if atual.grupo == grupo and atual.proprietario != proprietario:
                return False
            atual = atual.proxima
            if atual == inicio:
                break
        return True

    def interagir_com_casa(self):
        casa = self.posicao

        if casa.tipo == "Início":
            print(f"{self.nome} passou pela casa 'Início' e recebeu R${self.salario}.")
            self.saldo += self.salario

        elif casa.tipo == "Imóvel":
            if casa.proprietario is None:
                print(f"Você está na casa '{casa.nome}', disponível para compra!")
                print(f"Preço: R${casa.valor}, Aluguel: R${casa.aluguel}.")
                if self.saldo >= casa.valor:
                    escolha = input("Deseja comprar este imóvel? ('s' para sim, 'n' para não): ").strip().lower()
                    if escolha == "s":
                        self.saldo -= casa.valor
                        casa.proprietario = self
                        self.propriedades.append(casa)
                        print(f"Parabéns, {self.nome}! Você comprou o imóvel '{casa.nome}' por R${casa.valor}.")
                    elif escolha == "n":
                        print(f"Você decidiu não comprar o imóvel '{casa.nome}'.")
                    else:
                        print(f"Opção invalida, cancelando...")
                else:
                    print(f"Saldo insuficiente para comprar o imóvel '{casa.nome}'.")
            elif casa.proprietario != self:
                bonus = 0
                if self.verificar_bonus_grupo(casa.grupo, casa.proprietario):
                    bonus = casa.grupo.bonus


                aluguel_com_bonus = casa.aluguel + int(casa.aluguel * (bonus / 100))

                if self.saldo >= aluguel_com_bonus:
                    self.saldo -= aluguel_com_bonus
                    casa.proprietario.saldo += aluguel_com_bonus
                    print(f"{self.nome} pagou R${aluguel_com_bonus} de aluguel (incluindo bônus de {bonus}%) para {casa.proprietario.nome} pelo imóvel '{casa.nome}'.")
                else:
                    print(f"Saldo insuficiente, {self.nome}. Você não conseguiu pagar o aluguel de '{casa.nome}'.")


        elif casa.tipo == "Vá para a Prisão":
            atual = casa
            while atual.tipo != "Prisão":
                atual = atual.proxima

            print(f"{self.nome} caiu na casa 'Vá para a Prisão' e será movido diretamente para 'Prisão'.")

            casa.jogadores_presentes.remove(self)
            atual.jogadores_presentes.append(self)

            self.posicao = atual
            self.rodadas_preso = 2

            print(f"{self.nome} foi preso! Ficará 2 rodadas sem jogar.")


        elif casa.tipo == "Prisão":
            if self.rodadas_preso > 0:
                print(f"{self.nome} está preso! Faltam {self.rodadas_preso} rodadas para sair.")
            else:
                print(f"{self.nome} está apenas visitando a prisão. Nada acontece.")

        elif casa.tipo == "Sorte-Reves":
            carta = sr.sortear_sorte() if random.choice(["sorte", "reves"]) == "sorte" else sr.sortear_reves()
            print(f"{self.nome} caiu em uma casa de Sorte ou Revés!")
            print(f"Efeito: {carta}")
            self.aplicar_efeito_sorte_reves(carta)

        elif casa.tipo == "Especial":
            print(f"{self.nome} caiu em '{casa.nome}'. Nada acontece.")

    def aplicar_efeito_sorte_reves(self, carta):
        if "Receba" in carta:
            valor = int(re.search(r"R\$(\d+)", carta).group(1))
            self.saldo += valor
            print(f"{self.nome} recebeu R${valor}. Novo saldo: R${self.saldo}.")
        elif "Pague" in carta:
            valor = int(re.search(r"R\$(\d+)", carta).group(1))
            self.saldo -= valor
            print(f"{self.nome} pagou R${valor}. Novo saldo: R${self.saldo}.")

class GerenciadorDeJogadores:
    def __init__(self):
        self.jogadores = []

    def cadastrar_jogador(self, nome, saldo_inicial, salario):
        if len(self.jogadores) >= 6:
            print("Limite máximo de 6 jogadores atingido!")
            return

        for jogador in self.jogadores:
            if jogador.nome.lower() == nome.lower():
                print(f"Erro: Já existe um jogador com o nome '{nome}'. Escolha outro nome.")
                return

        novo_jogador = Jogador(nome, saldo_inicial, salario)
        self.jogadores.append(novo_jogador)
        print(f"Jogador '{nome}' cadastrado com sucesso!")

    def listar_jogadores(self):
        print("\n--- Lista de Jogadores ---")
        for i, jogador in enumerate(self.jogadores, start=1):
            print(f"{i}. {jogador.nome}")
        print("-" * 30)

    def selecionar_jogador(self):
        if not self.jogadores:
            print("Nenhum jogador cadastrado.")
            return None
        self.listar_jogadores()
        while True:
            try:
                opcao = int(input("Escolha o número do jogador: ")) - 1
                if 0 <= opcao < len(self.jogadores):
                    return self.jogadores[opcao]
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

    def ver_dados_jogador(self):
        jogador = self.selecionar_jogador()
        clear_terminal()
        if jogador:
            propriedades = [casa.nome for casa in jogador.propriedades] if jogador.propriedades else "Nenhuma"
            print("\n--- Dados do Jogador ---")
            print(f"Nome: {jogador.nome}")
            print(f"Saldo Atual: R${jogador.saldo}")
            print(f"Salário: R${jogador.salario}")
            print(f"Posição Atual: {jogador.posicao.tipo if jogador.posicao else 'Não iniciado'}")
            print(f"Propriedades: {propriedades}")
            print("-" * 30)
        else:
            print("Não há jogadores cadastrados.")

    def atualizar_jogador(self):
        jogador = self.selecionar_jogador()
        if jogador:
            while True:
                novo_saldo = input("Novo saldo (deixe em branco para não alterar): ")
                if novo_saldo.strip() == "":
                    break
                try:
                    novo_saldo = int(novo_saldo)
                    if novo_saldo < 0:
                        print("O saldo não pode ser negativo. Tente novamente.")
                    else:
                        jogador.saldo = novo_saldo
                        break
                except ValueError:
                    print("Por favor, insira um valor numérico válido para o saldo.")
            
            while True:
                novo_salario = input("Novo salário (deixe em branco para não alterar): ")
                if novo_salario.strip() == "":
                    break
                try:
                    novo_salario = int(novo_salario)
                    if novo_salario < 0:
                        print("O salário não pode ser negativo. Tente novamente.")
                    else:
                        jogador.salario = novo_salario
                        break
                except ValueError:
                    print("Por favor, insira um valor numérico válido para o salário.")
            clear_terminal()
            print(f"Jogador '{jogador.nome}' atualizado com sucesso!")

    def remover_jogador(self):
        jogador = self.selecionar_jogador()
        if jogador:
            self.jogadores.remove(jogador)
            clear_terminal()
            print(f"Jogador '{jogador.nome}' removido com sucesso!")

    def validar_minimo_jogadores(self):
        if len(self.jogadores) < 2:
            print("Erro: O jogo precisa de pelo menos 2 jogadores para começar!")
            return False
        return True

    def atualizar_jogadores_com_valores_padrao(self, saldo_inicial, salario):
        for jogador in self.jogadores:
            if jogador.saldo == 0:
                jogador.saldo = saldo_inicial
            if jogador.salario == 0:
                jogador.salario = salario
        print("Jogadores com saldo e salário zero foram atualizados para os valores configurados.")