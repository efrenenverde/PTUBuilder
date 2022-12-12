# Import the xlrd module
import xlrd, uuid

# Open the Workbook
workbook = xlrd.open_workbook("DATA SHEET.xls")

# Open the worksheet
worksheet = workbook.sheet_by_name("Features Data")

db = "["

# Iterate the rows and columns
for i in range(0, worksheet.nrows):
    if worksheet.cell_value(i, 0) != "" and worksheet.cell_value(i, 0) != "Name":
        dict = {
            "_id": str(uuid.uuid4().fields[-1])[:16],
            "name": worksheet.cell_value(i, 0).replace("\'", "ñ"),
            "tags": worksheet.cell_value(i, 1).replace("\'", "ñ"),
            "prerequisites": worksheet.cell_value(i, 2).replace("\'", "ñ"),
            "frequency": worksheet.cell_value(i, 3).replace("\'", "ñ"),
            "effect": worksheet.cell_value(i, 4).replace("\'", "ñ")
        }
        db = db + str(dict) + ",\n"

db = db.replace("\"", "ñ")
db = db.replace("\'", "\"")
db = db.replace("ñ", "\'")
db = db.replace("\xa01", " ")

db = db[:-1]
with open("results/feats.json", "w", encoding="utf-8") as outfile:
    outfile.write(db)