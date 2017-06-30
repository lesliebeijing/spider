import json

f = open('/Users/leslie/leslie/HelloScrapy/css.json')
data = json.load(f)

d1 = sorted(data, key=lambda x: x['score'], reverse=True)

for item in d1:
    print(item)
