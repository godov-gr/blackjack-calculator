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
    for _ in range(rounds):
        result = play_blackjack()
        stats[result] += 1

    return stats

# Запуск симуляции с измерением времени
start_time = time.time()  # Время начала
results = simulate_blackjack()
end_time = time.time()    # Время окончания

# Подсчет процентов
total_games = sum(results.values())
win_percentage = (results['win'] / total_games) * 100
loss_percentage = (results['loss'] / total_games) * 100
draw_percentage = (results['draw'] / total_games) * 100

# Вывод результатов и времени выполнения
print(f"Results after 1000 games: {results}")
print(f"Win percentage: {win_percentage:.2f}%")
print(f"Loss percentage: {loss_percentage:.2f}%")
print(f"Draw percentage: {draw_percentage:.2f}%")
print(f"Time taken: {end_time - start_time:.4f} seconds")
