from configuracao import Configuracao
from jogador import GerenciadorDeJogadores
from tabuleiro import Tabuleiro, Casa
from imoveis_padrao import lista_padrao_ace_attorney, lista_padrao_arcane, lista_padrao_dragon_ball, lista_padrao_resident_evil
from utils import clear_terminal

class Menu:
    def __init__(self):
        self.config = Configuracao()
        self.gerenciador_jogadores = GerenciadorDeJogadores()
        self.tabuleiro = Tabuleiro()

    def exibir_menu(self):
        while True:
            print("\n--- Menu Principal ---")
            print("1. Configurar jogo (saldo inicial, salário, rodadas)")
            print("2. Gerenciar jogadores")
            print("3. Gerenciar imóveis")
            print("4. Iniciar jogo")
            print("5. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.config.configurar()
                self.gerenciador_jogadores.atualizar_jogadores_com_valores_padrao(
                    self.config.saldo_inicial,
                    self.config.salario,
                )
            elif opcao == "2":
                clear_terminal()
                self.gerenciar_jogadores()
            elif opcao == "3":
                clear_terminal()
                self.gerenciar_imoveis()
            elif opcao == "4":
                clear_terminal()
                if self.validar_requisitos():
                    print("Todos os requisitos atendidos. O jogo pode começar!")
                    return True
                else:
                    print("Requisitos não atendidos. Complete as configurações antes de iniciar o jogo.")
            elif opcao == "5":
                print("Saindo do programa...")
                return False
            else:
                clear_terminal()
                print("Opção inválida!")

    def gerenciar_jogadores(self):
        while True:
            print("\n--- Gerenciar Jogadores ---")
            print("1. Cadastrar jogador")
            print("2. Listar jogadores")
            print("3. Ver dados de um jogador")
            print("4. Atualizar jogador")
            print("5. Remover jogador")
            print("6. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                clear_terminal()
                nome = input("Digite o nome do jogador: ")
                self.gerenciador_jogadores.cadastrar_jogador(
                    nome,
                    self.config.saldo_inicial,
                    self.config.salario,
                )
            elif opcao == "2":
                clear_terminal()
                self.gerenciador_jogadores.listar_jogadores()
            elif opcao == "3":
                clear_terminal()
                self.gerenciador_jogadores.ver_dados_jogador()
            elif opcao == "4":
                clear_terminal()
                self.gerenciador_jogadores.atualizar_jogador()
            elif opcao == "5":
                clear_terminal()
                self.gerenciador_jogadores.remover_jogador()
            elif opcao == "6":
                clear_terminal()
                break
            else:
                print("Opção inválida! Tente novamente.")

    def gerenciar_imoveis(self):
        while True:
            print("\n--- Gerenciar Imóveis ---")
            print("1. Cadastrar imóvel")
            print("2. Listar imóveis")
            print("3. Criar grupo")
            print("4. Editar grupo")
            print("5. Listar grupos de imóveis")
            print("6. Atualizar imóvel")
            print("7. Remover imóvel")
            print("8. Usar imóveis padrão")
            print("9. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                clear_terminal()
                while True:
                    nome = input("Digite o nome do imóvel: ")
                    validacao_nome = nome.replace(" ", "")
                    if self.tabuleiro.imovel_existe(nome):
                        print(f"Erro: Já existe um imóvel com o nome '{nome}'. Tente novamente.")
                    elif validacao_nome == "" or not nome:
                        print("Erro: O nome do imóvel não pode ser vazio. Tente novamente.")
                    else: break

                while True:
                    try:
                        valor = int(input("Digite o valor do imóvel: "))
                        if valor > 0:
                            break
                        else:
                            print("O valor do imóvel deve ser maior que zero. Tente novamente.")
                    except ValueError:
                        print("Por favor, insira um número válido para o valor do imóvel.")
                while True:
                    try:
                        aluguel = int(input("Digite o valor do aluguel: "))
                        if aluguel > 0:
                            break
                        else:
                            print("O valor do aluguel deve ser maior que zero. Tente novamente.")
                    except ValueError:
                        print("Por favor, insira um número válido para o valor do aluguel.")

                self.tabuleiro.cadastrar_imovel(nome, valor, aluguel)

            elif opcao == "2":
                clear_terminal()
                self.tabuleiro.listar_imoveis()

            elif opcao == "3":
                clear_terminal()
                while True:
                    grupo = input("Digite o nome do novo grupo: ")
                    validacao_grupo = grupo.replace(" ", "")
                    if self.tabuleiro.grupo_existe(grupo):
                        print(f"Erro: Já existe um grupo com o nome '{grupo}'. Tente novamente.")
                    elif validacao_grupo == "" or not grupo:
                        print("Erro: O nome do grupo não pode ser vazio. Tente novamente.")
                    else: break

                while True:
                    try:
                        bonus = int(input("Digite o bônus de conjunto (em %): "))
                        if bonus >= 0:
                            break
                        else:
                            print("O bônus não pode ser menor que zero. Tente novamente.")
                    except ValueError:
                        print("Por favor, insira um número válido para o bônus.")

                clear_terminal()
                self.tabuleiro.adicionar_grupo(grupo, bonus)

            elif opcao == "4":
                clear_terminal()
                grupos = self.tabuleiro.listar_grupos()
                if grupos:
                    escolha = input("Escolha o número do grupo que deseja editar: ")
                    if escolha.isdigit() and 1 <= int(escolha) <= len(grupos):
                        grupo_antigo = grupos[int(escolha) - 1]
                        novo_nome = input("Digite o novo nome do grupo: ")

                        while True:
                            try:
                                novo_bonus = int(input("Digite o novo bônus de conjunto (em %): "))
                                if novo_bonus > 0:
                                    break
                                else:
                                    print("O bônus não pode menor que zero. Tente novamente.")
                            except ValueError:
                                print("Por favor, insira um número válido para o bônus.")

                        self.tabuleiro.grupos[novo_nome] = self.tabuleiro.grupos.pop(grupo_antigo)
                        self.tabuleiro.grupos[novo_nome] = novo_bonus

                        atual = self.tabuleiro.inicio
                        for _ in range(self.tabuleiro.tamanho):
                            if atual.grupo == grupo_antigo:
                                atual.grupo = novo_nome
                            atual = atual.proxima
                        clear_terminal()
                        print(f"Grupo {novo_nome} editado com sucesso.")
                    else:
                        print("Opção inválida.")


            elif opcao == "5":
                clear_terminal()
                self.tabuleiro.listar_grupos()

            elif opcao == "6":
                clear_terminal()
                imoveis = []
                atual = self.tabuleiro.inicio
                for i in range(self.tabuleiro.tamanho):
                    imoveis.append(atual)
                    print(f"{i + 1}. Nome: {atual.nome}, Valor: R${atual.valor}, Aluguel: R${atual.aluguel}, Grupo: {atual.grupo}")
                    atual = atual.proxima

                if not imoveis:
                    print("Nenhum imóvel cadastrado para atualizar.")
                    return

                while True:
                    escolha = input("Escolha o número do imóvel que deseja atualizar: ")
                    if escolha.isdigit() and 1 <= int(escolha) <= len(imoveis):
                        imovel = imoveis[int(escolha) - 1]
                        break
                    else:
                        print("Opção inválida. Tente novamente.")

                print(f"Atualizando imóvel '{imovel.nome}'.")

                while True:
                    try:
                        novo_valor = input("Novo valor (deixe em branco para não alterar): ")
                        if novo_valor == "":
                            novo_valor = None
                            break
                        novo_valor = int(novo_valor)
                        if novo_valor > 0:
                            break
                        else:
                            print("O valor do imóvel deve ser maior que zero. Tente novamente.")
                    except ValueError:
                        print("Por favor, insira um número válido para o valor.")

                while True:
                    try:
                        novo_aluguel = input("Novo aluguel (deixe em branco para não alterar): ")
                        if novo_aluguel == "":
                            novo_aluguel = None
                            break
                        novo_aluguel = int(novo_aluguel)
                        if novo_aluguel > 0:
                            break
                        else:
                            print("O aluguel deve ser maior que zero. Tente novamente.")
                    except ValueError:
                        print("Por favor, insira um número válido para o aluguel.")

                grupos = self.tabuleiro.listar_grupos()
                novo_grupo = None
                if grupos:
                    print("\n--- Grupos Disponíveis ---")
                    for i, g in enumerate(grupos, start=1):
                        print(f"{i}. {g}")
                    while True:
                        escolha_grupo = input("Escolha um novo grupo para o imóvel ou deixe em branco para não alterar: ").strip()
                        if escolha_grupo == "":
                            break
                        if escolha_grupo.isdigit() and 1 <= int(escolha_grupo) <= len(grupos):
                            novo_grupo = grupos[int(escolha_grupo) - 1]
                            break
                        else:
                            print("Opção inválida. Tente novamente.")

                self.tabuleiro.atualizar_imovel(imovel.nome, novo_valor, novo_aluguel, novo_grupo)
                clear_terminal()
                print(f"Imóvel '{imovel.nome}' atualizado com sucesso!")

            elif opcao == "7":
                clear_terminal()
                imoveis = []
                atual = self.tabuleiro.inicio
                for i in range(self.tabuleiro.tamanho):
                    imoveis.append(atual)
                    print(f"{i + 1}. Nome: {atual.nome}, Valor: R${atual.valor}, Aluguel: R${atual.aluguel}, Grupo: {atual.grupo}")
                    atual = atual.proxima

                if not imoveis:
                    print("Nenhum imóvel cadastrado para remover.")
                    return

                while True:
                    escolha = input("Escolha o número do imóvel que deseja remover: ")
                    if escolha.isdigit() and 1 <= int(escolha) <= len(imoveis):
                        imovel = imoveis[int(escolha) - 1]
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                clear_terminal()
                self.tabuleiro.remover_imovel(imovel.nome)

            elif opcao == "8":
                clear_terminal()
                self.usar_imoveis_padrao()

            elif opcao == "9":
                clear_terminal()
                break

            else:
                print("Opção inválida! Tente novamente.")

    def usar_imoveis_padrao(self):
        print("\n--- Usar Imóveis Padrão ---")
        print("1. Tema: Ace Attorney")
        print("2. Tema: Arcane")
        print("3. Tema: Dragon Ball")
        print("4. Tema: Resident Evil")
        print("5. Voltar")

        opcao = input("Escolha uma lista padrão: ")

        if opcao == "1":
            lista = lista_padrao_ace_attorney()
        elif opcao == "2":
            lista = lista_padrao_arcane()
        elif opcao == "3":
            lista = lista_padrao_dragon_ball()
        elif opcao == "4":
            lista = lista_padrao_resident_evil()
        elif opcao == "5":
            return
        else:
            print("Opção inválida.")
            return

        clear_terminal()
        for imovel in lista:
            grupo = imovel["grupo"]
            bonus = imovel.get("bonus", 0)

            if grupo not in self.tabuleiro.grupos:
                self.tabuleiro.adicionar_grupo(grupo, bonus)

            if self.tabuleiro.imovel_existe(imovel["nome"]):
                continue

            novo_imovel = Casa("Imóvel", nome=imovel["nome"], valor=imovel["valor"], aluguel=imovel["aluguel"])
            novo_imovel.grupo = grupo
            self.tabuleiro.adicionar_casa(novo_imovel)
            # print(f"Imóvel '{imovel['nome']}' cadastrado com sucesso no grupo '{grupo}'!")

    def validar_requisitos(self):
        jogadores_ok = self.gerenciador_jogadores.validar_minimo_jogadores()
        imoveis_ok = self.tabuleiro.validar_minimo_imoveis()
        return jogadores_ok and imoveis_ok

    def negociar_propriedades(jogador1, jogadores):
        print("\n--- Negociar Propriedades ---")
        print(f"Propriedades de {jogador1.nome}: {[casa.nome for casa in jogador1.propriedades]}")

        comprador_nome = input("Digite o nome do jogador com quem deseja negociar: ")
        comprador = next((j for j in jogadores if j.nome == comprador_nome), None)

        if not comprador:
            print("Jogador não encontrado.")
            return

        print(f"Propriedades de {comprador.nome}: {[casa.nome for casa in comprador.propriedades]}")
        propriedade = input(f"Digite o nome da propriedade que {jogador1.nome} deseja vender: ")
        propriedade_venda = next((c for c in jogador1.propriedades if c.nome == propriedade), None)

        if not propriedade_venda:
            print(f"Propriedade '{propriedade}' não encontrada nas posses de {jogador1.nome}.")
            return

        oferta = int(input(f"Quanto {jogador1.nome} deseja pedir por '{propriedade}': "))
        print(f"{comprador.nome}, {jogador1.nome} está pedindo R${oferta} por '{propriedade}'.")

        resposta = input(f"{comprador.nome}, deseja aceitar a oferta? (sim/não): ").strip().lower()
        if resposta == "sim" and comprador.saldo >= oferta:
            comprador.saldo -= oferta
            jogador1.saldo += oferta
            jogador1.propriedades.remove(propriedade_venda)
            comprador.propriedades.append(propriedade_venda)
            propriedade_venda.proprietario = comprador
            print(f"Transação concluída! {comprador.nome} comprou '{propriedade}' por R${oferta}.")
        else:
            print("A negociação foi cancelada ou o saldo é insuficiente.")
