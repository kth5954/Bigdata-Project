from func import *
import pandas as pd

# Read all movie csv file
mov_13 = pd.read_csv("asset/new/yearly/mov_13.csv")
mov_14 = pd.read_csv("asset/new/yearly/mov_14.csv")
mov_15 = pd.read_csv("asset/new/yearly/mov_15.csv")
mov_16 = pd.read_csv("asset/new/yearly/mov_16.csv")
mov_17 = pd.read_csv("asset/new/yearly/mov_17.csv")
mov_18 = pd.read_csv("asset/new/yearly/mov_18.csv")
mov_19 = pd.read_csv("asset/new/yearly/mov_19.csv")

# Dataframe List
movList = [mov_19, mov_18, mov_17, mov_16, mov_15, mov_14, mov_13]

# concatenate the all movie csv file
mov_list = pd.concat(movList, ignore_index=True)
mov_list = mov_list.drop('idx', axis=1)
mov_list.to_csv("asset/new/mov_all.csv")


directors = pd.read_csv("asset/casts/directors.csv")
actors = pd.read_csv("asset/casts/actors.csv")
#
directors = directors.drop('idx', axis=1)
actors = actors.drop('idx', axis=1)
#
# directors.to_csv("asset/new/directors.csv", index=False)
# actors.to_csv("asset/new/actors.csv", index=False)



directors.to_csv("asset/new/directors.csv", index=False)
actors.to_csv("asset/new/actors.csv", index=False)

