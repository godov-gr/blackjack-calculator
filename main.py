import random
import time

# Определяем карты и их значения
cards = {'2': 2, '3': 3, '4': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Стратегия игрока (в соответствии с изображенной схемой)
strategy = [
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 5
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 6
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 7
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 8
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # 9
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],  # 10
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],  # 11
    ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 12
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 13
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 14
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 15
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 16
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 17
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 18
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 19
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 20
]

# Функция для подсчета суммы карт
def calculate_hand(hand):
    value = sum(cards[card] for card in hand)
    # Если сумма больше 21 и есть туз, считаем туз как 1
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Функция для получения стратегии на основе руки игрока и карты дилера
def get_strategy(player_score, dealer_card):
    if player_score < 5 or player_score > 20:
        return 'S'  # Если значение не попадает в таблицу, предположим, что игрок останется на месте
    dealer_index = cards[dealer_card] - 2  # Индекс карты дилера (2-10)
    return strategy[player_score - 5][dealer_index]

# Функция для симуляции одной партии с умным игроком
def play_blackjack_smart():
    deck = list(cards.keys()) * 4
    random.shuffle(deck)

    # Раздаем карты игроку и дилеру
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    player_score = calculate_hand(player_hand)
    dealer_score = calculate_hand(dealer_hand[:1])  # Учитываем только первую карту дилера

    action = get_strategy(player_score, dealer_hand[0])

    if action == 'H':
        return "fold", 1  # Игрок скидывает карты и теряет 1$
    elif action == 'D':
        player_hand.append(deck.pop())  # Игрок удваивает ставку и берет одну карту
        player_score = calculate_hand(player_hand)
        while calculate_hand(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
        dealer_score = calculate_hand(dealer_hand)
        if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
            return "double_loss", 2  # Игрок теряет 2$
        else:
            return "double_win", 2  # Игрок выигрывает 2$
    else:
        while calculate_hand(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
        dealer_score = calculate_hand(dealer_hand)
        if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
            return "loss", 1  # Игрок теряет 1$
        elif player_score > dealer_score or dealer_score > 21:
            return "win", 1  # Игрок выигрывает 1$
        else:
            return "draw", 0  # Ничья, ставка не изменяется

# Функция для запуска симуляции с умным игроком
def simulate_blackjack_smart(rounds=1000000):
    stats = {"win": 0, "loss": 0, "draw": 0, "double_win": 0, "double_loss": 0, "fold": 0}
    player_money = 1
    casino_money = 1

    for _ in range(rounds):
        result, money_change = play_blackjack_smart()
        stats[result] += 1

        # Обновление денег на основе результата
        if result == "win" or result == "double_win":
            player_money += money_change
            casino_money -= money_change
        elif result == "loss" or result == "double_loss" or result == "fold":
            player_money -= money_change
            casino_money += money_change

    return stats, player_money, casino_money

# Запуск симуляции 10 раз с измерением времени для умного игрока
total_results = {"win": 0, "loss": 0, "draw": 0, "double_win": 0, "double_loss": 0, "fold": 0}
total_player_money = 0
total_casino_money = 0

for i in range(10):
    start_time = time.time()  # Время начала
    results, player_money, casino_money = simulate_blackjack_smart()
    end_time = time.time()    # Время окончания
    
    # Подсчет процентов
    total_games = sum(results.values())
    win_percentage = ((results['win'] + results['double_win']) / total_games) * 100
    loss_percentage = ((results['loss'] + results['double_loss'] + results['fold']) / total_games) * 100
    draw_percentage = (results['draw'] / total_games) * 100
    
    # Вывод результатов для каждого запуска
    print(f"Results after 1,000,000 games (Run {i + 1}): {results}")
    print(f"Win percentage: {win_percentage:.2f}%")
    print(f"Loss percentage: {loss_percentage:.2f}%")
    print(f"Draw percentage: {draw_percentage:.2f}%")
    print(f"Player money after 1,000,000 games: ${player_money}")
    print(f"Casino money after 1,000,000 games: ${casino_money}")
    print(f"Time taken: {end_time - start_time:.4f} seconds\n")
    
    # Суммирование результатов
    total_results['win'] += results['win']
    total_results['loss'] += results['loss']
    total_results['draw'] += results['draw']
    total_results['double_win'] += results['double_win']
    total_results['double_loss'] += results['double_loss']
    total_results['fold'] += results['fold']
    total_player_money += player_money
    total_casino_money += casino_money

# Итоговый вывод средних значений и общего результата
print("Final summary after 10 runs:")
average_win_percentage = ((total_results['win'] + total_results['double_win']) / (10 * 1000000)) * 100
average_loss_percentage = ((total_results['loss'] + total_results['double_loss'] + total_results['fold']) / (10 * 1000000)) * 100
average_draw_percentage = (total_results['draw'] / (10 * 1000000)) * 100

print(f"Average win percentage: {average_win_percentage:.2f}%")
print(f"Average loss percentage: {average_loss_percentage:.2f}%")
print(f"Average draw percentage: {average_draw_percentage:.2f}%")
print(f"Total player money after 10 runs: ${total_player_money}")
print(f"Total casino money after 10 runs: ${total_casino_money}")
