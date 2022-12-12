# Import the xlrd module
import xlrd, xlwt, re

# Open the Workbook
workbook = xlrd.open_workbook("DATA SHEET.xls")

# Open the worksheet
worksheet = workbook.sheet_by_name("Features Data")

breakers = ["", "Name", "--", "Maniobra", "Nombre Español"]
atributos = ["Acrobatics", "Athletics", "Charm", "Combat", "Command",
            "General Education", "Medicine Education", "Occult Education",
            "Pokémon Education", "Technology Education", "Focus",
            "Guile", "Intimidate", "Intuition", "Perception", "Stealth", "Survival"]
others = ["Elemental Connection"]
rangos = ["Pathetic", "Untrained", "Novice", "Adept", "Expert", "Master", "Virtuoso"]
specials = [["Atributo Especializado", '=IF(COUNTIF(B2:B18, ">=3"),TRUE,FALSE)'],
            ["Virtuoso", '=AND(COUNTIF(B2:B18, ">=6"), B1>=20)'],
            ["Agility Training", '=AND(Athletics>=3, Command>=2)'],
            ["Brutal Training", '=AND(Intimidate>=3, Command>=2)'],
            ["Inspired Training", '=AND(Charm>=3, Command>=2)'],
            ["Walk It Off", '=AND(Athletics>=4, Focus>=3)'],
            ["Face Me Whelp", '=SPECIAL(Face Me Whelp)'],
            ["Brawler", '=SPECIAL(Brawler)'],
            ["Beautiful Ballet Rank 1", '=SPECIAL(Beautiful Ballet Rank 1)'],
            ["Cool Conduct Rank 1", '=SPECIAL(Cool Conduct Rank 1)'],
            ["Cute Cuddle Rank 1", '=SPECIAL(Cute Cuddle Rank 1)'],
           # ["Smart Scheme Rank 1", '=SPECIAL(Smart Scheme Rank 1)'],
            ["Tough Tumble Rank 1", '=SPECIAL(Tough Tumble Rank 1)'],
            ["Stat Ace", '=SPECIAL(Stat Ace)'],
            ["Defense Ace", '=SPECIAL(Defense Ace)'],
            ["Special Attack Ace", '=SPECIAL(Special Attack Ace)'],
            ["Special Defense Ace", '=SPECIAL(Special Defense Ace)'],
            ["Attack Ace", '=SPECIAL(Attack Ace)'],
            ["Speed Ace", '=SPECIAL(Speed Ace)'],
            ["Inspired Training", '=AND(Charm>=3, Command>=2)'],
            ["Focused Command", '=AND(Command>=6, =OR(Focus>=6, Guile>=6, Intimidate>=6, Pokémon Education>=6))'],
            ["Tutoring", '=AND(General Education>=3, SPECIAL(Tutoring))'],
            ["Mentor", '=SPECIAL(Mentor)'],
            ["Fashionista", '=SPECIAL(Fashionista)'],
            ["Rogue", '=SPECIAL(Rogue)'],
            ["Cheerleader", '=AND(Inspired Training, Charm>=3)'],]

db="["
class baseFeat:
    def __init__(self, Name, Prereq, Effect, Tags, Freq):
        self.Name = Name
        self.Prereq = Prereq
        self.Effect = Effect
        self.Tags = Tags
        self.Freq = Freq
    def toString(self):
        solution = '{"Name": "'+ self.Name +'",\n "Effect": "'+ self.Effect +'",\n "Freq": "'+ self.Freq +'",\n "Prereq": '
        solution += '"'+ self.Prereq +'"\n'
        solution = solution[:-1] + ',\n "Tags": ['
        for tag in self.Tags:
            solution += '"'+tag+'",'
        solution = solution[:-1] + ']\n}'
        return solution

globalHolder = []

# Iterate the rows and columns
for i in range(0, worksheet.nrows):
    if worksheet.cell_value(i, 0) not in breakers:
        thisFeat = baseFeat("Feat", "", "Nothing", ["Tag", "Tags"], "Never")
        cell = worksheet.cell_value(i, 2)
        thisFeat.Name = worksheet.cell_value(i, 0).replace("\'", "ñ")
        formula = ""
        featName = worksheet.cell_value(i, 0).replace("\'", "ñ")
        thisFeat.Prereq = "SPECIAL("+featName+")"

        if featName == "Moment of Action [Playtest]":
            print(repr(worksheet.cell_value(i, 4)))
        thisFeat.Effect = worksheet.cell_value(i, 4).replace("\'", "ñ").replace("\n", " ").replace("\"", "ñ").replace("\\", "").replace("\r", " ")
        thisFeat.Freq = worksheet.cell_value(i, 3).replace("\'", "ñ")

        ## TAGS ##

        tagHolder = worksheet.cell_value(i, 1)
        tagHolder = tagHolder.replace("[", "").replace("] ", " ").replace("]", " ")
        tagArray = []
        for entry in tagHolder.split(" "):
            if entry != '':
                tagArray.append(entry)
        thisFeat.Tags = tagArray

        ## PREREQUISITES ##

        # Si -, siempre se puede
        if cell == "-":
            formula = "true"
            thisFeat.Prereq = formula
            db += thisFeat.toString() + ',\n'
            continue
        
        # Prereqs especiales que sería una movida parsear
        done = False
        for special in specials:
            if featName == special[0]:
                thisFeat.Prereq = special[1]
                done = True
        if done:
            db += thisFeat.toString() + ',\n'
            continue

        # Los que necesitan nivel
        if "Nivel" in cell:
            formula = "TrainerLevel>=" + cell[5:]
            thisFeat.Prereq = formula
            db += thisFeat.toString() + ',\n'
            continue

        # Los que necesitan atributos
        atrCount = 2
        atrColumn = "B"
        condArr = []
        isOr = " or " in cell
        isAnd = " and " in cell
        skillCount = []
        rakCount = 1
        for skill in rangos:
            for word in cell.split(' '):
                if word == skill:
                    skillCount.append([skill, rakCount])
            rakCount+=1
        if(len(skillCount) > 1):
            isAnd=True
            abiCount = 0
            modded = cell.replace(",", "")
            for att in atributos:
                for word in modded.split(' '):
                    if word == att:
                        condArr.append(word+">=" + str(skillCount[0][1]))

        for atr in atributos:
            if atr in cell:
                count = 1
                for ran in rangos:
                    if ran in cell:
                        condArr.append(atr+">=" + str(count))
                    count = count+1
            atrCount += 1
        
        # Gestiona statements
        if isOr:
            formula = "=OR("
            for cond in condArr:
                formula += cond + ","
            thisFeat.Prereq = formula[:-1] + ")"
        elif isAnd:
            formula = "=AND("
            for cond in condArr:
                formula += cond + ","
            thisFeat.Prereq = formula[:-1] + ")"
        elif len(condArr)>0:
            formula = condArr[0]
            thisFeat.Prereq = formula

        globalHolder.append(featName)
        for entry in globalHolder:
            if entry in cell:
                if "SPECIAL" in thisFeat.Prereq:
                    thisFeat.Prereq = entry
                else:
                    thisFeat.Prereq = "=AND("+thisFeat.Prereq + ", " + entry + ")"
        db += thisFeat.toString() + ',\n'

with open("results/feats-pre.json", "w", encoding="utf-8") as outfile:
    db = db[:-2] + "]"
    db = db.replace("ñ", "\'")
    db = db.replace("–", "-")
    db = db.replace("’", "\'")
    db = db.replace("“", "\'")
    db = db.replace("”", "\'")
    outfile.write(db )