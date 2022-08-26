import random



suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self) -> str:
        return self.rank + ' of ' + self.suit

#print(Card('Spades', 'Ace'))
class Deck:
    def __init__(self) -> None:
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    def __str__(self) -> str:
        deck_comp = ''
        for card in self.deck:
            deck_comp +='\n' + card.__str__()
        return 'The deck has: ' + deck_comp
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self) -> None:
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self, card: Card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    def adjust_ace(self):
        while self.value > 21 and self.aces > 0:
            self.aces -= 1
            self.value -= 10

class Chips:
    def __init__(self) -> None:
        self.total = 100
        self.bet = 0
    def lose_bet(self):
        self.total -= self.bet
    def win_bet(self):
        self.total += self.bet

class Game:
    def __init__(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.chips = Chips()
        self.stop_game = False
        self.play()
    def play(self):
        while not self.stop_game: 
            self.take_bet()
            self.deal_cards()
            self.show_some_cards()
            self.player_turn()
            self.dealer_turn()
            self.show_all_cards()
            self.winner()
            self.ask_to_play_again()
    def take_bet(self):
        while True: #! DANGER
            try:
                self.chips.bet = int(input('How many chips would you like to bet? '))
            except ValueError:
                print('Sorry, your bet must be an integer!')
            else:
                if self.chips.bet > self.chips.total:
                    print('Sorry, your bet can\'t exceed', self.chips.total)
                else:
                    break
    def deal_cards(self):
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
    def show_some_cards(self):
        print('\nDealer\'s Hand:')
        print(' <card hidden>')
        print(self.dealer_hand.cards[1])
        print('\nPlayer\'s Hand:', *self.player_hand.cards, sep='\n ')
    def player_turn(self):
        while True: #!DANGER
            print('\nYou have', self.chips.total, 'chips')
            print('Your  bet:', self.chips.bet)
            print('\nDo you want to hit or stand? Enter h or s: ')
            choice = input().lower()
            if choice == 'h':
                self.player_hand.add_card(self.deck.deal())
                self.show_some_cards()
                if self.player_hand.value > 21:
                    # self.lose_bet()
                    break
            elif choice == 's':
                break
            else: 
                print('Sorry, please enter h or s: ')
    def dealer_turn(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
        self.show_all_cards()
    def show_all_cards(self):
        print('\nDealer\'s Hand:', *self.dealer_hand.cards, sep='\n ')
        print('Dealer\'s Hand =', self.dealer_hand.value)
        print('\nPlayer\'s Hand:', *self.player_hand.cards, sep='\n ')
        print('Player\'s Hand =', self.player_hand.value)
    def winner(self):
        if self.player_hand.value > 21:
            self.lose_bet()
        elif self.dealer_hand.value > 21:
            self.win_bet()
        elif self.player_hand.value > self.dealer_hand.value:
            self.win_bet()
        elif self.player_hand.value < self.dealer_hand.value:
            self.lose_bet()
        else:
            print('It\'s a tie!')
    def lose_bet(self):
        self.chips.lose_bet()
        print('You lost!')
    def win_bet(self):
        self.chips.win_bet()
        print('You won!')
    def ask_to_play_again(self):
        print('\nDo you wont to play again? Enter y or n: ')
        if input() == 'y':
            self.deck = Deck()
            self.deck.shuffle()
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.play()
        else:
            print('Thanks for playing!')
            self.stop_game = True



Game()