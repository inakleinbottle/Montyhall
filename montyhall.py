"""
Package for simulating the Monty Hall game with various strategies.

This package provides the `MontyHallExperiment` class, that is used to
run a number of simulations on a Monty Hall type problem and determine,
empirically, the probability of success using a given strategy. The
classical Monty Hall problem is provided as `CLASSICAL_MONTY_HALL`.
This is a pre-instantiated experiment with three doors carrying equal
probabilities.

The strategy should be a function that takes two arguments, the
list of available doors and a list of past selections. The function
should return the number, from the doors list, of the selected door.
Two standard strategies are implemented here, the always swap stategy
(optimum solution for the classical problem) and the never swap
strategy.
"""
import random
import functools
import inspect
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import accumulate

__all__ = [
    "Door", 
    "MontyHallExperiment", 
    "CLASSICAL_MONTY_HALL", 
    "always_swap", 
    "never_swap",
]

class Door:
    """
    Door for use in a Monty Hall experiment.

    Each door can be given an custom probability if this differs from
    the classical case of equal probabilities.
    """

    def __init__(self, probability=None):
        if probability is not None:
            assert 0 < probability < 1, "Probability must be between 0 and 1"
        self.probability = probability

    def __repr__(self):
        return f"Door(probabilty={self.probability})"

    def __str__(self):
        return f"Door with probability {self.probability}"


def experiment(doors, strategy, correct):
    """
    Function that runs the actual experiment.

    A selection is first chosen at random. Then, whilst there are at
    least 3 doors remaining, the host reveals one incorrect door that
    is not the door most recently selected. Then the contestant's
    strategy is applied to obtain the next selection.

    Once only two doors remain, the experiment returns True if the most
    recent selection was the correct door, and False otherwise.
    """
    selections = [random.choice(doors)]
    while len(doors) > 2:
        elim = random.choice([d for d in doors if not d == correct
                              if not d == selections[-1]])
        doors.remove(elim)
        selections.append(strategy(doors, selections))
    return selections[-1] == correct
        

class MontyHallExperiment:
    """
    Monty Hall type problem experiment.

    The available doors can be specified individually when creating an
    experiment object, or by using the keyword-only number_of_doors
    parameter. 
    """

    def __init__(self, *doors, number_of_doors=None, experiment=experiment):
        if number_of_doors and doors:
            raise ValueError("Number of doors and individual doors cannot be"
                             " specified together")
        if number_of_doors:
            prob = 1./number_of_doors
            doors = [Door(prob) for _ in range(number_of_doors)]
        else:
            doors = list(doors)
            number_of_doors = len(doors)

        existing = sum(d.probability for d in doors 
                       if d.probability is not None)
        if not existing <= 1:
            raise ValueError("existing probability sum to more than 1")
            
        prob = (1. - existing)/number_of_doors

        for door in doors:
            if door.probability is None:
                door.probability = prob

        self.doors = doors

        self.experiment = experiment

    def get_correct_doors(self, number):
        """
        Generate the sequence of correct doors randomly according to
        the probability assigned to each door.

        This is a generator function.
        """
        cum_weights = list(accumulate(d.probability for d in self.doors))
        for _ in range(number):
            rand_no = random.random()
            yield min(i for i, w in enumerate(cum_weights)
                      if rand_no < w)

    def run_simulations(self, strategy, number=1000, max_workers=None):
        """
        Run the number of simulations.

        Simulations are run concurrently in individual processes. For
        this reason, the provided strategy must be a function and not a
        lambda. The maximum numbers of worker processes can be 
        controlled by the `max_workers` parameter. By default, this is
        the number of cores of the host computer.

        Returns the proportion of experiments that were successful.
        """
        start = time.time()
        assert inspect.isfunction(strategy), "strategy must be a function"
        doors = list(range(len(self.doors)))
        func = functools.partial(self.experiment, doors, strategy) 
        with ProcessPoolExecutor(max_workers=max_workers) as pool:
            results = pool.map(func, self.get_correct_doors(number))
            successes = sum(1 for r in results if r)
        print(f"Ran {number} simulations in {time.time() - start} seconds")
        return successes / number


def always_swap(doors, past_selections):
    """
    Strategy that always swaps when given a chance.

    This is the optimum strategy for the classical Monty Hall problem.
    """
    return min(i for i in doors if not i == past_selections[-1])

def never_swap(doors, past_selections):
    """
    Strategy that never swaps when given a chance.
    """
    return past_selections[-1]


CLASSICAL_MONTY_HALL = MontyHallExperiment(number_of_doors=3)
