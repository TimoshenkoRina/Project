import random
from time import sleep

class Roulette:
    "логика игры"
    def __init__(self, money_sys):
        self.wheel_numbers = list(range(37)) # Список чисел 0-36
        self.reds = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.money_sys = money_sys

    def spin_wheel(self):
        """вращаем рулетку"""
        print("\n Катится крутится...")
        sleep(1)
        result = random.choice(self.wheel_numbers) # Выбираем результат вращения
        color= self.get_color(result)
        # запоминаем цвет и число
        print(f"Выпало число: {result} ({color})")
        return result

    def get_color(self, number):
        """смотрим цвет"""
        if number == 0:
            return 'зеленый'
        elif number in self.reds:
            return 'красный'
        else:
            return 'черный'

    def get_bet_details(self):
        """выбор пользователя"""
        print("\n1. Число (x35)\n2. Цвет (x2)\n3. Чет/Нечет (x2)\n4. Выход")
        choice = input("Выбор: ")

        if choice == '1':
            try:
                num = int(input("Число (0-36): "))
                if 0 <= num <= 36:
                    return {'type': 'number', 'value': num, 'k': 35}
                    # 'type' тип ставки, 'value' значение, 'k' коэффициент
            except ValueError:
                pass
        elif choice == '2':
            c = input("1-Красное, 2-Черное: ")
            if c == '1': return {'type': 'color', 'value': 'красный', 'k': 2}
            if c == '2': return {'type': 'color', 'value': 'черный', 'k': 2}
        elif choice == '3':
            p = input("1-Чет, 2-Нечет: ")
            if p == '1': return {'type': 'parity', 'value': 0, 'k': 2}
            if p == '2': return {'type': 'parity', 'value': 1, 'k': 2}
        elif choice == '4':
            return None

        print("Неверный выбор.")
        return None

    def check_win(self, result, bet_details):
        """проверяем коэффициент ставки"""
        win_k = 0 # коэффициент выигрыша (по умолчанию - 0 как проигрыш)

        if bet_details['type'] == 'number':
            if result == bet_details['value']: win_k = bet_details['k']

        elif bet_details['type'] == 'color':
            if self.get_color(result) == bet_details['value']: win_k = bet_details['k']

        elif bet_details['type'] == 'parity':
            if result != 0 and result % 2 == bet_details['value']: win_k = bet_details['k']

        return win_k

    def start_game(self):
        """ход игры"""
        print("\nРУЛЕТКА")
        for i in range (5):
            # смотрим сколько денег у игрока
            bet = self.money_sys.place_bet()
            if bet == 0: break

            # выбираем режим игры
            details = self.get_bet_details()
            if not details:
                # если пользователь ничего не выбрал и функция
                # равна None, нужно отменить ставку и вернуть деньги
                self.money_sys.add_money(bet)
                continue

            result = self.spin_wheel()
            multiplier = self.check_win(result, details)

            if multiplier > 0:
                # считаем выигрыш и изначальную ставку (+1)
                win = bet * (multiplier + 1)
                print(f"ПОБЕДА! Выигрыш: {win}")
                # начисляем выигрыш
                self.money_sys.add_money(win)
            else:
                print("Проигрыш.")