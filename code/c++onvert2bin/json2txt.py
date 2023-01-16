import pandas as pd
from functools import reduce

json = pd.read_json("data/LottoNumberArchive/Lottonumbers_complete.json")
data = json["data"]
numbers = [data[day]["Lottozahl"] for day in range(len(data))]
collapsed = reduce(lambda a, b: a + b, numbers)
test = bytearray(collapsed)

with open("./lotto_numbers.txt", "w") as out:
    # out.write(test)
    for number in collapsed:
        print(number, file=out)
