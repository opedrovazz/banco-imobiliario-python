from menu import Menu
from partida import Partida

def main():
    menu = Menu()
    jogo_pronto = menu.exibir_menu()

    if jogo_pronto:
        partida = Partida(menu.tabuleiro, menu.gerenciador_jogadores, menu.config.max_rodadas)
        partida.iniciar()
    else:
        print("Configurações não concluídas. O jogo foi encerrado.")

if __name__ == "__main__":
    main()
