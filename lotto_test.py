"""Testing of Lottery class"""

from typing import Callable, cast, TypeVar, Tuple
import unittest
import time
from lottery import Lottery

TCallable = TypeVar("TCallable", bound=Callable)


class TestConstructor(unittest.TestCase):
    """Tests of Lottery class"""

    def _good(function: TCallable) -> TCallable:
        """Constructor should run without exception"""

        def wrapper(self, *args, **kwargs):  # type: ignore
            return_value = function(self, *args, **kwargs)
            available_tickets, number_of_guesses, max_number, ticket_cost = return_value
            game = Lottery(
                available_tickets=available_tickets,
                number_of_guesses=number_of_guesses,
                max_number=max_number,
                ticket_cost=ticket_cost,
            )
            self.assertEqual(game.available_tickets, available_tickets)
            self.assertEqual(game.customers.shape, (available_tickets,))
            self.assertEqual(game.last_customer_id, 0)
            self.assertEqual(game.number_of_guesses, number_of_guesses)
            self.assertEqual(game.tickets_sold, 0)
            self.assertEqual(game.tickets.shape, (available_tickets, number_of_guesses))
            self.assertEqual(game.max_number, max_number)
            self.assertEqual(game.ticket_cost, ticket_cost)
            self.assertEqual(game.win_per_customer_id, {})
            self.assertEqual(game.winner_numbers.shape, (number_of_guesses,))
            return return_value

        return cast(TCallable, wrapper)

    def _bad(function: TCallable) -> TCallable:
        """Constructor should run exception"""

        def wrapper(self, *args, **kwargs):  # type: ignore
            return_value = function(self, *args, **kwargs)
            available_tickets, number_of_guesses, max_number, ticket_cost = return_value
            with self.assertRaises(Exception):
                Lottery(
                    available_tickets=available_tickets,
                    number_of_guesses=number_of_guesses,
                    max_number=max_number,
                    ticket_cost=ticket_cost,
                )
            return return_value

        return cast(TCallable, wrapper)

    @_bad
    def test_constructor_no_ticket_to_sell(self) -> Tuple[int, int, int, float]:
        """no tickets to sell"""
        available_tickets = 0
        number_of_guesses = 5
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_good
    def test_constructor_one_ticket_to_sell(self) -> Tuple[int, int, int, float]:
        """no tickets to sell"""
        available_tickets = 1
        number_of_guesses = 5
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_bad
    def test_constructor_no_number_to_guess(self) -> Tuple[int, int, int, float]:
        """no number to guess"""
        available_tickets = 100
        number_of_guesses = 0
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_good
    def test_constructor_one_number_to_guess(self) -> Tuple[int, int, int, float]:
        """no tickets to sell"""
        available_tickets = 100
        number_of_guesses = 1
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_bad
    def test_constructor_number_of_guesses_bigger_than_max_number(
        self,
    ) -> Tuple[int, int, int, float]:
        """number of guesses bigger than max number"""
        available_tickets = 100
        number_of_guesses = 91
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_good
    def test_constructor_number_of_guesses_equal_to_max_number(
        self,
    ) -> Tuple[int, int, int, float]:
        """number of guesses bigger than max guessable number"""
        available_tickets = 100
        number_of_guesses = 90
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_good
    def test_constructor_number_of_guesses_less_than_max_number(
        self,
    ) -> Tuple[int, int, int, float]:
        """number of guesses are less than tha maximu guessable number"""
        available_tickets = 100
        number_of_guesses = 89
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost

    @_good
    def test_constructor_normal(self) -> Tuple[int, int, int, float]:
        """Normal functioning of constructor"""
        available_tickets = 100
        number_of_guesses = 5
        max_number = 90
        ticket_cost = 1.0
        return available_tickets, number_of_guesses, max_number, ticket_cost


class SpeedTest(unittest.TestCase):
    """Performance tests of Lottery class"""

    def test_game_runtime_one_user(self) -> None:
        """a 1 million ticket game with a 5/90 lotto runs faster than 7.5 s"""
        start = time.time()
        available_tickets = 100000
        number_of_guesses = 5
        max_number = 90
        ticket_cost = 1.0
        game = Lottery(
            available_tickets=available_tickets,
            number_of_guesses=number_of_guesses,
            max_number=max_number,
            ticket_cost=ticket_cost,
        )
        game.buy_ticket(100000)
        game.draw_winners()
        end = time.time()
        print(end - start)
        self.assertLess(end - start, 10)


if __name__ == "__main__":
    unittest.main()
