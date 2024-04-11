# Telegram Game of Life Bot

## About
This project is an implementation of Conway's Game of Life using a Telegram bot. The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input.

## How it works

In this implementation, every message sent to the group where the bot is added can start the evolution process based on some probabilities, so the evolution will not be always the same as in the basic algorithm.

When a message is sent to the group, different actions come into play:
### New ecosystem
If there are no ecosystem alive, the probability that a new ecosystem can be born is set on .env file (default 20%).

### Evolution
When there is a living ecosystem, the probability of new evolution depends on the number of the messages received after new ecosystem born. By default, every message increase 1% this probability, so, at least every 100 messages the ecosystem will evolve.

When a new evolution occurs, there are again some actions:
#### Ecosystem
- By default, there is a 2% that the entire ecosystem die
- Every evolution can increase this probability, in order to add some "oldness". By default, every evolution increases 0,1%.

#### Organisms
When en ecosystem evolve, the basic algorithm for "Game of Life" starts, but with some additions. In this implementation, there are not only "organisms" in general; there are 2 main groups: Flora and Fauna. There are a "free" interpretations about the "Trophic levels", and every level has a "survival" value, that represents the probability to survive in the entire ecosystem.

For example, a flower is more fragile than a wolf.

**Flora**

The flora organisms are all the organisms related, well, with flora: plants, flowers, mushrooms... This organism is categorized as "Trophic Level 0". The survival level is 1.

**Fauna**

In this group there are basically animals, a lot of, and has different sub groups (Trophic Levels):

_Level1_: bees, flies, bugs... The survival level is 1.

_Level2_: small animals like rabbits, squirrels, small birds, deers, goats... These animals are generally herbivorous. The survival level is 2.

_Level3_: bigger animals, like pigs, cows, monkeys, giraffes, elephants... These animals are generally omnivores, but not very dangerous or predatory. The survival level is 3.

_Level4_: basically, big predators and mostly carnivores, like lions, tigers, sneaks, wolfs... The survival level is 4.

With this, when the basic algorithm determine that an organism keep alive, the following actions starts:
- The neighbors are relevant. In resume, if neighbors are more dangerous than the organism, the organism can be devoured.
- If the organism is not devoured, there is a basic probability that the organism die suddenly (by default, 5%). This value can be modified with every evolution (by default, increases 0.1%).
- If the organism is not devoured or die suddenly, keep alive.

## How to use
The recommended use is using Docker:

1. Clone the project
2. Rename .env.template file to .env
3. Fill the required parameters on .env, and change the probabilities if you want.


If you want to run directly with Python: