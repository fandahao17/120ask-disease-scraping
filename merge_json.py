import glob
import json

chars = 'abcdefg'

for ch in chars:
    print(ch)
    jsons = []
    for f in glob.glob('{}/*.json'.format(ch)):
        file = open(f)
        jsons.append(json.load(file))

    json.dump(jsons, open('{}.json'.format(ch), 'w'), ensure_ascii=False, indent=4)
