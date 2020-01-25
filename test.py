from functions import *


a = [['#'] * 5 for i in range(5)]
m = arrow((0, 0), (4, 4))
for x, y in m:
    a[x][y] = '%'
for i in range(5):
    for j in range(5):
        print(a[4 - i][j], end=' ')
    print()