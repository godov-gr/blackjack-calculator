import random
import time

# Определяем карты и их значения
cards = {'2': 2, '3': 3, '4': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Функция для подсчета суммы карт
def calculate_hand(hand):
    value = sum(cards[card] for card in hand)
    # Если сумма больше 21 и есть туз, считаем туз как 1
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Функция для симуляции одной партии
def play_blackjack():
    deck = list(cards.keys()) * 4
    random.shuffle(deck)

    # Раздаем карты игроку и дилеру
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Ход игрока
    while calculate_hand(player_hand) < 17:  # Игрок останавливается на 17 и выше
        player_hand.append(deck.pop())

    # Ход дилера
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    player_score = calculate_hand(player_hand)
    dealer_score = calculate_hand(dealer_hand)

    # Определение победителя
    if player_score > 21:
        return "loss"
    elif dealer_score > 21 or player_score > dealer_score:
        return "win"
    elif player_score < dealer_score:
        return "loss"
    else:
        return "draw"

# Функция для запуска симуляции
def simulate_blackjack(rounds=1000000):
    stats = {"win": 0, "loss": 0, "draw": 0}
    player_money = 1
    casino_money = 1

    for _ in range(rounds):
        result = play_blackjack()
        stats[result] += 1

        # Обновление денег на основе результата
        if result == "win":
            player_money += 1
            casino_money -= 1
        elif result == "loss":
            player_money -= 1
            casino_money += 1

    return stats, player_money, casino_money

# Запуск симуляции 10 раз с измерением времени
total_results = {"win": 0, "loss": 0, "draw": 0}
total_player_money = 0
total_casino_money = 0

for i in range(10):
    start_time = time.time()  # Время начала
    results, player_money, casino_money = simulate_blackjack()
    end_time = time.time()    # Время окончания
    
    # Подсчет процентов
    total_games = sum(results.values())
    win_percentage = (results['win'] / total_games) * 100
    loss_percentage = (results['loss'] / total_games) * 100
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
    total_player_money += player_money
    total_casino_money += casino_money

# Итоговый вывод средних значений и общего результата
print("Final summary after 10 runs:")
average_win_percentage = (total_results['win'] / (10 * 1000000)) * 100
average_loss_percentage = (total_results['loss'] / (10 * 1000000)) * 100
average_draw_percentage = (total_results['draw'] / (10 * 1000000)) * 100

print(f"Average win percentage: {average_win_percentage:.2f}%")
print(f"Average loss percentage: {average_loss_percentage:.2f}%")
print(f"Average draw percentage: {average_draw_percentage:.2f}%")
print(f"Total player money after 10 runs: ${total_player_money}")
print(f"Total casino money after 10 runs: ${total_casino_money}")
