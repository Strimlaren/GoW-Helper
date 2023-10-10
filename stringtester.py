string = """Yasmine 5
Orpheus 10
Gaard 15
"""

def find_medal_rewards(string):
    medals = {"Gaard": 0, "Yasmine": 0, "Orpheus": 0, "Aranaea": 0, "Anu": 0, "Nysha": 0}
    temp = string.splitlines()
    num = ""

    for medal in medals:  # Gaard
        for item in temp:  # "mic x1"
            if item.find(medal) != -1:  # if Gaard is in medals
                for char in item:
                    if char.isnumeric():
                        num += char
                medals[medal] = int(num)
                num = ""
    print(medals)

find_medal_rewards(string)