"Lottery application"

from typing import Callable, cast, TypeVar, Tuple
import logging
import configparser
from nptyping import NDArray, Int, Shape
import numpy
from numpy.random import default_rng

TCallable = TypeVar("TCallable", bound=Callable)

config = configparser.ConfigParser()
config.read("lottery.cfg")
LEVEL = logging.DEBUG
if config["DEFAULT"]["logging"] == "INFO":
    LEVEL = logging.INFO
elif config["DEFAULT"]["logging"] == "WARNING":
    LEVEL = logging.WARNING
elif config["DEFAULT"]["logging"] == "ERROR":
    LEVEL = logging.ERROR
elif config["DEFAULT"]["logging"] == "CRITICAL":
    LEVEL = logging.CRITICAL

logging.basicConfig(filename="lottery.log", level=LEVEL)


def outputless_logger(function: TCallable) -> TCallable:
    """logs functions without return value"""

    def wrapper(*args, **kwargs):  # type: ignore
        """outputless wrapper"""
        logging.info(function.__name__)
        return function(*args, **kwargs)

    return cast(TCallable, wrapper)


def generic_logger(function: TCallable) -> TCallable:
    """logs functions with return value"""

    def wrapper(*args, **kwargs):  # type: ignore
        """generic wrapper"""
        logging.info(function.__name__)
        return_value = function(*args, **kwargs)
        logging.info(return_value)
        return return_value

    return cast(TCallable, wrapper)


class Lottery:
    """Lottery"""

    available_tickets: int
    customers: numpy.ndarray
    last_customer_id: int
    max_number: int
    number_of_guesses: int
    tickets_sold: int
    tickets: NDArray[Shape["*, ..."], Int]
    ticket_cost: float
    win_per_customer_id: dict
    winner_numbers: numpy.ndarray

    @outputless_logger
    def __init__(
        self,
        available_tickets: int,
        number_of_guesses: int,
        max_number: int,
        ticket_cost: float,
    ):
        if max_number > 255:
            logging.error("Maximum number is bigger than 255")
            raise Exception("Max number is bigger than 255")
        if available_tickets <= 0:
            logging.error("No tickets to sell")
            raise Exception("No tickets to sell")
        if number_of_guesses <= 0:
            logging.error("No numbers to guess")
            raise Exception("No numbers to guess")
        if number_of_guesses > max_number:
            logging.error("Max number is bigger than number of guesses")
            raise Exception("Max number is bigger than number of guesses")
        logging.info("available_tickets %i", available_tickets)
        logging.info("number_of_guesses %i", number_of_guesses)
        logging.info("max_number %i", max_number)
        logging.info("ticket_cost %f", ticket_cost)
        self.available_tickets = available_tickets
        self.customers = numpy.zeros((available_tickets))
        self.last_customer_id = 0
        self.max_number = max_number
        self.number_of_guesses = number_of_guesses
        self.rng = default_rng()
        self.tickets_sold = 0
        self.tickets = numpy.zeros(
            (self.available_tickets, self.number_of_guesses), dtype="uint8"
        )
        self.ticket_cost = ticket_cost
        self.win_per_customer_id = {}
        self.winner_numbers = numpy.array(numpy.zeros(self.number_of_guesses))

    @generic_logger
    def __random_numbers(self) -> numpy.ndarray:
        logging.info("max number %s", self.max_number)
        logging.info("number of guesses %s", self.number_of_guesses)
        random_numbers = self.rng.choice(
            self.max_number, size=self.number_of_guesses, replace=False
        )
        logging.debug(random_numbers)
        return random_numbers

    @generic_logger
    def buy_ticket(self, ticket_amount: int) -> Tuple[int, numpy.ndarray]:
        """Buys "ticket_amount" of tickets"""
        logging.info("ticket amount %i", ticket_amount)
        if ticket_amount + self.tickets_sold > self.available_tickets:
            logging.error("Not enough tickets to buy.")
            raise Exception("Not enough tickets to buy.")
        numbers_drawn = numpy.array(
            [self.__random_numbers() for n in range(ticket_amount)], dtype="uint8"
        )
        logging.debug("numbers_drawn")
        logging.debug(numbers_drawn)
        self.tickets[
            self.tickets_sold : self.tickets_sold + ticket_amount
        ] = numbers_drawn
        logging.debug("tickets")
        logging.debug(self.tickets)
        self.customers[
            self.tickets_sold : self.tickets_sold + ticket_amount
        ] = numpy.full((ticket_amount), self.last_customer_id)
        logging.debug("customers")
        logging.debug(self.customers)
        self.tickets_sold += ticket_amount
        logging.debug("tickets_sold %i", self.tickets_sold)
        logging.debug("last_customer_id %i", self.last_customer_id)
        self.last_customer_id += 1
        return self.last_customer_id - 1, numbers_drawn

    @generic_logger
    def __calculate_prize_won(self, winners: numpy.ndarray) -> None:
        logging.debug("winners")
        logging.debug(winners)
        if self.tickets_sold != self.available_tickets:
            logging.error("Not all tickets sold")
            raise Exception("Not all tickets sold")
        slot_prize_pool = (
            self.ticket_cost * self.tickets_sold
        ) / self.number_of_guesses
        logging.debug("Prize pools %f", slot_prize_pool)
        count_matches = numpy.unique(winners, return_counts=True)
        logging.debug("count_matches")
        logging.debug(count_matches)
        slot_winners = [
            count_matches[1][number] if number in count_matches[0] else 0
            for number in range(self.number_of_guesses + 1)
        ]
        logging.debug("slot_winners")
        logging.debug(slot_winners)
        worth_of_win = [
            slot_prize_pool / share if share != 0 else 0 for share in slot_winners
        ]
        logging.debug("worth_of_win")
        logging.debug(worth_of_win)
        self.win_per_customer_id = {}
        for customer_id in range(self.last_customer_id):
            self.win_per_customer_id[customer_id] = 0
        for ticket_id, customer in enumerate(self.customers):
            number_of_matches = winners.T[ticket_id]
            customer_id = customer
            self.win_per_customer_id[customer_id] += worth_of_win[number_of_matches]
        logging.debug("win_per_customer")
        logging.debug(self.win_per_customer_id)

    @generic_logger
    def draw_winners(self) -> Tuple[numpy.ndarray, dict]:
        """After all tickets sold, calculate prizes of winners."""
        logging.debug("asd")
        if self.tickets_sold != self.available_tickets:
            logging.error("Not all tickets sold")
            raise Exception("Not all tickets sold")
        self.winner_numbers += self.__random_numbers()
        logging.debug("winner_numbers")
        logging.debug(self.winner_numbers)
        matches = numpy.full(self.tickets.shape, False)
        for i in self.winner_numbers:
            matches |= self.tickets == i
        winners = numpy.count_nonzero(matches, axis=1)
        logging.debug("winners")
        logging.debug(winners)
        self.__calculate_prize_won(winners)
        return self.winner_numbers, self.win_per_customer_id
