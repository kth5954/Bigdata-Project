import pandas as pd

#  연도별 감독,배우 리스트 만들고 하나의 column으로 합치기

mov_13 = pd.read_csv("asset/new/yearly/mov_13.csv")
mov_14 = pd.read_csv("asset/new/yearly/mov_14.csv")
mov_15 = pd.read_csv("asset/new/yearly/mov_15.csv")
mov_16 = pd.read_csv("asset/new/yearly/mov_16.csv")
mov_17 = pd.read_csv("asset/new/yearly/mov_17.csv")
mov_18 = pd.read_csv("asset/new/yearly/mov_18.csv")
mov_19 = pd.read_csv("asset/new/yearly/mov_19.csv")

movList = [mov_19,mov_18,mov_17,mov_16,mov_15,mov_14,mov_13]
dirList = []
actorList = []

for i in movList:
    for j in list(i.columns):
        if j[:3] == "dir":
            dirList.append(pd.Series(i[j]))

for i in movList:
    for j in list(i.columns):
        if j[:3] == "act":
            actorList.append(pd.Series(i[j]))
actor_list = pd.DataFrame(set(pd.concat(actorList, ignore_index=True)))
direcror_list = pd.DataFrame(set(pd.concat(dirList, ignore_index=True)))

actor_list.to_csv("asset/new/actors.csv")
direcror_list.to_csv("asset/new/directors.csv")

