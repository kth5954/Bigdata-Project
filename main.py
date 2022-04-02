import pandas as pd

test = pd.read_csv("asset/test set prediction.csv")

col_list = ['pred0', 'pred1', 'pred2', 'pred3', 'pred4', 'pred5', 'pred6', 'pred7']
predict = []
for i in range(len(test)):
    a = list(test.loc[i, col_list])
    max_v = a[0]
    for j in range(1, len(a)):
        if a[j] > a[j-1]:
            max_v = a[j]
    for k in range(len(a)):
        if a[k] == max_v:
            predict.append(k)

cnt = 0
for i in range(len(test)):
    if test.loc[i, 'catnum'] == predict[i]:
        cnt += 1

print("예측률: ", 100*(cnt/len(test['catnum'])), "%")
