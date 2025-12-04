class MoneySystem:
    """виртуальный кошелек и управление балансом"""
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance # ставим начальный баланс 1000

    def get_balance(self):
        return self.balance

    def add_money(self, amount):
        """Добавить деньги"""
        if amount > 0:
            self.balance += amount
            print(f"Баланс пополнен на {amount}. Текущий: {self.balance}")
        else:
            print("Сумма пополнения должна быть положительной.")

    def place_bet(self):
        """Запрашивает ставку у пользователя и списывает её,
        если хватает средств"""
        while True:
            print(f"\nВаш баланс: {self.balance}")
            try:
                bet_input = int(input("Сделайте вашу ставку (0 для выхода): "))

                if bet_input == 0:
                    return 0

                # проверяем, хватает ли пользователю денег
                if bet_input > self.balance:
                    print("Недостаточно средств!")
                elif bet_input < 0:
                    print("Ставка не может быть отрицательной.")
                else:
                    self.balance -= bet_input
                    return bet_input

            except ValueError:
                print("Ошибка ввода.")