import random

class SorteReves:
    def __init__(self):
        self.sortes = [
            "Você encontrou dinheiro no chão! Receba R$200.",
            "Sua empresa teve lucros inesperados! Receba R$300.",
            "Você ganhou um prêmio na loteria! Receba R$500.",
            "Uma herança distante foi deixada para você. Receba R$400.",
            "Você vendeu uma propriedade com lucro! Receba R$250.",
            "Você recebeu um bônus no trabalho. Receba R$150.",
            "Seus investimentos em ações deram retorno positivo. Receba R$350.",
            "Um amigo pagou uma dívida antiga. Receba R$100.",
            "Você ganhou uma promoção no trabalho. Receba R$450.",
            "Um cliente deixou uma gorjeta generosa! Receba R$50.",
            "Você encontrou um tesouro escondido. Receba R$600.",
            "Você ganhou uma aposta com um amigo. Receba R$75.",
            "Seus aluguéis foram pagos adiantados. Receba R$250.",
            "Você recebeu um prêmio por bom comportamento cívico. Receba R$200.",
            "Um parente distante deixou um presente financeiro para você. Receba R$300."
        ]
        self.reves = [
            "Você foi multado por excesso de velocidade. Pague R$150.",
            "Sua conta de luz veio mais alta que o esperado. Pague R$100.",
            "Um reparo emergencial em sua casa custou caro. Pague R$200.",
            "Você perdeu dinheiro em um investimento ruim. Pague R$300.",
            "Você teve despesas médicas inesperadas. Pague R$250.",
            "Sua empresa sofreu um revés financeiro. Pague R$400.",
            "Um parente pediu um empréstimo e não pagou. Pague R$150.",
            "Você teve que pagar impostos atrasados. Pague R$350.",
            "Você perdeu uma aposta para um amigo. Pague R$100.",
            "Seu carro quebrou e precisou de conserto. Pague R$500.",
            "Você foi roubado em uma viagem. Pague R$300.",
            "Você esqueceu de pagar uma conta importante e teve multa. Pague R$200.",
            "Seu animal de estimação ficou doente e precisou de tratamento. Pague R$150.",
            "Uma reforma inesperada no seu imóvel custou caro. Pague R$400.",
            "Você perdeu dinheiro jogando cartas com amigos. Pague R$50."
        ]

    def sortear_sorte(self):
        return random.choice(self.sortes)

    def sortear_reves(self):
        return random.choice(self.reves)
