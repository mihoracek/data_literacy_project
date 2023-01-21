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
    
    return csv.to_numpy().flatten()

def read_sportka():
    time_info = [
        "Date", "Year", "Week", "Day"
    ]
    draw = [
        f"d{d+1}n{n+1}" for n in range(7) for d in range(2)
    ]

    csv = pd.read_csv(
        "data/sportka.csv",
        sep=';',
        header=0,
        names=time_info + draw,
        usecols=draw
    )
    
    return csv.to_numpy().flatten()

def read_ny_lotto():
    columns = ["Date", "Draw", "Bonus", "Extra"]

    csv = pd.read_csv(
        "data/NY_Lotto.csv",
        sep=',',
        header=0,
        names=columns,
        usecols=["Draw"]
    )

    numbers = [
        [int(n) for n in row.split()] for row in csv["Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

def read_uk_lotto():
    time_info = ["No.", "Day", "DD", "MMM", "YYYY"]
    draw = ["Number 1", "Number 2", "Number 3", "Number 4", "Number 5", "Number 6", "Bonus Number"]
    win_info = ["Jackpot", "Wins", "Machine", "Set"]

    csv = pd.read_csv(
        "data/UK_Lotto_drawn.csv",
        sep=',',
        header=0,
        names=time_info + draw + win_info,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_uk_lotto_tuesday():
    time_info = ["No.", "Day", "DD", "MMM", "YYYY"]
    draw = ["Number 1", "Number 2", "Number 3", "Number 4", "Number 5", "Number 6"]
    win_info = ["Jackpot", "Wins", "Machine", "Set"]

    csv = pd.read_csv(
        "data/UK_Lotto_tuesdays_drawn.csv",
        sep=',',
        header=0,
        names=time_info + draw + win_info,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_texas_lotto():
    time_info = ["Game Name", "Month", "Day", "Year"]
    draw = ["Number 1", "Number 2", "Number 3", "Number 4", "Number 5", "Number 6"]

    csv = pd.read_csv(
        "data/Texas_Lotto.csv",
        sep=',',
        header=0,
        names=time_info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_italy_lotto():
    info = ["Date", "City"]
    draw = ["Number 1", "Number 2", "Number 3", "Number 4", "Number 5"]

    csv = pd.read_csv(
        "data/Italy_Lotto.csv",
        sep=';',
        header=0,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_italy_lotto_super():
    info = ["Date", "No. in year"]
    draw = ["Number 1", "Number 2", "Number 3", "Number 4", "Number 5", "Number 6", "Jolly number"]

    csv = pd.read_csv(
        "data/Italy_Lotto_Super.csv",
        sep=';',
        header=0,
        names=info + draw + ["Superstar number"],
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_italy_lotto_10e():
    info = ["Date", "No. in year"]
    draw = [f"Number {n+1}" for n in range(20)]
    bonus = ["Bonus 1", "Bonus 2"]

    csv = pd.read_csv(
        "data/Italy_Lotto_10e.csv",
        sep=';',
        header=0,
        names=info + draw + bonus,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_israel_lotto():
    info = ["Game", "Date"]
    draw = [f"Number {n+1}" for n in range(6)]

    csv = pd.read_csv(
        "data/Israel_Lotto.csv",
        sep=',',
        header=0,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_australia_monday_lotto():
    info = ["Draw number", "Date"]
    draw = [f"Number {n+1}" for n in range(8)]
    winnings = [f"W{n}" for n in range(24)]

    csv = pd.read_csv(
        "data/Australia_Lotto_mondays.csv",
        sep=',',
        header=0,
        names=info + draw + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_australia_wednesday_lotto():
    info = ["Draw number", "Date"]
    draw = [f"Number {n+1}" for n in range(8)]
    winnings = [f"W{n}" for n in range(24)]

    csv = pd.read_csv(
        "data/Australia_Lotto_wednesdays.csv",
        sep=',',
        header=0,
        names=info + draw + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_australia_saturdays_lotto():
    info = ["Draw number", "Date"]
    draw = [f"Number {n+1}" for n in range(8)]
    winnings = [f"W{n}" for n in range(24)]

    csv = pd.read_csv(
        "data/Australia_Lotto_saturdays.csv",
        sep=',',
        header=0,
        names=info + draw + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_australia_oz_lotto():
    info = ["Draw number", "Date"]
    draw = [f"Number {n+1}" for n in range(6)]
    bonus = ["Bonus 1", "Bonus 2"]
    winnings = [f"W{n}" for n in range(28)]

    csv = pd.read_csv(
        "data/Australia_Lotto_oz.csv",
        sep=',',
        header=0,
        names=info + draw + ["Number 7"] + bonus + ["Bonus 3"] + winnings,
        usecols=draw + bonus    # Number 7 and Bonus got added later, not for all draws
    )

    return csv.to_numpy().flatten()

def read_australia_powerball():
    info = ["Draw number", "Date"]
    draw = [f"Number {n+1}" for n in range(5)]
    ignore = ["Number 6", "Number 7", "Powerball"]
    winnings = [f"W{n}" for n in range(36)]

    csv = pd.read_csv(
        "data/Australia_Powerball.csv",
        sep=',',
        header=0,
        names=info + draw + ignore + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_australia_set4life():
    info = ["Draw number", "Date"]
    draw = [f"Number {n+1}" for n in range(7)]
    bonus = ["Bonus 1", "Bonus 2"]
    winnings = [f"W{n}" for n in range(32)]

    csv = pd.read_csv(
        "data/Australia_Set4Life.csv",
        sep=',',
        header=0,
        names=info + draw + ["Number 8"] + bonus + winnings,
        usecols=draw + bonus
    )

    return csv.to_numpy().flatten()

def read_canada_lotto():
    draw = [f"Number {n+1}" for n in range(7)]

    csv = pd.read_csv(
        "data/Canada_Lotto_649.csv",
        sep=',',
        header=0,
        names=["Date"] + draw + ["Stupid trailing comma"],
        usecols=draw
    )

    return csv.to_numpy().flatten()

readers = [
    read_lotto,
    read_eurojackpot,
    read_sportka,
    read_ny_lotto,
    read_uk_lotto,
    read_uk_lotto_tuesday,
    read_texas_lotto,
    read_italy_lotto,
    read_italy_lotto_super,
    read_italy_lotto_10e,
    read_israel_lotto,
    read_australia_monday_lotto,
    read_australia_wednesday_lotto,
    read_australia_saturdays_lotto,
    read_australia_oz_lotto,
    read_australia_powerball,
    read_australia_set4life,
    read_canada_lotto
]

with open("data/lottery_numbers.txt", "w") as out:
    for read in readers:
        for number in read():
            print(number, file=out)
