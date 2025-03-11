import pandas as pd
data = ['1','2']

datas = [pd.to_numeric(x) for x in data]
print(datas)
# #1번째 실행
# '1' -> 1
# '2' -> 2
# 'A' -> error