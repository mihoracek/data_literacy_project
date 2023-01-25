import pandas as pd
from functools import reduce

def read_lotto():
    json = pd.read_json("data/LottoNumberArchive/Lottonumbers_complete.json")
    data = json["data"]
    numbers = [data[day]["Lottozahl"] for day in range(len(data))]
    return reduce(lambda a, b: a + b, numbers)

def read_eurojackpot():
    lottery_draw = [
        "Number 1", "Number 2", "Number 3", "Number 4", "Number 5", "Eurozahl 1", "Eurozahl 2"
    ]
    winnings = [    # Lottery prize in the draw and no. of winners and their winnings for each of 12 categories
        f"{i+1}" for i in range(12 * 2)
    ]

    csv = pd.read_csv(
        "data/Eurojackpot.csv",
        sep=';',
        header=0,
        names=["Date"] + lottery_draw + ["Prize"] + winnings,
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
        "data/Czech_Republic_Sportka.csv",
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

def read_ny_cash4life():
    columns = ["Date", "Draw", "Cash Ball"]

    csv = pd.read_csv(
        "data/NY_Cash4Life.csv",
        sep=',',
        header=0,
        names=columns,
        usecols=["Draw"]
    )

    numbers = [
        [int(n) for n in row.split()] for row in csv["Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

def read_ny_mega_millions():
    columns = ["Date", "Draw", "Mega Ball", "Multiplier"]

    csv = pd.read_csv(
        "data/NY_Mega_Millions.csv",
        sep=',',
        header=0,
        names=columns,
        usecols=["Draw"]
    )

    numbers = [
        [int(n) for n in row.split()] for row in csv["Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

def read_ny_pick_10():
    columns = ["Date", "Draw"]

    csv = pd.read_csv(
        "data/NY_Pick_10.csv",
        sep=',',
        header=0,
        names=columns,
        usecols=["Draw"]
    )

    numbers = [
        [int(n) for n in row.split()] for row in csv["Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

def read_ny_powerball():
    columns = ["Date", "Draw", "Multiplier"]

    csv = pd.read_csv(
        "data/NY_Powerball.csv",
        sep=',',
        header=0,
        names=columns,
        usecols=["Draw"]
    )

    numbers = [
        [int(n) for n in row.split()] for row in csv["Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

class read_ny_quick_draw:
    def __init__(self, year):
        self.year = year
    
    def __call__(self):
        columns = ["Date", "Draw No.", "Draw Time", "Draw", "Extra"]

        csv = pd.read_csv(
            f"data/NY_Quick_Draw_{self.year}.csv",
            sep=',',
            header=0,
            names=columns,
            usecols=["Draw"]
        )

        numbers = [
            [int(n) for n in row.split()] for row in csv["Draw"]
        ]

        return reduce(lambda a, b: a + b, numbers)

def read_ny_take_5():
    columns = ["Date", "Evening Draw", "Evening Bonus", "Midday Draw", "Midday Bonus"]

    csv = pd.read_csv(
        "data/NY_Take_5.csv",
        sep=',',
        header=0,
        names=columns,
        usecols=["Evening Draw", "Midday Draw"]
    )

    numbers = [
        [int(n) for n in row.split()] for row in csv["Evening Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

def read_poland_lotto():
    info = ["Index", "Date"]
    draw = [f"Number {n+1}" for n in range(6)]

    csv = pd.read_csv(
        "data/Poland_Lotto.csv",
        sep=',',
        header=None,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_poland_lotto_plus():
    info = ["Index", "Date"]
    draw = [f"Number {n+1}" for n in range(6)]

    csv = pd.read_csv(
        "data/Poland_Lotto_Plus.csv",
        sep=',',
        header=None,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_poland_lotto_mini():
    info = ["Index", "Date"]
    draw = [f"Number {n+1}" for n in range(5)]

    csv = pd.read_csv(
        "data/Poland_Lotto_Mini.csv",
        sep=',',
        header=None,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_poland_multi():
    info = ["Index", "Date", "Time"]
    draw = [f"Number {n+1}" for n in range(20)]

    csv = pd.read_csv(
        "data/Poland_Multi.csv",
        sep=',',
        header=None,
        names=info + draw + ["Bonus"],
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_euromillions():
    draw = [f"Number {n+1}" for n in range(5)]
    bonus = ["Star 1", "Star 2"]

    csv = pd.read_csv(
        "data/Euromillions.csv",
        sep=',',
        header=0,
        names=["Date"] + draw + bonus,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_belgium_lotto():
    draw = [f"Number {n+1}" for n in range(6)]

    csv = pd.read_csv(
        "data/Belgium_Lotto.csv",
        sep=',',
        header=0,
        names=["Date"] + draw + ["Bonus"],
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_belgium_keno():
    draw = [f"Number {n+1}" for n in range(20)]

    csv = pd.read_csv(
        "data/Belgium_Keno.csv",
        sep=',',
        header=0,
        names=["Date"] + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_slovakia_keno10():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(20)]

    csv = pd.read_csv(
        "data/Slovakia_Keno10.csv",
        sep=';',
        header=0,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_slovakia_keno_10():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(20)]

    csv = pd.read_csv(
        "data/Slovakia_Keno_10.csv",
        sep=';',
        header=0,
        names=info + draw,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_slovakia_lotto1():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(6)] + ["Bonus"]
    winnings = [f"Win Info {n+1}" for n in range(20)]

    csv = pd.read_csv(
        "data/Slovakia_Lotto1.csv",
        sep=';',
        header=0,
        names=info + draw + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_slovakia_lotto2():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(6)] + ["Bonus"]
    winnings = [f"Win Info {n+1}" for n in range(19)]

    csv = pd.read_csv(
        "data/Slovakia_Lotto2.csv",
        sep=';',
        header=0,
        names=info + draw + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_slovakia_lotto_535():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(5)]
    winnings = [f"Win Info {n+1}" for n in range(12)]

    csv = pd.read_csv(
        "data/Slovakia_Lotto_535.csv",
        sep=';',
        header=0,
        names=info + draw + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_nh_keno_603():
    info = ["Name", "Date", "Time", "Draw No."]
    draw = ["Draw"]

    csv = pd.read_csv(
        "data/NH_Keno_603.csv",
        sep=',',
        header=0,
        names=info + draw + ["Bonus"] + ["Stupid trailing comma"],
        usecols=draw
    )

    numbers = [
        [int(n) for n in row.split("-")] for row in csv["Draw"]
    ]

    return reduce(lambda a, b: a + b, numbers)

def read_slovakia_sportka1():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(6)]
    winnings = [f"Win Info {n+1}" for n in range(20)]

    csv = pd.read_csv(
        "data/Slovakia_Sportka1.csv",
        sep=';',
        header=0,
        names=info + draw + ["Bonus"] + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

def read_slovakia_sportka2():
    info = ["Index", "Date", "Week"]
    draw = [f"Number {n+1}" for n in range(6)]
    winnings = [f"Win Info {n+1}" for n in range(19)]

    csv = pd.read_csv(
        "data/Slovakia_Sportka2.csv",
        sep=';',
        header=0,
        names=info + draw + ["Bonus"] + winnings,
        usecols=draw
    )

    return csv.to_numpy().flatten()

class read_dc_keno:
    def __init__(self, year):
        self.year = year
    
    def __call__(self):
        info = ["Date", "Draw No."]

        csv = pd.read_csv(
            f"data/DC_Keno_{self.year}.csv",
            sep=',',
            header=0,
            names=info + ["Draw"],
            usecols=["Draw"]
        )

        numbers = [
            [int(n) for n in row.split()] for row in csv["Draw"]
        ]

        return reduce(lambda a, b: a + b, numbers)

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
    read_canada_lotto,
    read_ny_cash4life,
    read_ny_mega_millions,
    read_ny_pick_10,
    read_ny_powerball,
    read_ny_take_5,
    read_poland_lotto,
    read_poland_lotto_plus,
    read_poland_lotto_mini,
    read_poland_multi,
    read_euromillions,
    read_belgium_lotto,
    read_belgium_keno,
    read_slovakia_keno_10,
    read_slovakia_lotto1,
    read_slovakia_lotto2,
    read_slovakia_lotto_535,
    read_nh_keno_603,
    read_slovakia_sportka1,
    read_slovakia_sportka2,
    read_dc_keno(2021)
    # read_ny_quick_draw,
]

with open("data/lottery_numbers.txt", "w") as out:
    for read in readers:
        for number in read():
            print(number, file=out)
