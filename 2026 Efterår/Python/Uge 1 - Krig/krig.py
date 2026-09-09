import random

class Card:

    suit = [
        "hjerter","ruder","klør","spar"
    ]

    def __init__(self, value):
        self.value = value
        self.suitValue = value//13
        self.numberValue = value % 13

    def __str__(self):
        return Card.suit[self.suitValue]+ " " + (
            "es" if self.numberValue == 0 else
            "konge" if self.numberValue == 12 else
            "dame" if self.numberValue == 11 else
            "bonde" if self.numberValue == 10 else
            str(self.numberValue+1)
        )

class Deck:
    def __init__(self, initial=None, name = "Bunke"):
        self.name = name
        self.cards = cards if initial is None else initial

    @classmethod
    def allCards(cls):
        cls([Card(x) for x in range(52)])

    def shuffle(self):
        random.shuffle(self.cards)

    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, card):
        self.cards.remove(card)

    def pickCard(self):
         card = self.cards[0]
         self.removeCard(card)
         return card

    def split(self, players):
        result = [Deck([],"Spiller "+str(x+1)) for x in range(players)]
        while self.cards:
            for player in result:
                player.addCard(self.cards.pop())
        return result

    def __str__(self):
        return "'"+self.name+"' med "+str(len(self.cards))+" kort"

class Krig:
    def __init__(self, players=2):
        d = Deck.allCards()
        d.shuffle()

        self.round = 0
        self.players = d.split(players)
        self.active_players = list(self.players)

        self.table = Deck([],"bordet")

    def finished(self):
        self.active_players = [p for p in self.active_players if p.cards]
        return len(self.active_players)==1

    def action(self):
        if self.finished(): return True

        self.round += 1
        yield ("Runde "+str(self.round))

        def getRoundWinner(players):
            playedCards = [(p,p.cards[0]) for p in players]

            max = -1
            for card in playedCards:
                self.table.addCard(card[1])
                yield (str(card[0])+" spiller "+str(card[1]))
                card[0].removeCard(card[1])

                max = card[1].numberValue if (card[1].numberValue>max and max!=0) or card[1].numberValue==0 else max

            winningPlayers = [c[0] for c in playedCards if c[1].numberValue==max]

            if len(winningPlayers)>1:
                yield ("Der er krig mellem spillerne: "+", ".join([str(p) for p in winningPlayers]))
                for p in list(winningPlayers):
                    count = 3
                    if len(p.cards)>3:
                        yield ("Spiller "+str(p)+" lægger 3 kort til krigen.")
                    elif len(p.cards)==0:
                        yield ("Spiller "+str(p)+" har ikke flere kort og taber krigen.")
                        count = 0
                        winningPlayers.remove(p)
                    else:
                        yield ("Spiller "+str(p)+" har kun "+str(len(p.cards))+" kort og lægger derfor "+str(len(p.cards)-1)+" kort.")
                        count = len(p.cards)-1

                    for i in range(count):
                        card = p.cards[0]
                        self.table.addCard(card)
                        p.removeCard(card)

                yield from getRoundWinner(winningPlayers)

            yield (str(winningPlayers[0])+" vinder "+str(self.table))

            while len(self.table.cards):
                card = self.table.cards[0]
                self.table.removeCard(card)
                winningPlayers[0].addCard(card)

        yield from getRoundWinner(self.active_players)

if __name__=="__main__":
    for i in range(10):
        k = Krig()
        while not k.finished() and k.round<15000:
            result = k.action()
            text = "\n".join(result)
            # print(text)
        print((k.round))

if __name__=="__main__":
    k = Krig()
    while not k.finished():
        result = k.action()

