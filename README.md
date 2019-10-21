# Montyhall
This package provides tools for running simulations of the Monty Hall problem and similar problems and determining how many of those simulations are successful.

## Background
The Monty Hall gameshow has a simple premise. There are three doors,
behind one of which is a prize. The contestant is asked to choose one
door. The host will then reveal another door that does not conceal the
prize. The contestant is then given the opportunity to swap.

Conventional thinking would suggest that at this stage, each of the
remaining two doors has an equal probability of concealing the prize,
but this is not the case. Indeed, at the beginning, each door has an
equal probability, one in three (1/3), of being the prize door. Say
the contestant chooses door A. Then door A has a 1/3 probability of
being correct while, combined, the probability that either B or C is
correct is 2/3. The host now reveals one of the remaining doors to be
false, say door B. Now the probability that one of door B or C is the
prize door is still 2/3, but we have the additional information that
the probability that door B is correct is 0, so all of this 2/3
probability that B or C is correct must lie with door C. Thus the
contestant is twice as likely to win if they swap to door C.

## Example - The classical Monty Hall problem
To run experiments for the classical Monty Hall problem, we can used the pre-defined `CLASSICAL_MONTY_HALL` experiment object.
```python3
>>> from montyhall import CLASSICAL_MONTY_HALL, always_swap, never_swap
>>> CLASSICAL_MONTY_HALL.run_simulations(always_swap)
0.669
>>> CLASSICAL_MONTY_HALL.run_simulations(never_swap)
0.315
```
After the default (1000) number of experiments, the estimated probability of success using the `always_swap` strategy is roughly 0.666 (2/3), while that of the `never_swap` strategy is roughly 0.333 (1/3), as expected. (Note that the simulations have a random element, so your results may differ.)

## Example - A variation on the classical problem
The `MontyHallExperiment` class can be used to run simulations for variations of the classical problem. For example, if instead we have four doors carrying equal probabilities then we can run the corresponding simulations as follows.
```python3
>>> from montyhall import MontyHallExperiment, always_swap, never_swap
>>> exp = MontyHallExperiment(number_of_doors=4)
>>> exp.run_simulations(always_swap)
0.612
>>> exp.run_simulations(never_swap)
0.28
```
Alternatively, we can control the probability that a given door is the correct door in the experiment by providing the doors explicitly.
```python3
>>> from montyhall import always_swap, never_swap, MontyHallExperiment, Door
>>> exp = MontyHallExperiment(Door(0.5), Door(0.3), Door(0.2))
>>> exp.run_simulations(always_swap)
0.672
>>> exp.run_simulations(never_swap)
0.332
```

## Installation
At present, the package can only be installed manually.

Clone the repository from github using
```
git clone https://github.com/inakleinbottle/Montyhall.git
```


## License
This package is shared under the MIT license (see LICENSE.txt).





