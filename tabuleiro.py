import random
from utils import clear_terminal

class Casa:
    def __init__(self, tipo, nome, grupo=None, valor=0, aluguel=0, proprietario=None):
        self.tipo = tipo
        self.nome = nome
        self.grupo = grupo
        self.valor = valor
        self.aluguel = aluguel
        self.proprietario = proprietario
        self.jogadores_presentes = []
        self.proxima = None

    def __str__(self):
        jogadores = ', '.join([j.nome for j in self.jogadores_presentes]) or "Nenhum"
        proprietario = self.proprietario.nome if self.proprietario else "Sem proprietário"
        return f"Casa: {self.nome} | Tipo: {self.tipo} | Proprietário: {proprietario} | Jogadores: {jogadores}"

class Tabuleiro:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0
        self.grupos = {}

    def adicionar_casa(self, nova_casa):
        if self.inicio is None:
            self.inicio = nova_casa
            self.inicio.proxima = self.inicio
        else:
            atual = self.inicio
            while atual.proxima != self.inicio:
                atual = atual.proxima
            atual.proxima = nova_casa
            nova_casa.proxima = self.inicio
        self.tamanho += 1
        # print(f"Casa '{nova_casa.nome}' adicionada ao tabuleiro.")

    def exibir_tabuleiro(self):
        if not self.inicio:
            print("O tabuleiro está vazio.")
            return
        atual = self.inicio
        for i in range(self.tamanho):
            print(f"Casa {i + 1}: Tipo: {atual.tipo}, Nome: {atual.nome}, Valor: {atual.valor}, Aluguel: {atual.aluguel}")
            atual = atual.proxima

    def listar_imoveis(self):
        if self.inicio is None:
            print("Nenhum imóvel cadastrado no tabuleiro.")
            return

        imoveis_por_grupo = {}
        atual = self.inicio

        for _ in range(self.tamanho):
            grupo = atual.grupo if atual.grupo else "Sem Grupo"
            if grupo not in imoveis_por_grupo:
                imoveis_por_grupo[grupo] = []
            imoveis_por_grupo[grupo].append(atual)
            atual = atual.proxima

        print("--- Imóveis no Tabuleiro ---")
        for grupo, imoveis in imoveis_por_grupo.items():
            print(f"\n{grupo}:")
            for i, imovel in enumerate(imoveis, start=1):
                print(f"  {i}. Nome: {imovel.nome}, Valor: R${imovel.valor}, Aluguel: R${imovel.aluguel}")
        print("-" * 30)

    def atualizar_imovel(self, nome, novo_valor=None, novo_aluguel=None, novo_grupo=None):
        atual = self.inicio
        for _ in range(self.tamanho):
            if atual.nome == nome:
                if novo_valor is not None:
                    atual.valor = novo_valor
                if novo_aluguel is not None:
                    atual.aluguel = novo_aluguel
                if novo_grupo is not None:
                    atual.grupo = novo_grupo

    def remover_imovel(self, nome):
        if not self.inicio:
            print("O tabuleiro está vazio.")
            return
        anterior = None
        atual = self.inicio
        for i in range(self.tamanho):
            if atual.tipo == "Imóvel" and atual.nome == nome:
                if anterior:
                    anterior.proxima = atual.proxima
                else:
                    temp = self.inicio
                    while temp.proxima != self.inicio:
                        temp = temp.proxima
                    temp.proxima = atual.proxima
                    self.inicio = atual.proxima
                self.tamanho -= 1
                print(f"Imóvel '{nome}' removido com sucesso!")
                return
            anterior = atual
            atual = atual.proxima
        print(f"Imóvel '{nome}' não encontrado.")
    
    def validar_minimo_imoveis(self):
        contador = 0
        atual = self.inicio
        for _ in range(self.tamanho):
            if atual.tipo == "Imóvel":
                contador += 1
            atual = atual.proxima
        if contador < 10:
            print("Erro: O tabuleiro precisa de pelo menos 10 imóveis para iniciar o jogo!")
            return False
        return True

    def adicionar_grupo(self, nome, bonus):
        if nome not in self.grupos:
            self.grupos[nome] = bonus
        #     print(f"Grupo '{nome}' criado com sucesso com bônus de {bonus}%.")
        # else:
        #     print(f"Grupo '{nome}' já existe.")

    def listar_grupos(self):
        if not self.grupos:
            print("\nNenhum grupo cadastrado.")
            return []
        print("\n--- Grupos Disponíveis ---")
        for i, (grupo, bonus) in enumerate(self.grupos.items(), start=1):
            print(f"{i}. {grupo} (Bônus: {bonus}%)")
        print("-" * 30)
        return list(self.grupos.keys())
    
    def cadastrar_imovel(self, nome, valor, aluguel):
        grupos_disponiveis = self.listar_grupos()

        while True:
            if not grupos_disponiveis:
                while True:
                    grupo = input("Digite o nome do novo grupo: ")
                    validacao_grupo = grupo.replace(" ", "")
                    
                    if validacao_grupo == "" or not grupo:
                        print("Erro: O nome do imóvel não pode ser vazio. Tente novamente.")
                    else: break

                while True:
                    try:
                        bonus = int(input("Digite o bônus de conjunto (em %): "))
                        if bonus > 0:
                            break
                        else:
                            print("O bônus não pode ser menor que zero. Tente novamente.")
                    except ValueError:
                        print("Por favor, insira um número válido para o bônus.")

                self.adicionar_grupo(grupo, bonus)
                grupos_disponiveis = self.listar_grupos()
            else:
                print("Escolha um grupo para o imóvel ou digite '0' para criar um novo grupo:")
                for i, g in enumerate(grupos_disponiveis, start=1):
                    print(f"{i}. {g}")
                escolha = input("Digite o número do grupo ou '0': ").strip()

                if escolha == "0":
                    grupo = input("Digite o nome do novo grupo: ")

                    while True:
                        try:
                            bonus = int(input("Digite o bônus de conjunto (em %): "))
                            if bonus > 0:
                                break
                            else:
                                print("O bônus não pode ser menor que zero. Tente novamente.")
                        except ValueError:
                            print("Por favor, insira um número válido para o bônus.")

                    self.adicionar_grupo(grupo, bonus)
                    grupos_disponiveis = self.listar_grupos()
                elif escolha.isdigit() and 1 <= int(escolha) <= len(grupos_disponiveis):
                    grupo = grupos_disponiveis[int(escolha) - 1]
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        novo_imovel = Casa("Imóvel", nome=nome, valor=valor, aluguel=aluguel)
        novo_imovel.grupo = grupo
        self.adicionar_casa(novo_imovel)
        clear_terminal()
        print(f"Imóvel '{nome}' cadastrado com sucesso no grupo '{grupo}'!")

    def imovel_existe(self, nome):
        atual = self.inicio
        for _ in range(self.tamanho):
            if atual.nome == nome:
                return True
            atual = atual.proxima
        return False

    def grupo_existe(self, nome):
        return nome in self.grupos

    def montar_tabuleiro(self):
        imoveis = self.listar_imoveis_para_construcao()

        if not imoveis:
            print("Não há imóveis suficientes para montar o tabuleiro.")
            return

        random.shuffle(imoveis)

        casas_especiais = [
            Casa("Início", nome="Início"),
            Casa("Vá para a Prisão", nome="Vá para a Prisão"),
            Casa("Prisão", nome="Prisão"),
            Casa("Especial", nome="Férias")
        ]

        num_sorte_reves = len(imoveis) // 10
        for _ in range(num_sorte_reves):
            casas_especiais.append(Casa("Sorte-Reves", nome="Sorte ou Revés"))

        total_casas = len(imoveis) + len(casas_especiais)
        random.shuffle(casas_especiais)

        self.inicio = None
        anterior = None

        index_especial = 0
        for i in range(total_casas):
            if index_especial < len(casas_especiais) and i % (total_casas // len(casas_especiais)) == 0:
                nova_casa = casas_especiais[index_especial]
                index_especial += 1
            elif imoveis:
                imovel = imoveis.pop(0)
                nova_casa = Casa("Imóvel", nome=imovel["nome"], grupo=imovel["grupo"],
                                valor=imovel["valor"], aluguel=imovel["aluguel"])
            else:
                continue

            if self.inicio is None:
                self.inicio = nova_casa
            else:
                anterior.proxima = nova_casa

            anterior = nova_casa

        if anterior:
            anterior.proxima = self.inicio

        print("Tabuleiro montado com sucesso!")

    def listar_imoveis_para_construcao(self):
        if not self.inicio:
            print("Nenhum imóvel cadastrado no tabuleiro.")
            return []

        imoveis = []
        atual = self.inicio
        for _ in range(self.tamanho):
            if atual.tipo == "Imóvel":
                imoveis.append({
                    "nome": atual.nome,
                    "grupo": atual.grupo,
                    "valor": atual.valor,
                    "aluguel": atual.aluguel,
                })
            atual = atual.proxima

        return imoveis

    def exibir_estado_tabuleiro(self):
        if not self.inicio:
            print("O tabuleiro está vazio.")
            return

        atual = self.inicio
        while atual.tipo != "Início":
            atual = atual.proxima

        print("\n--- Estado Atual do Tabuleiro ---")
        casas_exibidas = 0
        inicio = atual

        while True:
            jogadores_na_casa = ", ".join([jogador.nome for jogador in atual.jogadores_presentes]) or "Nenhum"

            detalhes = [f"Casa {casas_exibidas + 1}: {atual.nome}", f"Tipo: {atual.tipo}"]

            if atual.tipo == "Imóvel":
                detalhes.extend([
                    f"Proprietário: {atual.proprietario.nome if atual.proprietario else 'Sem proprietário'}",
                    f"Grupo: {atual.grupo}",
                    f"Valor: R${atual.valor}",
                    f"Aluguel: R${atual.aluguel}"
                ])

            detalhes.append(f"Jogadores: {jogadores_na_casa}")

            print(" | ".join(detalhes))

            atual = atual.proxima
            casas_exibidas += 1

            if atual == inicio:
                break

        print("-" * 30)
