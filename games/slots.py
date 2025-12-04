import random
import time

symbols = ['I', 'T', 'M', 'O'] # символы, которые перебираем
k = {'JACKPOT': 100, '4_SAME': 20, '3_SAME': 5} # пишем коэффициенты

class SlotsGame:
    def __init__(self, money_sys):
        self.money_sys = money_sys

    def get_combination(self):
        """крутим барабаны используя рандом"""
        return [random.choice(symbols) for i in range(4)]

    def check_win(self, combo):
        """проверка на джекпот"""
        if combo == ['I', 'T', 'M', 'O']:
            return 'JACKPOT', k['JACKPOT']

        # проверяем сколько раз каждый символ встречается в строке
        counts = [combo.count(s) for s in set(combo)]

        if max(counts) == 4: return '4_SAME', k['4_SAME']
        if max(counts) == 3: return '3_SAME', k['3_SAME']

        # возвращаем именно этот формат, потому что
        # функция возвращает значения в формате 18 строчки
        # (return 'JACKPOT', k['JACKPOT'])
        return 'NONE', 0

    def start_game(self):
        """ход игры"""
        print("\n==СЛОТЫ ITMO==")
        time.sleep(0.5)
        print("\nДЖЕКПОТ ITMO: x100")
        print("4 одинаковых: x20")
        print("3 одинаковых: x5")
        time.sleep(0.5)

        # запускаем 5 прокруток
        for i in range (5):
            # проверяем баланс
            bet = self.money_sys.place_bet()
            if bet == 0: return

            print("\nКрутим барабаны")
            time.sleep(1)

            combo = self.get_combination() # вращаем барабаны
            print(f"\nRESULT: {' '.join(combo)}")
            time.sleep(1)

            win_type, mult = self.check_win(combo)

            if mult > 0:
                win_real = bet * mult
                print(f"{win_type}! Выигрыш: {win_real}. Додеп??")
                self.money_sys.add_money(win_real + bet)
            else:
                print("Проигрыш. Додеп?")