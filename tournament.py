import random
import pathlib

from schnapsen.game import SchnapsenGamePlayEngine
from schnapsen.bots import RandBot, RdeepBot, IS_project_bot

from schnapsen.bots.ml_bot import create_replay_memory_dataset, train_model, MLPlayingBot

bot1_sample = RandBot(rand=random.Random(), name="randbot")
bot2 = RdeepBot = RdeepBot(num_samples= 2, depth = 2, rand=random.Random(), name="RdeepBot")


create_replay_memory_dataset(bot1=bot1_sample, bot2=bot2)
train_model('LR')

engine = SchnapsenGamePlayEngine()

model_dir = "ML_models"
model_name = "simple_model"
model_location = pathlib.Path(model_dir) / model_name

myrepeats = 50

bot1 = IS_project_bot(name="IS_project_bot")
bot3 = MLPlayingBot(model_location=model_location, name="MLBot")

bots = [bot1, bot2, bot3]
n = len(bots)
wins = {str(bot): 0 for bot in bots}
matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

totalgames = (n * n - n) / 2 * myrepeats
playedgames = 0

print("Playing {} games:".format(int(totalgames)))
for a, b in matches:
    for r in range(myrepeats):
        if random.choice([True, False]):
            p = [a, b]
        else:
            p = [b, a]

        winner_id, game_points, score = engine.play_game(
            bots[p[0]], bots[p[1]], random.Random(45)
        )

        wins[str(winner_id)] += game_points

        playedgames += 1
        print(
            "Played {} out of {:.0f} games ({:.0f}%): {} \r".format(
                playedgames, totalgames, playedgames / float(totalgames) * 100, wins
            )
        )

bots = [bot1, bot2]
n = len(bots)
wins = {str(bot): 0 for bot in bots}
matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

totalgames = (n * n - n) / 2 * myrepeats
playedgames = 0

print("Playing {} games:".format(int(totalgames)))
for a, b in matches:
    for r in range(myrepeats):
        if random.choice([True, False]):
            p = [a, b]
        else:
            p = [b, a]

        winner_id, game_points, score = engine.play_game(
            bots[p[0]], bots[p[1]], random.Random(45)
        )

        wins[str(winner_id)] += game_points

        playedgames += 1
        print(
            "Played {} out of {:.0f} games ({:.0f}%): {} \r".format(
                playedgames, totalgames, playedgames / float(totalgames) * 100, wins
            )
        )

bots = [bot1, bot3]
n = len(bots)
wins = {str(bot): 0 for bot in bots}
matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

totalgames = (n * n - n) / 2 * myrepeats
playedgames = 0

print("Playing {} games:".format(int(totalgames)))
for a, b in matches:
    for r in range(myrepeats):
        if random.choice([True, False]):
            p = [a, b]
        else:
            p = [b, a]

        winner_id, game_points, score = engine.play_game(
            bots[p[0]], bots[p[1]], random.Random(45)
        )

        wins[str(winner_id)] += game_points

        playedgames += 1
        print(
            "Played {} out of {:.0f} games ({:.0f}%): {} \r".format(
                playedgames, totalgames, playedgames / float(totalgames) * 100, wins
            )
        )