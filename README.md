# Telegram Game of Life Bot
Another useless Telegram Bot.

## About
This project is an implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using a Telegram bot. The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input.

## How it works
TL;DR

Every message sent to the group can start the process to create a new ecosystem or evolve the current ecosystem. The ecosystem can die because of the normal algorithm or custom variations. An organism can die because of the normal algorithm or custom variations. Every new ecosystem, evolution or die (of the entire ecosystem, not organism) will be notified to the group. End.

---

In this implementation, every message sent to the group where the bot is added can start the evolution process based on some probabilities.

When a message is sent to the group, different actions come into play:

NOTE: all the probabilities can be set on .env file.

### New ecosystem
If there are no ecosystem alive, the probability of a new ecosystem being born is 20% by default. This offers some uncertainty in not knowing when a new ecosystem will be created.

### Evolution
When there is a living ecosystem, the probability of new evolution depends on the number of the messages received after new ecosystem born. By default, every message increase 1% this probability, so, at least every 100 messages the ecosystem will evolve.

When a new evolution occurs, there are again some actions:
#### Ecosystem
- By default, there is a 2% that the entire ecosystem die (epidemic, meteorite, natural disaster...)
- Every evolution can increase this probability, in order to add some "oldness" or "degradation". By default, every evolution increases 0,1%.

#### Organisms
When en ecosystem evolve, the basic algorithm for "Game of Life" starts, but with some additions.

In this implementation, there are not only "organisms" in general; there are 2 main groups: Flora and Fauna. And there are a "free" interpretations about the "Trophic levels". In addition, every level has a "survival" value (1 to 4), that represents the probability to survive in the entire ecosystem. For example, a flower is more fragile than a wolf.

**Flora**

The flora organisms are all the organisms related, well, with flora: plants, flowers, trees, mushrooms... This organism is categorized as "Trophic Level 0", and the survival level is 1.

**Fauna**

In this group there are basically animals, and has different subgroups (Trophic Levels):

_Level1_: basically insects like bees, flies, ants, bugs... The survival level is 1.

_Level2_: small animals like rabbits, squirrels, small birds, goats... These animals are generally herbivorous. The survival level is 2.

_Level3_: bigger animals, like pigs, cows, monkeys, giraffes, elephants... These animals are generally omnivores, but not as dangerous as predators. The survival level is 3.

_Level4_: basically, big predators and mostly carnivores, like lions, tigers, sneaks, wolfs... The survival level is 4.

With this, when the basic algorithm determine that an organism keep alive, the following actions starts:
- The neighbors are relevant. In resume, if neighbors are more dangerous than the organism, the organism can be devoured.
- If the organism is not devoured, there is a default probability of 5% that the organism die suddenly (ill, accident...). This value can be modified with every evolution (by default, increases 0.1%).
- If the organism is not devoured or die suddenly, keep alive.

## GenAI integration
GenAI? What can the GenAI do in an simple algorithm to create end destroy ecosystems?

By default, when some events occurs, a message is sent to the group. For example, "New ecosystem is being born...", "The ecosystem has died" or "Ecosystem evolving...".

Well, the idea here is to generate this messages using GenAI. For example, instead of "New ecosystem is being born...", is more interesting "In a newly planted forest, animals and plants begin to adapt and relate, forming a new ecosystem."

This feature is in beta, so, you know, and for now, there are options to user OpenAI or AzureOpenAI services.

The prompts and pre-prompts are defined on `utils/prompts`

## How to use
The recommended use is using Docker:

1. Clone the project
2. Rename .env.template file to .env
3. Fill the required parameters on .env, and change the probabilities if you want.
4. Run docker compose with `docker compose up -d`
5. Wait for your ecosystem to be born, and enjoy.

If you want to run directly with Python:

1. Clone the project
2. Rename .env.template file to .env
3. Fill the required parameters on .env, and change the probabilities if you want.
4. Run `pip install -r requirements.txt`
5. Run `python app.py`
6. Wait for your ecosystem to be born, and enjoy.

## Some links
The probabilities defined may seem chosen randomly, and in some ways they are, but not entirely. Here are some links:

- https://www.nature.com/articles/d43978-021-00105-7
- https://www.sciencedirect.com/science/article/pii/S1755436522000020
- https://www.weforum.org/agenda/2021/09/pandemics-epidemics-disease-covid-likelyhood/
- https://elordenmundial.com/mapas-y-graficos/probabilidad-morir-siendo-adulto-mundo/