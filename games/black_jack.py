import time
from games.cards import Deck

class BlackjackGame:
    def __init__(self, money_sys):
        self.money_sys = money_sys
        self.player_hand = []
        self.dealer_hand = []

    def get_card_value(self, card):
        # Наш класс Card имеет поля .rank и .suit
        rank = card.rank
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)

    def calculate_score(self, hand):
        """Рассчитывает сумму очков в руке с учетом тузов"""
        score = sum(self.get_card_value(card) for card in hand)
        aces = sum(1 for card in hand if card.rank == 'A')

        # Пока перебор и есть тузы, превращаем их из 11 в 1
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    def draw_card(self, hand, visible=True):
        # Если колода пуста (или её нет), создаем новую колоду
        if not hasattr(self, 'deck') or len(self.deck) == 0:
            self.deck = Deck(size=52)  # ЗДЕСЬ МЫ БЕРЕМ 52 КАРТЫ

        # Используем метод .draw() нашего класса Deck
        card = self.deck.draw()
        hand.append(card)

        if visible:
            # card теперь объект, поэтому используем card.rank, а не card['rank']
            print(f"  Карта: {card}")
            time.sleep(1)

        return card

    def show_hand(self, hand, owner="Игрок", hide_first_card=False):
        """Показывает карты в руке"""
        print(f"\nКарты {owner}:")
        time.sleep(1)

        if hide_first_card and owner == "Дилер":
            print(f"  1. [СКРЫТА]")
            time.sleep(1)
            for i in range(1, len(hand)):
                print(f"  {i + 1}. {hand[i]}")

            print(f"  Сумма: ? + {self.calculate_score(hand[1:])}")
            time.sleep(1)

        else:
            for i, c in enumerate(hand, 1):
                print(f"  {i}. {c}")
            print(f"  Сумма: {self.calculate_score(hand)}")
            time.sleep(1)

    def start_game(self):
        """
        Основной игровой метод (аналог start_game в других твоих играх).
        """
        print("\n==БЛЭКДЖЕК==")

        # Цикл на 5 раундов
        for i in range (5):
            # Делаем ставку через money_system
            bet = self.money_sys.place_bet()
            if bet == 0:
                break

            # Запуск раунда
            self.play_round(bet)

            # Спрашиваем про продолжение
            if input("\nИграем дальше? (Enter - да, 0 - выход): ") == '0':
                break

    def play_round(self, bet):
        """Логика одного раунда"""
        self.deck = Deck(size=52)
        self.player_hand = []
        self.dealer_hand = []

        print("\nРаздача...")
        time.sleep(1)
        # Игрок
        self.draw_card(self.player_hand)
        self.draw_card(self.player_hand)
        # Дилер
        self.draw_card(self.dealer_hand)
        self.draw_card(self.dealer_hand, visible=False)  # Вторая карта скрыта

        self.show_hand(self.player_hand, "Игрок")
        self.show_hand(self.dealer_hand, "Дилер", hide_first_card=True)

        # Проверка на мгновенный Блэкджек (сразу 21)
        p_score = self.calculate_score(self.player_hand)
        if p_score == 21:
            print("\nБЛЭКДЖЕК!")
            # Проверим дилера
            d_score = self.calculate_score(self.dealer_hand)
            if d_score == 21:
                print("У дилера тоже Блэкджек. Ничья.")
                self.money_sys.add_money(bet)  # Возврат ставки
            else:
                win = int(bet * 2.5)  # 3 к 2
                print(f"Победа 3:2! Выигрыш: {win}")
                self.money_sys.add_money(win)
            return  # Раунд окончен

        # Ход игрока
        while True:
            choice = input("\n1. Взять (Hit)\n2. Стоп (Stand)\n3. Удвоить (Double)\nВыбор: ")

            if choice == '1':  # Hit
                self.draw_card(self.player_hand)
                self.show_hand(self.player_hand, "Игрок")
                if self.calculate_score(self.player_hand) > 21:
                    print("\nПЕРЕБОР! Вы проиграли.")
                    return  # Деньги уже ушли при ставке

            elif choice == '2':  # Stand
                break

            elif choice == '3':  # Double
                if self.money_sys.balance >= bet:
                    self.money_sys.balance -= bet  # Списываем доп. ставку
                    bet *= 2  # Удваиваем текущую ставку
                    print(f"Ставка удвоена: {bet}")

                    self.draw_card(self.player_hand)  # Только одна карта
                    self.show_hand(self.player_hand, "Игрок")

                    if self.calculate_score(self.player_hand) > 21:
                        print("\nПЕРЕБОР! Вы проиграли.")
                        return
                    break  # После удвоения ход переходит дилеру
                else:
                    print("Недостаточно денег для удвоения!")

            else:
                print("Неверный ввод")

        # Ход дилера
        print("\nХод дилера")
        self.show_hand(self.dealer_hand, "Дилер", hide_first_card=False)  # Открываем карту

        while self.calculate_score(self.dealer_hand) < 17:
            print("Дилер берет карту...")
            time.sleep(1)
            self.draw_card(self.dealer_hand)
            self.show_hand(self.dealer_hand, "Дилер")

        # Итоги
        p_sum = self.calculate_score(self.player_hand)
        d_sum = self.calculate_score(self.dealer_hand)

        print(f"\nИтог: Вы {p_sum} vs Дилер {d_sum}")

        if d_sum > 21:
            print("Дилер перебрал! Вы выиграли!")
            self.money_sys.add_money(bet * 2)
        elif d_sum > p_sum:
            print("Дилер победил.")
        elif d_sum < p_sum:
            print("Вы победили!")
            self.money_sys.add_money(bet * 2)
        else:
            print("Ничья.")
            self.money_sys.add_money(bet)
