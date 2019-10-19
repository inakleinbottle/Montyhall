from itertools import accumulate
import random
import concurrent.futures as cf
import functools

class Door:

    def __init__(self, probability=None):
        if probability is not None:
            assert 0 < probability < 1, "Probability must be between 0 and 1"
        self.probability = probability



def experiment(doors, strategy, correct):
    selections = [random.choice(doors)]
    while len(doors) > 2:
        elim = random.choice([d for d in doors if not d == correct
                              if not d == selections[-1]])
        doors.pop(elim)
        selections.append(strategy(doors, selections))
    return selections[-1] == correct
        

class MontyHallExperiment:

    def __init__(self, *doors, number_of_doors=None):
        if number_of_doors and doors:
            raise ValueError("Number of doors and individual doors cannot be"
                             " specified together")
        if number_of_doors:
            prob = 1./number_of_doors
            doors = [Door(prob) for _ in range(number_of_doors)]
        else:
            doors = list(doors)

        existing = sum(d.probability for d in doors 
                       if d.probability is not None)
        if not existing <= 1:
            raise ValueError("existing probability sum to more than 1")
            
        prob = (1. - existing)/number_of_doors

        for door in doors:
            if door.probability is None:
                door.probability = prob

        self.doors = doors

    def get_correct_doors(self, number):
        cum_weights = list(accumulate(d.probability for d in self.doors))
        for _ in range(number):
            rand_no = random.random()
            yield min(i for i, w in enumerate(cum_weights)
                      if rand_no < w)

    def run_simulations(self, strategy, number=1000):
        """
        Run the number of simulations.
        """
        doors = list(range(len(self.doors)))
        func = functools.partial(experiment, doors, strategy) 
        with cf.ProcessPoolExecutor() as pool:
            results = pool.map(func, self.get_correct_doors(number))
            successes = sum(1 for r in results if r)
        return successes / number


def always_swap(doors, past_selections):
    return min(i for i in doors if i not in past_selections)

