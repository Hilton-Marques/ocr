import easyocr
from spellchecker import SpellChecker
import csv
reader = easyocr.Reader(['pt'])
result = reader.readtext('conta_03.jpg',allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVXZ.%-/ ,',width_ths = 2.0,mag_ratio=3,height_ths=2.5)
spell = SpellChecker(language='pt')

n = len(result)
names = []
codes = []
prices = [0] * 100
##find first line
for i in range(0,n):
    value = result[i]
    text = value[1]
    try:
        item = int(text[2])
    except:
        continue
    if item == 1:
        text = value[1]
        break
count = 1
for j in range(i,n):
    value = result[j]
    text = value[1]
    x = text.split()
    first = x[0]
    if (text.find(',') != -1):
        find_price = False
        for word in x:
            if (word.find(',') == -1):
                continue
            new_text = word.replace(',','.')
            try:
                price = float(new_text)
                if (price < 0):
                    continue
                prices[count - 1] = new_text
                find_price = True
                break
            except:
                continue
        if (not find_price):
            new_text = text.replace(' ','')
            new_text = new_text.replace(',','.')
            try:
                price = float(new_text)
                if (price < 0):
                    continue
                prices[count - 1] = new_text
            except:
                pass     
    if (len(x) > 3):
        try:
            if (count < 10):
                nr = int(first[-1])
            elif (count > 9 and count < 100):
                nr = int(first[-2:])
        except:
            continue
        if (nr == count):
            code = x[1]
            name = x[2]
            #names.append(spell.correction(name))
            names.append(name)
            codes.append(code)
            count += 1
        else:
            ##check if it is a code
            try:
                nr = int(first)
            except:
                continue
            if (nr > 1000):
                code = x[0]
                name = x[1]
                #names.append(spell.correction(name))
                names.append(name)
                codes.append(code)
                count += 1

    #try to find price
    # if (text.find(',') == -1):
    #     continue
    # new_text = text.replace(' ','')
    # new_text = new_text.replace(',','.')
    # try:
    #     price = float(new_text)
    # except:
    #     continue
    # prices.append(new_text)
prices  = prices[1:nr+1]

field_names = ['code', 'name', 'price']

cols = {'code':codes, 'name':names, 'price':prices}

with open('conta.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    #writer.writerows(cols)
    for row in range(max(len(value) for value in cols.values())):
        row_data = {}
        for field, values in cols.items():
            if row < len(values):
                row_data[field] = values[row]
            else:
                row_data[field] = ""
        writer.writerow(row_data)
