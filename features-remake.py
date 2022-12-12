# https://handsontable.github.io/hyperformula/api/
# Import the xlrd module

import xlrd

# Open the Workbook
workbook = xlrd.open_workbook("DATA SHEET.xls")

# Open the worksheet
worksheet = workbook.sheet_by_name("Features Data")

breakers = ["", "Name", "--", "Maniobra", "Nombre Español"]
atributos = ["Acrobatics", "Athletics", "Charm", "Combat", "Command",
             "General Education", "Medicine Education", "Occult Education",
             "Pokemon Education", "Pokémon Education", "Technology Education", "Focus",
             "Guile", "Intimidate", "Intuition", "Perception", "Stealth", "Survival"]
others = ["Elemental Connection"]
rangos = ["Pathetic", "Untrained", "Novice",
          "Adept", "Expert", "Master", "Virtuoso"]
specials = [["Commanderñs Voice", ""],
            ["Agility Training",
                "'Skills': {'And': {'Athetics': 3, 'Command':2}}"],
            ["Brutal Training",
                "'Skills': {'And': {'Intimidate': 3, 'Command':2}}"],
            ["Inspired Training",
                "'Skills': {'And': {'Charm': 3, 'Command':2}}"],
            ["Walk It Off", "'Skills': {'And': {'Athetics': 4, 'Focus':3}}"],
            ["Face Me Whelp", ""],
            ["Species Savant", ""],
            ["Brawler", ""],
            ["Beautiful Ballet Rank 1", ""],
            ["Cool Conduct Rank 1", ""],
            ["Cute Cuddle Rank 1", ""],
            ["Tough Tumble Rank 1", ""],
            ["Stat Ace", ""],
            ["Type Ace", ""],
            ["Sneak Attack", ""],
            ["Defense Ace", ""],
            ["Special Attack Ace", ""],
            ["Special Defense Ace", ""],
            ["Attack Ace", ""],
            ["Speed Ace", ""],
            ["Provocateur", ""],
            ["Focused Command",
                "'Skills': {'And': {'Command':6}, 'Or': {'Focus':6, 'Guile':6, 'Intimidate':6, 'Pokemon Education':6}}"],
            ["Tutoring", ""],
            ["Type Sync", ""],
            ["Hydro Jet", ""],
            ["Waterñs Shroud", ""],
            ["Engineer", "'Edges': ['Pokebot Training']"],
            ["Backpacker", "'Edges': ['Traveler']"],
            ["Jailbreaker", "'Edges': ['Basic Balls']"],
            ["Pheromone Markers", "'Feats': ['Swarmlord'], 'Skills':{'Or':{'Command': 4, 'Survival': 4}}"],
            ["Overgrowth", "'Feats': ['Druid'], 'Skills':{'Or':{'General Education': 4, 'Survival': 4}}"],
            ["Earthshifter", "'Feats': ['Earth Shaker'], 'Skills':{'Or':{'Focus': 4, 'Intuition': 4}}"],
            ["Fighterñs Versatility", ""],
            ["First Aid Expertise",
                "'Edges': ['Medic Training'], 'Skills':{'And':{'Medicine Education': 5}}"],
            ["Poke Ball Crafter",
                "'Edges': ['Basic Balls', 'Poké Ball Repair'], 'Skills':{'And':{'Technology Education': 5}}"],
            ["Poké Ball Crafter",
                "'Edges': ['Basic Balls', 'Poké Ball Repair'], 'Skills':{'And':{'Technology Education': 5}}"],
            ["Psionic Sight", "'Edges': ['Elemental Connection (Psychic)']"],
            ["Telekinetic", "'Edges': ['Elemental Connection (Psychic)', 'Iron Mind']"],
            ["Telepath", "'Edges': ['Elemental Connection (Psychic)', 'Iron Mind'], 'Skills':{'And':{'Intuition': 3}}"],
            ["Channeler", "'Edges': ['Mystic Senses']"],
            ["Aura Guardian", "'Edges': ['Elemental Connection (Fighting)']"],
            ["Crystal Artificer", "'Edges': ['Gem Lore']"],
            ["Chemist", "'Edges': ['Repel Crafter']"],
            ["Tumbler", "'Edges': ['Acrobat']"],
            ["Top Tier Berries", "'Edges': ['Green Thumb']"],
            ["Signature Move", ""],
            ["Type Expertise", ""],
            ["Skill Monkey", ""],
            ["Mentor", ""], ["Highlander", ""], ["Unconquerable", ""], [
                "Tyrantñs Roar", ""], ["This Will Not Stand", ""],
            ["Fashionista", ""],
            ["Rogue", ""], ["Arcane Favor", ""], ["Fey Trance", ""],
            ["Researcher",
                "'Skills': {'Or': {'General Education': 3, 'Medicine Education': 3, 'Occult Education': 3, 'Pokémon Education': 3, 'Technology Education': 3 }}"],
            ["Let Me Help You With That", ""],
            ["Cheerleader",
                "'Feats': ['Inspired Training'], 'Skills': {'And': {'Charm': 3}}"],
            ["Medical Techniques [Medic]",
                "'Feats': ['Medic'], 'Skills': {'And': {'Medicine Education': 4}}"],
            ["Iñm A Doctor Rank 1", "'Feats': ['Medic']"],
            ["Iñm A Doctor Rank 2",
                "'Feats': ['Medic'], 'Skills': {'And': {'Medicine Education': 4}}"],
            ["Front Line Healer", "'Feats': ['Medic']"]]

db = "["

class baseFeat:
    def __init__(self, Name, Prereq, Effect, Tags, Freq):
        self.Name = Name
        self.Prereq = Prereq
        self.Effect = Effect
        self.Tags = Tags
        self.Freq = Freq

    def toString(self):
        solution = '{"Name": "' + self.Name + '",\n "Effect": "' + \
            self.Effect + '",\n "Freq": "' + self.Freq + '",\n "Prereq": '
        solution += str(self.Prereq).replace("\'", "\"") + '\n'
        solution = solution[:-1] + ',\n "Tags": ['
        for tag in self.Tags:
            solution += '"'+tag+'",'
        solution = solution[:-1] + ']\n}'
        return solution

class baseFeat2:
    def __init__(self, Name, Prereq, Effect, Tags, Freq):
        self.Name = Name
        self.Prereq = Prereq
        self.Effect = Effect
        self.Tags = Tags
        self.Freq = Freq

    def toString(self):
        solution = '"' +self.Name +'": {"Name": "' + self.Name + '",\n "Effect": "' + \
            self.Effect + '",\n "Freq": "' + self.Freq + '",\n "Prereq": '
        solution += str(self.Prereq).replace("\'", "\"") + '\n'
        solution = solution[:-1] + ',\n "Tags": ['
        for tag in self.Tags:
            solution += '"'+tag+'",'
        solution = solution[:-1] + ']\n}'
        return solution


globalHolder = []

# Iterate the rows and columns
for i in range(0, worksheet.nrows):
    if worksheet.cell_value(i, 0) not in breakers:
        thisFeat = baseFeat2("Feat", "", "Nothing", ["Tag", "Tags"], "Never")
        cell = worksheet.cell_value(i, 2)
        thisFeat.Name = worksheet.cell_value(i, 0).replace("\'", "ñ")
        formula = ""
        featName = worksheet.cell_value(i, 0).replace("\'", "ñ").replace(
            "\n", " ").replace("\"", "ñ").replace("\\", "").replace("\r", " ")
        thisFeat.Prereq = "'UNCHANGED'"
        thisFeat.Effect = worksheet.cell_value(i, 4).replace("\'", "ñ").replace(
            "\n", " ").replace("\"", "ñ").replace("\\", "").replace("\r", " ")
        thisFeat.Freq = worksheet.cell_value(i, 3).replace("\'", "ñ")

        ## TAGS ##

        tagHolder = worksheet.cell_value(i, 1)
        tagHolder = tagHolder.replace("[", "").replace(
            "] ", " ").replace("]", " ").split(" ")
        tagArray = []
        i = 0
        while i < len(tagHolder):
            if tagHolder[i] != '':
                if tagHolder[i] in ["Special", "+Special"] and i+1 < len(tagHolder):
                    tagArray.append(tagHolder[i] + " " + tagHolder[i+1])
                    i += 1
                else:
                    tagArray.append(tagHolder[i])
            i += 1
        thisFeat.Tags = tagArray

        ## Prereq ##
        preBody = {
        }

        # Prereqs especiales que sería una movida parsear
        done = False
        for special in specials:
            if featName == special[0]:
                if special[1] != "":
                    preBody = '{'+special[1].replace("\"", "\'")+'}'
                else:
                    preBody["Special"] = featName
                done = True
        if done:
            thisFeat.Prereq = preBody
            db += thisFeat.toString() + ',\n'
            globalHolder.append(featName)
            continue

        # Procesamos feats
        moddedCell = cell
        preBody['Feats'] = []
        for entry in globalHolder:
            if entry in moddedCell:
                if entry == "Medic":
                    print('+++++', featName, "--", entry, "--", moddedCell)
                preBody['Feats'].append(entry.replace("\'", "ñ").replace(
                    "\n", " ").replace("\"", "ñ").replace("\\", "").replace("\r", " "))
                moddedCell.replace(entry, '')

        # Vamos a tratar estos datos
        moddedCell = moddedCell.replace(",", "").split(' ')
        eduCount = 0
        for entry, next in zip(moddedCell, moddedCell[1:]):
            if next == "Education":
                moddedCell[eduCount] += ' Education'
            eduCount += 1

        # Los que necesitan Atributos
        atrCount = 2
        isOr = " or " in cell
        isAnd = " and " in cell
        condArr = {}

        rankList = []
        rankCount = 1
        for rank in rangos:
            for word in cell.split(' '):
                if word == rank:
                    rankList.append([rank, rankCount])
            rankCount += 1

        if len(rankList) > 0:
            isAnd = True
            if featName == "Medic":
                print(moddedCell)
            for att in atributos:
                for word in moddedCell:
                    if word == att:
                        condArr[word] = rankList[0][1]
                        if featName == "Medic":
                            print(att, word, '--', condArr)

        # Gestiona statements
        if isOr and condArr != {}:
            preBody['Skills'] = {'Or': condArr}
        elif isAnd and condArr != {}:
            preBody['Skills'] = {'And': condArr}

        if preBody['Feats'] == []:
            preBody.pop('Feats')

        thisFeat.Prereq = preBody
        db += thisFeat.toString() + ',\n'

        if featName != "Medic":
            globalHolder.append(featName)

with open("results/feats-remake.json", "w", encoding="utf-8") as outfile:
    db = db[:-2] + "]"
    db = db.replace("ñ", "\'")
    db = db.replace("–", "-")
    db = db.replace("’", "\'")
    db = db.replace("“", "\'")
    db = db.replace("”", "\'")
    outfile.write(db)
