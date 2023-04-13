import random


SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}



class Card:
    def __init__(self, suit:str, rank:str):
        """Create a new card.

        Args:
            suit (str): The card suit.
            rank (str): The card rank.
        """

        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        """The string representation of the card.

        Returns:
            str: The card with the string format "[rank] of [suit]".
        """

        return self.rank + ' of ' + self.suit
    
    def get_value(self):
        """Get the value of the card.

        Returns:
            int: The numeric value of the card.
        """

        return VALUES[self.rank]

class Deck:
    def __init__(self) -> None:
        """Initialize a Deck.
        """

        self.deck:list[Card] = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def __str__(self) -> str:
        """The string representation of the deck.

        Returns:
            str: The cards in the deck.
        """

        deck_comp = ''
        for card in self.deck:
            deck_comp +='\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        """Shuffle all cards in the deck.
        """

        random.shuffle(self.deck)

    def deal(self):
        """Give out a single card from the deck.

        Returns:
            Card: The card given.
        """
        
        single_card = self.deck[0]
        self.deck.__delitem__(0)
        return single_card

    def print_all(self):
        """Print the names of all cards in the deck.

        Returns:
            list[str]: All the string representations of all cards in the deck.
        """

        card_names:list[str] = []
        for card in self.deck:
            card_names.append(str(card))
        return card_names

class Hand:
    def __init__(self) -> None:
        """Initialize a new Hand.
        """
        self.cards:list[Card] = []
        self.value = 0
        self.aces = 0

    def add_card(self, card: Card):
        """Add a card to the Hand.

        Args:
            card (Card): The card to add.
        """

        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        
    def adjust_ace(self):
        """Adjusts aces from the hand if possible and required.
        """
        if self.value > 21 and self.aces > 0:
            if (self.aces == self.cards.__len__()):
                for i in range(self.cards.__len__() - 1):
                    self.aces -= 1
                    self.value -= 10

            else:
                self.aces -= 1
                self.value -= 10

class Chips:
    def __init__(self) -> None:
        """Initialize new Chips.
        """
        self.total = 100
        self.bet = 0

    def lose_bet(self):
        """Trigger a lost bet.
        """
        self.total -= self.bet

    def win_bet(self):
        """Trigger a won bet.
        """

        self.total += self.bet

class Game:
    def __init__(self) -> None:
        """Initialize a game.
        """

        self.m = 0
        """The amount of the cards remaining in the deck + 1 (for the hidden card of the dealer)."""
        self.l = 0
        """The amount of cards the player can draw to have a total score of <= 21."""
        self.deck = Deck()
        """The Game Deck"""
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.chips = Chips()
        self.stop_game = False
        self.play()

    def play(self):
        """Run the game.
        """

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
        """Take the bet from the player.
        """

        while True: #! DANGER
            try:
                print('You have', self.chips.total, 'chips')
                self.chips.bet = int(input('How many chips would you like to bet? '))
            except ValueError:
                print('Sorry, your bet must be an integer!')
            else:
                if self.chips.bet > self.chips.total:
                    print('Sorry, your bet can\'t exceed', self.chips.total)
                else:
                    break

    def deal_cards(self):
        """Deal 2 cards to the player and to the dealer.
        """

        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def show_some_cards(self):
        """Show the player's cards and the second card of the dealer.
        """

        print('\nDealer\'s Hand:')
        print(' <card hidden>')
        print(self.dealer_hand.cards[1])
        print('\nPlayer\'s Hand:', *self.player_hand.cards, sep='\n ')

    def jufo_calculations(self):
        """Calculations for the JuFo Project

        Containing the AI.
        """

        self.m = 0
        self.m = self.deck.deck.__len__() + 1
        
        self.l = 0

        possible_cards:list[Card] = self.deck.deck
        possible_cards.append(self.dealer_hand.cards[0])
        
        copy_cards = self.player_hand.cards
        copy_hand = Hand()

        for card in copy_cards:
            copy_hand.add_card(card)

        for card in possible_cards:
            copy_hand.add_card(card)
            copy_hand.adjust_ace()

            if copy_hand.value <= 21:
                self.l = self.l + 1
            
            copy_hand = Hand()

            for copied_card in copy_cards:
                copy_hand.add_card(copied_card)
        
        chance = self.l / self.m

        if self.player_hand.value > 18:
            print('You should probably stay.')
        else:
            print('The chance to draw a card that does not overbuy you is ' + str(chance*100) + '%')

    def jufo_calculations_dealer(self):
        """
            AI like the Dealer
        """
        if self.player_hand.value > 16:
            print("The Dealer Algorithm would stay.")
        if self.player_hand.value < 17:
            print("The Dealer Algorithm would draw a card.")

    def jufo_calculations_thorp(self):
        """AI like Thorp
        """
        self.open_cards:list[Card] = self.player_hand.cards.__add__([self.dealer_hand.cards[1]])
        self.thorp = 0
        for ocard in self.open_cards:
            if ocard.get_value() < 7:
                self.thorp = self.thorp + 1
            if ocard.get_value() > 9:
                self.thorp = self.thorp -1
        print("After Thorps calculations you would get the value:"+ str(self.thorp)) 

    def player_turn(self):
        """Execute the player's turn.
        """

        while True: #!DANGER
            print('\nYou have', self.chips.total, 'chips')
            print('Your bet:', self.chips.bet)
            self.jufo_calculations()
            self.jufo_calculations_dealer()
            self.jufo_calculations_thorp()
            print('\nDo you want to hit or stand? Enter h or s: ')
            choice = input().lower()
            if choice == 'h':
                self.player_hand.add_card(self.deck.deal())
                self.show_some_cards()
                self.player_hand.adjust_ace()
                if self.player_hand.value > 21:
                    break
            elif choice == 's':
                break
            else: 
                print('Sorry, please enter h or s: ')

    def dealer_turn(self):
        """Execute the dealer's turn.
        """

        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.adjust_ace()

    def show_all_cards(self):
        """Show all cards.
        """

        print('\nDealer\'s Hand:', *self.dealer_hand.cards, sep='\n ')
        print('Dealer\'s Hand =', self.dealer_hand.value)
        print('\nPlayer\'s Hand:', *self.player_hand.cards, sep='\n ')
        print('Player\'s Hand =', self.player_hand.value)

    def winner(self):
        """Check who won the game.
        """

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
        """Loose the bet.
        """
        self.chips.lose_bet()
        print('You lost!')

    def win_bet(self):
        """Win the bet.
        """
        self.chips.win_bet()
        print('You won!')

    def ask_to_play_again(self):
        """Ask the player if they want to play again.
        """

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