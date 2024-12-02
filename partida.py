from utils import rolar_dado, exibir_status, clear_terminal

class Partida:
    def __init__(self, tabuleiro, gerenciador_jogadores, max_rodadas):
        self.tabuleiro = tabuleiro
        self.gerenciador_jogadores = gerenciador_jogadores
        self.max_rodadas = max_rodadas
        self.turno_atual = 1
        self.rodada_atual = 1

    def iniciar(self):
        clear_terminal()
        print("\n--- Início da Partida ---")

        self.tabuleiro.montar_tabuleiro()

        casa_inicial = None
        atual = self.tabuleiro.inicio
        for _ in range(self.tabuleiro.tamanho):
            if atual.tipo == "Início":
                casa_inicial = atual
                break
            atual = atual.proxima

        if not casa_inicial:
            self.tabuleiro.exibir_estado_tabuleiro()
            raise Exception("Erro: A casa 'Início' não foi encontrada no tabuleiro.")

        for jogador in self.gerenciador_jogadores.jogadores:
            jogador.posicao = casa_inicial
            if jogador not in casa_inicial.jogadores_presentes:
                casa_inicial.jogadores_presentes.append(jogador)

        self.turno_atual = 1

        for rodada in range(self.max_rodadas):
            self.rodada_atual = rodada + 1
            print(f"\n--- Rodada {self.rodada_atual} ---")

            jogadores_ativos = [j for j in self.gerenciador_jogadores.jogadores if j.saldo > 0]
            if len(jogadores_ativos) == 1:
                vencedor = jogadores_ativos[0]
                print(f"\nO jogo terminou! O vencedor é {vencedor.nome} com um saldo de R${vencedor.saldo}.")
                return

            for jogador in jogadores_ativos:
                if jogador.rodadas_preso > 0:
                    clear_terminal()
                    print(f"{jogador.nome} está preso. Rodadas restantes: {jogador.rodadas_preso}.")
                    jogador.rodadas_preso -= 1
                    continue
                else: clear_terminal()
                self.turno_jogador(jogador)

            self.turno_atual += 1

        print("\nO número máximo de rodadas foi alcançado.")
        self.declarar_vencedor()


    def turno_jogador(self, jogador):
        jogou_dado = False

        while True:
            print(f"\n--- Turno de {jogador.nome} ---")
            print("\nEscolha uma ação:")
            if not jogou_dado:
                print("1. Jogar o dado")
            print("2. Exibir status dos jogadores")
            print("3. Ver estado do tabuleiro")
            if self.turno_atual > 1:
                print("4. Trocar propriedades")
                print("5. Comprar propriedades")
                print("6. Vender propriedades")
            print("7. Terminar turno")
            print("0. Abandonar a partida")
            opcao = input("Digite o número da opção: ")

            if opcao == "1" and not jogou_dado:
                clear_terminal()
                dado = rolar_dado()
                jogou_dado = True
                print(f"{jogador.nome} rolou o dado e tirou {dado}.")
                jogador.mover(dado)
                jogador.interagir_com_casa()
                print(f"Saldo atual de {jogador.nome}: R${jogador.saldo}")
            elif opcao == "2":
                clear_terminal()
                exibir_status(self.gerenciador_jogadores)
            elif opcao == "3":
                clear_terminal()
                self.tabuleiro.exibir_estado_tabuleiro()
            elif opcao == "4" and self.turno_atual > 1:
                clear_terminal()
                self.trocar_propriedades(jogador)
            elif opcao == "5" and self.turno_atual > 1:
                clear_terminal()
                self.comprar_propriedades(jogador)
            elif opcao == "6" and self.turno_atual > 1:
                clear_terminal()
                self.vender_propriedades(jogador)
            elif opcao == "7":
                clear_terminal()
                print(f"{jogador.nome} terminou seu turno.")
                break
            elif opcao == "0":
                clear_terminal()
                self.abandonar_partida(jogador)
                break
            else:
                clear_terminal()
                print("Opção inválida! Tente novamente.")


    def abandonar_partida(self, jogador):
        print(f"\n{jogador.nome} decidiu abandonar a partida.")
        
        for propriedade in jogador.propriedades:
            propriedade.proprietario = None
            print(f"O imóvel '{propriedade.nome}' agora está disponível para compra.")

        self.gerenciador_jogadores.jogadores.remove(jogador)
        print(f"{jogador.nome} foi removido do jogo.")

    def vender_propriedades(self, vendedor):
        print("\n--- Vender Propriedades ---")
        propriedades_vendedor = vendedor.propriedades
        if not propriedades_vendedor:
            print(f"{vendedor.nome} não possui propriedades para vender.")
            return

        print("\n--- Suas Propriedades ---")
        for idx, propriedade in enumerate(propriedades_vendedor, start=1):
            print(f"{idx}. {propriedade.nome} (Valor: R${propriedade.valor}, Aluguel: R${propriedade.aluguel})")

        while True:
            try:
                escolha_prop = int(input(f"Escolha o número da propriedade para vender (1-{len(propriedades_vendedor)}): "))
                if 1 <= escolha_prop <= len(propriedades_vendedor):
                    propriedade_venda = propriedades_vendedor[escolha_prop - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        compradores = [j for j in self.gerenciador_jogadores.jogadores if j != vendedor]
        if not compradores:
            print("Não há outros jogadores disponíveis para comprar.")
            return

        print("\n--- Jogadores Disponíveis ---")
        for idx, comprador in enumerate(compradores, start=1):
            print(f"{idx}. {comprador.nome} (Saldo: R${comprador.saldo})")

        while True:
            try:
                escolha_comprador = int(input(f"Escolha o número do comprador (1-{len(compradores)}): "))
                if 1 <= escolha_comprador <= len(compradores):
                    comprador = compradores[escolha_comprador - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        while True:
            try:
                valor_venda = int(input(f"Quanto deseja pedir por '{propriedade_venda.nome}'? "))
                if valor_venda > 0:
                    break
                else:
                    print("O valor da venda deve ser maior que zero. Tente novamente.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        print(f"{comprador.nome}, {vendedor.nome} está pedindo R${valor_venda} por '{propriedade_venda.nome}'.")
        resposta = input(f"{comprador.nome}, deseja aceitar a oferta? ('s' para sim, 'n' para não): ").strip().lower()

        if resposta == "s" and comprador.saldo >= valor_venda:
            comprador.saldo -= valor_venda
            vendedor.saldo += valor_venda
            vendedor.propriedades.remove(propriedade_venda)
            comprador.propriedades.append(propriedade_venda)
            propriedade_venda.proprietario = comprador
            print(f"Transação concluída! {comprador.nome} comprou '{propriedade_venda.nome}' por R${valor_venda}.")
        elif resposta == "s" and comprador.saldo < valor_venda:
            print(f"Saldo insuficiente! {comprador.nome} não pode comprar '{propriedade_venda.nome}'.")
        elif resposta == 'n':
            print("Você decidiu não vender o imóvel.")
        else:
            print("Opção inválida, cancelando...")

    def trocar_propriedades(self, jogador1):
        print("\n--- Trocar Propriedades ---")
        jogadores = [j for j in self.gerenciador_jogadores.jogadores if j != jogador1]
        if not jogadores:
            print("Não há outros jogadores disponíveis para troca.")
            return

        print("\n--- Jogadores Disponíveis ---")
        for idx, jogador in enumerate(jogadores, start=1):
            print(f"{idx}. {jogador.nome} (Propriedades: {[casa.nome for casa in jogador.propriedades]})")

        while True:
            try:
                escolha_jogador = int(input(f"Escolha o número do jogador para trocar (1-{len(jogadores)}): "))
                if 1 <= escolha_jogador <= len(jogadores):
                    jogador2 = jogadores[escolha_jogador - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        print(f"\n--- Propriedades de {jogador1.nome} ---")
        for idx, prop in enumerate(jogador1.propriedades, start=1):
            print(f"{idx}. {prop.nome} (Valor: R${prop.valor}, Aluguel: R${prop.aluguel})")

        while True:
            try:
                escolha_prop1 = int(input(f"Escolha a propriedade de {jogador1.nome} para trocar (1-{len(jogador1.propriedades)}): "))
                if 1 <= escolha_prop1 <= len(jogador1.propriedades):
                    propriedade1 = jogador1.propriedades[escolha_prop1 - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        print(f"\n--- Propriedades de {jogador2.nome} ---")
        for idx, prop in enumerate(jogador2.propriedades, start=1):
            print(f"{idx}. {prop.nome} (Valor: R${prop.valor}, Aluguel: R${prop.aluguel})")

        while True:
            try:
                escolha_prop2 = int(input(f"Escolha a propriedade de {jogador2.nome} para trocar (1-{len(jogador2.propriedades)}): "))
                if 1 <= escolha_prop2 <= len(jogador2.propriedades):
                    propriedade2 = jogador2.propriedades[escolha_prop2 - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        print(f"\nProposta de troca:")
        print(f"{jogador1.nome}: {propriedade1.nome}")
        print(f"{jogador2.nome}: {propriedade2.nome}")

        resposta = input("Ambos os jogadores concordam com a troca? ('s' para sim, 'n' para não): ").strip().lower()
        if resposta == "s":
            jogador1.propriedades.remove(propriedade1)
            jogador2.propriedades.remove(propriedade2)
            jogador1.propriedades.append(propriedade2)
            jogador2.propriedades.append(propriedade1)
            propriedade1.proprietario = jogador2
            propriedade2.proprietario = jogador1
            print("Troca concluída com sucesso!")
        elif resposta == "n":
            print("Os jogadores decidiram não trocar as propriedades.")
        else:
            print("Opção inválida, cancelando...")

    def comprar_propriedades(self, comprador):
        print("\n--- Comprar Propriedades ---")
        vendedores = [j for j in self.gerenciador_jogadores.jogadores if j != comprador and j.propriedades]
        if not vendedores:
            print("Nenhum jogador possui propriedades disponíveis para venda.")
            return

        print("\n--- Jogadores Disponíveis ---")
        for idx, vendedor in enumerate(vendedores, start=1):
            print(f"{idx}. {vendedor.nome} (Propriedades: {[casa.nome for casa in vendedor.propriedades]})")

        while True:
            try:
                escolha_vendedor = int(input(f"Escolha o número do vendedor (1-{len(vendedores)}): "))
                if 1 <= escolha_vendedor <= len(vendedores):
                    vendedor = vendedores[escolha_vendedor - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        print(f"\n--- Propriedades de {vendedor.nome} ---")
        for idx, propriedade in enumerate(vendedor.propriedades, start=1):
            print(f"{idx}. {propriedade.nome} (Valor: R${propriedade.valor}, Aluguel: R${propriedade.aluguel})")

        while True:
            try:
                escolha_prop = int(input(f"Escolha o número da propriedade para comprar (1-{len(vendedor.propriedades)}): "))
                if 1 <= escolha_prop <= len(vendedor.propriedades):
                    propriedade_compra = vendedor.propriedades[escolha_prop - 1]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

        while True:
            try:
                oferta = int(input(f"Quanto deseja oferecer por '{propriedade_compra.nome}'? "))
                if oferta > 0:
                    break
                else:
                    print("O valor deve ser maior que zero. Tente novamente.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        print(f"{vendedor.nome}, {comprador.nome} está oferecendo R${oferta} por '{propriedade_compra.nome}'.")
        resposta = input(f"{vendedor.nome}, deseja aceitar a oferta? ('s' para sim, 'n' para não): ").strip().lower()

        if resposta == "s" and comprador.saldo >= oferta:
            comprador.saldo -= oferta
            vendedor.saldo += oferta
            vendedor.propriedades.remove(propriedade_compra)
            comprador.propriedades.append(propriedade_compra)
            propriedade_compra.proprietario = comprador
            print("Compra concluída com sucesso!")
        elif resposta == "s" and comprador.saldo < oferta:
            print(f"Saldo insuficiente! {comprador.nome} não pode comprar '{propriedade_compra.nome}'.")
        elif resposta == "n":
            print("Você decidiu não comprar o imóvel.")
        else:
            print("Opção invalida, cancelando...")

    def declarar_vencedor(self):
        print("\n--- Encerramento da Partida ---")
        jogadores_ativos = [j for j in self.gerenciador_jogadores.jogadores if j.saldo > 0]
        if jogadores_ativos:
            vencedor = max(jogadores_ativos, key=lambda j: j.saldo)
            print(f"O vencedor é {vencedor.nome} com um saldo de R${vencedor.saldo}!")
        else:
            print("Todos os jogadores estão falidos. Não há vencedor!")
        print("\nObrigado por jogar!")
