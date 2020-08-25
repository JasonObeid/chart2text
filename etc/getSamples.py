import json
import pandas as pd
import os
from sklearn import utils
import csv
import weasyprint as wsp
import PIL as pil
import matplotlib.pyplot as plt

def trim(source_filepath, target_filepath=None, background=None):
    if not target_filepath:
        target_filepath = source_filepath
    img = pil.Image.open(source_filepath)
    if background is None:
        background = img.getpixel((0, 0))
    border = pil.Image.new(img.mode, img.size, background)
    diff = pil.ImageChops.difference(img, border)
    bbox = diff.getbbox()
    img = img.crop(bbox) if bbox else img
    img.save(target_filepath)

nlpPath = os.listdir('../results/aug17/generated')
basePath = os.listdir('../results/aug17/generated_baseline')
untemplatedPath = os.listdir('../results/aug17/generated_untemplated')

nlpPath.sort()
basePath.sort()
untemplatedPath.sort()

twoBarList, multiBarList, twoLineList, multiLineList = [], [], [], []

nlpList, baseList, untemplatedList = [], [], []

for nlpFile in nlpPath:
    with open('../results/aug17/generated/'+nlpFile) as file:
        document = json.loads(file.read())
        if document['columnType'] == 'two':
            if document['graphType'] == 'bar':
                twoBarList.append(nlpFile)
            else:
                twoLineList.append(nlpFile)
        else:
            if document['graphType'] == 'bar':
                multiBarList.append(nlpFile)
            else:
                multiLineList.append(nlpFile)

twoBarListShuffled = utils.shuffle(
    twoBarList, random_state=0)

multiBarListShuffled = utils.shuffle(
    multiBarList, random_state=0)

twoLineListShuffled = utils.shuffle(
    twoLineList, random_state=0)

multiLineListShuffled = utils.shuffle(
    multiLineList, random_state=0)

csvPath = "../results/aug17/samples.csv"
with open(csvPath, mode='a', newline='') as csvFile:
    csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
    csvWriter.writerow(["imgPath", "generated", "generated_baseline", "generated_untemplated", "gold", "titles"])
    # multiBar, twoLine, multiLine  , multiBarListShuffled[:25], twoLineListShuffled[:25], multiLineListShuffled[:25])
    for twoBar in twoBarListShuffled[:25]:
        with open('../results/aug17/generated/' + twoBar) as file1:
            document1 = json.loads(file1.read())
            generated = ''.join(document1['summary']).strip().replace('_','')
            gold = document1['gold'].strip()
            title = document1['title'].strip()
            webPath = 'https://chart2text.s3.amazonaws.com/' + twoBar[:-5] + '.png'
            imgPath = '../results/aug17/samples/' + twoBar[:-5] + '.png'
            df = pd.DataFrame(document1['data'])
            dico = {label: 'float32' for label in df.columns[1:]}
            try:
                df = df.astype(dico)
            except Exception as e:
                print(e)
                for n in df.columns[1:]:
                    for m in df.index:
                        value = df.at[m, n]
                        df.at[m, n] = float(''.join(ch for ch in str(value) if ch.isdigit() or ch == '.'))
            df.set_index(df.columns[0], drop=True, inplace=True)
            ax = df.plot.bar()
            ax.set_ylabel(document1['yAxis'])
            plt.savefig(imgPath, bbox_inches="tight")
            plt.close()
        with open('../results/aug17/generated_baseline/' + twoBar) as file2:
            document2 = json.loads(file2.read())
            generated_baseline = ''.join(document2['summary']).strip().replace('_','')
        with open('../results/aug17/generated_untemplated/' + twoBar) as file3:
            document3 = json.loads(file3.read())
            generated_untemplated = ''.join(document3['summary']).strip().replace('_','')
        csvWriter.writerow([webPath, generated, generated_baseline, generated_untemplated, gold, title])

    for twoLine in twoLineListShuffled[:25]:
        with open('../results/aug17/generated/' + twoLine) as file1:
            document1 = json.loads(file1.read())
            generated = ''.join(document1['summary']).strip().replace('_','')
            gold = document1['gold'].strip()
            title = document1['title'].strip()

            webPath = 'https://chart2text.s3.amazonaws.com/' + twoLine[:-5] + '.png'
            imgPath = '../results/aug17/samples/' + twoLine[:-5] + '.png'
            df = pd.DataFrame(document1['data'])
            dico = {label: 'float32' for label in df.columns[1:]}
            try:
                df = df.astype(dico)
            except Exception as e:
                print(e)
                for n in df.columns[1:]:
                    for m in df.index:
                        value = df.at[m, n]
                        df.at[m, n] = float(''.join(ch for ch in str(value) if ch.isdigit() or ch == '.'))
            df.set_index(df.columns[0], drop=True, inplace=True)
            ax = df.plot.line()
            ax.set_ylabel(document1['yAxis'])
            plt.savefig(imgPath, bbox_inches="tight")
            plt.close()
        with open('../results/aug17/generated_baseline/' + twoLine) as file2:
            document2 = json.loads(file2.read())
            generated_baseline = ''.join(document2['summary']).strip().replace('_','')
        with open('../results/aug17/generated_untemplated/' + twoLine) as file3:
            document3 = json.loads(file3.read())
            generated_untemplated = ''.join(document3['summary']).strip().replace('_','')
        csvWriter.writerow([webPath, generated, generated_baseline, generated_untemplated, gold, title])

    for multiBar in multiBarListShuffled[:25]:
        with open('../results/aug17/generated/' + multiBar) as file1:
            document1 = json.loads(file1.read())
            generated = ''.join(document1['summary']).strip()
            gold = document1['gold'].strip()
            title = document1['title'].strip()

            webPath = 'https://chart2text.s3.amazonaws.com/' + multiBar[:-5] + '.png'
            imgPath = '../results/aug17/samples/' + multiBar[:-5] + '.png'
            df = pd.DataFrame(document1['data'])
            dico = {label: 'float32' for label in df.columns[1:]}
            try:
                df = df.astype(dico)
            except Exception as e:
                print(e)
                for n in df.columns[1:]:
                    for m in df.index:
                        value = df.at[m, n]
                        df.at[m, n] = float(''.join(ch for ch in str(value) if ch.isdigit() or ch == '.'))
            df.set_index(df.columns[0], drop=True, inplace=True)
            ax = df.plot.bar()
            plt.savefig(imgPath, bbox_inches="tight")
            plt.close()
        with open('../results/aug17/generated_baseline/' + multiBar) as file2:
            document2 = json.loads(file2.read())
            generated_baseline = ''.join(document2['summary']).strip().replace('_','')
        with open('../results/aug17/generated_untemplated/' + multiBar) as file3:
            document3 = json.loads(file3.read())
            generated_untemplated = ''.join(document3['summary']).strip().replace('_','')
        csvWriter.writerow([webPath, generated, generated_baseline, generated_untemplated, gold, title])

    for multiLine in multiLineListShuffled[:25]:
        with open('../results/aug17/generated/' + multiLine) as file1:
            document1 = json.loads(file1.read())
            generated = ''.join(document1['summary']).strip().replace('_','')
            gold = document1['gold'].strip()
            title = document1['title'].strip()

            webPath = 'https://chart2text.s3.amazonaws.com/' + multiLine[:-5] + '.png'
            imgPath = '../results/aug17/samples/' + multiLine[:-5] + '.png'
            df = pd.DataFrame(document1['data'])
            dico = {label: 'float32' for label in df.columns[1:]}
            try:
                df = df.astype(dico)
            except Exception as e:
                print(e)
                for n in df.columns[1:]:
                    for m in df.index:
                        value = df.at[m, n]
                        df.at[m, n] = float(''.join(ch for ch in str(value) if ch.isdigit() or ch == '.'))
            ax = df.plot.line()
            plt.savefig(imgPath, bbox_inches="tight")
            plt.close()
        with open('../results/aug17/generated_baseline/' + multiLine) as file2:
            document2 = json.loads(file2.read())
            generated_baseline = ''.join(document2['summary']).strip().replace('_','')
        with open('../results/aug17/generated_untemplated/' + multiLine) as file3:
            document3 = json.loads(file3.read())
            generated_untemplated = ''.join(document3['summary']).strip().replace('_','')
        csvWriter.writerow([webPath, generated, generated_baseline, generated_untemplated, gold, title])