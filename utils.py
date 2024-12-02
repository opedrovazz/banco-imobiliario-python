import os
import platform
import random

def rolar_dado():
    return random.randint(1, 6)

def exibir_menu():
    print("1. Cadastrar jogador")
    print("2. Cadastrar imóvel")
    print("3. Iniciar jogo")
    print("4. Sair")

def exibir_status(gerenciador_jogadores):
    print("\n--- Status dos Jogadores ---")
    for jogador in gerenciador_jogadores.jogadores:
        print(f"Jogador: {jogador.nome}")
        print(f"  Saldo: R${jogador.saldo}")
        if jogador.posicao:
            print(f"  Posição atual: {jogador.posicao.tipo}")
        else:
            print("  Posição atual: Não definido")
        propriedades = [prop.nome for prop in jogador.propriedades]
        print(f"  Propriedades: {', '.join(propriedades) if propriedades else 'Nenhuma'}")
    print("-" * 30)

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
