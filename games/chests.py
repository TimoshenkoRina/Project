import random
from typing import List
import time
from games.cards import Deck, Card

main_ranks=['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
main_suits=['буби', 'черви', 'крести', 'пики']

class Player:
    def __init__(self, name):
        self.name = name
        self.hand: List[Card] = []
        self.chests = 0

    def add_cards(self, cards):
        """добавляем карты, если ты их угадал"""
        self.hand.extend(cards)
        self.check_chests()

    def remove_cards_rank(self, rank):
        """если соперник угадал карты:
        1. формируем список карт, которые отдаем
        2. формируем список, который остался"""
        give = [c for c in self.hand if c.rank == rank]
        self.hand = [c for c in self.hand if c.rank != rank]
        return give

    def has_rank(self, rank):
        """первый вопрос
        у тебя есть девятки?"""
        return any(c.rank == rank for c in self.hand)

    def count_rank(self, rank):
        """второй вопрос
        у тебя их 1/2/3?"""
        return sum(1 for c in self.hand if c.rank == rank)

    def has_suits(self, rank, suits):
        """третий вопрос
        это пики/буби/черви/крести?
        сравниваем масти на руке с мастью, которую спросили"""
        my_suits=[c.suit for c in self.hand if c.rank == rank]
        return set(my_suits)==set(suits)

    def check_chests(self):
        """проверка кол-ва сундучков
        если сумма карт одинакового ранга==4,
        то это сундучок. Удаляем сундучок из руки"""
        for rank in main_ranks:
            if sum(1 for c in self.hand if c.rank == rank)==4:
                self.chests += 1
                print (f'{self.name} собрал сундучок из {rank}!')
                self.hand = [c for c in self.hand if c.rank != rank]

    def get_hand_ranks(self):
        """что бы компьютер мог спрашивать карты у пользователя
        он должен знать, какие карты у него на руке"""
        return list(set(c.rank for c in self.hand))

class ComputerPlayer(Player):
    """класс для логики компьютера (наследует методы от Player)
    Но вопросы задает свои из прописанной логики и случайностей"""
    def ask_rank(self):
        """спрашиваем ранг. Если рука пуская, то можно
        спросить любой ранг"""
        if not self.hand:
            return random.choice(main_ranks)
        # проверяем, какие карты есть на руках
        # выбираем из них карту для вопроса
        choice = random.choice(self.get_hand_ranks())
        print (f'У тебя есть {choice}?')
        time.sleep(2)
        return choice

    def ask_count(self):
        """спрашиваем кол-во"""
        choice= random.randint(1, 3)
        print (f'Я думаю у тебя их {choice}')
        time.sleep(2)
        return choice

    def ask_suits(self, count):
        """спрашиваем масть"""
        choice = random.sample(main_suits, count)
        print (f"Это масти {', '.join(choice)}")
        time.sleep(2)
        return choice

class HumanPlayer(Player):
    """класс для логики человека (наследует методы от Player).
    Вопросы идут с клавиатуры"""
    def ask_rank(self):
        """спрашиваем ранг карты"""
        print (f'\nТвои карты:{self.hand}')
        while True:
            rank= input('Спроси величину карты (6, 7, ... J, Q, K, A): ').upper().strip()
            if self.has_rank(rank):
                return rank
            print("Можно спрашивать только карты, которые есть у тебя на руках!")

    def ask_count(self):
        """спрашиваем кол-во"""
        while True:
            try:
                k=int(input('Сколько их у противника? (1-3): '))
                if 1<=k<=3:
                    return k
            except ValueError:
                pass
            print ('Введи число от 1 до 3')

    def ask_suits(self, k):
        """спрашиваем масти"""
        print(f'Введи {k} масти (например: черви пики):')
        while True:
            user_input = input('> ').lower().split()

            chosen_suits = [a for a in user_input if a in main_suits]
            if len(chosen_suits) != k:
                print(f'Нужно ввести ровно {k} корректных масти.')
                continue
            return list(set(chosen_suits))

class ChestsGame:
    """ход игры"""
    def __init__(self, money_sys):
        self.money_sys = money_sys
        self.deck = Deck(size=36)

        self.computer = ComputerPlayer("Компьютер")
        self.human = HumanPlayer("Пользователь")

        self.first_player = self.human
        self.second_player = self.computer

    def deal_cards(self):
        """выбираем по сколько карт раздаем.
        Тянем по одной карте по очереди для человека и компьютера
        если колоду вытянуть удалось, то записываем её в руку"""
        print('сколько карт раздавать?')
        number = int(input('> '))
        print('\nРаздача карт...')
        time.sleep(2)
        for i in range(number):
            c1 = self.deck.draw()
            c2 = self.deck.draw()
            if c1: self.human.add_cards([c1])
            if c2: self.computer.add_cards([c2])

    def switch_turn(self):
        """смена хода"""
        self.first_player, self.second_player = self.second_player, self.first_player

    def check_deck(self):
        """если у игрока закончились карты и карты есть в
        колоде, то добираем карты.
        Если карты в колоде тоже закончились, игра завершается"""
        if not self.first_player.hand and self.deck.cards:
            print (f'У {self.first_player.name} закончились карты, додеп...')
            time.sleep(2)
            new_card = self.deck.draw()
            self.first_player.add_cards([new_card])
        if not self.first_player.hand:
            return False
        return True

    def play_turn(self):
        """ход игры"""
        if not self.check_deck():
            # Если карт нет, игра заканчивается
            return False

        print(f'\nХодит {self.first_player.name}')
        time.sleep(2)

        # Спрашиваем карту
        rank = self.first_player.ask_rank()
        if not self.second_player.has_rank(rank):
            print (f'У {self.second_player.name} нет такой карты')
            time.sleep(2)
            self.switch_turn()
            return True
        else:
            print (f'У {self.second_player.name} есть такая карта')
            time.sleep(2)

        # Спрашиваем кол-во
        count_guess = self.first_player.ask_count()
        real_count = self.second_player.count_rank(rank)
        if count_guess != real_count:
            print("Неверное количество! Ход переходит.")
            time.sleep(2)
            self.switch_turn()
            return True

        print("Количество угадано!")
        time.sleep(2)

        # Спрашиваем масти
        suits_guess = self.first_player.ask_suits(count_guess)
        if self.second_player.has_suits(rank, suits_guess):
            print(f"БИНГО! {self.first_player.name} угадал масти и забирает карты!")
            time.sleep(2)
            won_cards = self.second_player.remove_cards_rank(rank)
            self.first_player.add_cards(won_cards)
            return True
        else:
            print("Масти названы неверно.")
            time.sleep(2)
            self.switch_turn()
            return True

    def start_game(self):
        """главный цикл игры"""
        print("\n==СУНДУЧКИ==")
        time.sleep(2)

        bet = self.money_sys.place_bet()
        if bet == 0:
            return

        self.deal_cards() # Раздаем карты

        while True: # Условия конца игры
            try:
                if self.human.chests + self.computer.chests == 9:
                    break
                if not self.play_turn():
                    # Когда карты в колоде закончатся, функция
                    # вернет False => игра закончится
                    break
            except KeyboardInterrupt:
                print("\nВыход...")
                return

        # Итоги игры
        print("\nИГРА ОКОНЧЕНА")
        time.sleep(2)

        print(f"Пользователь: {self.human.chests} | Компьютер: {self.computer.chests}")

        if self.human.chests > self.computer.chests:
            win_amount = bet * 2
            print(f"ПОБЕДА! Выигрыш: {win_amount}")
            self.money_sys.add_money(win_amount)
        elif self.human.chests < self.computer.chests:
            print("Поражение.")
        else:
            print("Ничья. Возврат ставки.")
            self.money_sys.add_money(bet)