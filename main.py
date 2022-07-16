"Example of lottery usage"

from lottery import Lottery

if __name__ == "__main__":
    game = Lottery(
        available_tickets=10, number_of_guesses=5, max_number=90, ticket_cost=1
    )
    print(game.buy_ticket(3))
    print(game.buy_ticket(3))
    print(game.buy_ticket(4))
    print(game.draw_winners())
