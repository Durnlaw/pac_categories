import pandas

item = []
for y in range(0,50):
    item.append(y)

for x in item:
    print(x)
    if x%5 == 0:
        print(x, 'divisble by tten')
    else:
        print('nerd')