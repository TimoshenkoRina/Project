from money_system import MoneySystem
from games.chests import ChestsGame
from games.roll import Roulette
from games.slots import SlotsGame
from games.black_jack import BlackjackGame

def main():
    """главная функция запуска консоли"""
    # создаем один кошелек на всю игру, пока не прервется код
    wallet = MoneySystem(initial_balance=1000)

    while True:
        # выводим каждый раз в меню актуальный баланс и список игр
        print(f"\nГЛАВНОЕ МЕНЮ | Баланс: {wallet.get_balance()}")
        print("1. Сундучки")
        print("2. Рулетка")
        print("3. Слоты")
        print("4. Блэкджек")
        print("0. Выход")

        choice = input("Выбор > ")

        # запускаем все игры
        if choice == '1':
            game = ChestsGame(wallet)
            game.start_game()
        elif choice == '2':
            game = Roulette(wallet)
            game.start_game()
        elif choice == '3':
            game = SlotsGame(wallet)
            game.start_game()
        elif choice == '4':
            game = BlackjackGame(wallet)
            game.start_game()
        elif choice == '0':
            print("Пока!")
        else:
            print("Неверный ввод")

# запускаем программу
if __name__ == "__main__":
    main()