import pandas as pd
from functools import reduce

def read_lotto():
    json = pd.read_json("data/LottoNumberArchive/Lottonumbers_complete.json")
    data = json["data"]
    numbers = [data[day]["Lottozahl"] for day in range(len(data))]
    return reduce(lambda a, b: a + b, numbers)

def read_eurojackpot():
    lottery_draw = [
        "Date", "Number 1", "Number 2", "Number 3", "Number 4", "Number 5", "Eurozahl 1", "Eurozahl 2"
    ]
    winnings = [    # Lottery prize in the draw and no. of winners and their winnings for each of 12 categories
        "Prize"] + [f"{i+1}" for i in range(12 * 2)
    ]

    csv = pd.read_csv(
        "data/EJ_ab_2018.csv",
        sep=';',
        header=0,
        names=lottery_draw + winnings,
        usecols=lottery_draw
    )
    numbers = [
        [a, b, c, d, e] for a, b, c, d, e in zip(
            csv["Number 1"], csv["Number 2"], csv["Number 3"], csv["Number 4"], csv["Number 5"]
        )
    ]

    return reduce(lambda a, b: a + b, numbers)

lotto_numbers = read_lotto()
eurojackpot_numbers = read_eurojackpot()

with open("lotto_numbers.txt", "w") as out:
    for number in lotto_numbers:
        print(number, file=out)
    for number in eurojackpot_numbers:
        print(number, file=out)
