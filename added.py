# 추가된 값 합치기

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
from func import *

mov_all = pd.read_csv("asset//new/mov_all.csv")
mov_add = pd.read_csv("asset/new/mov_add.csv")
actor_rna = pd.read_csv("asset/casts/actor_rna.csv")
director_rna = pd.read_csv("asset/casts/director_rna.csv")

old_actors = list(actor_rna['name'])
old_directors = list(director_rna['name'])

a_a = []; a_b = []
d_a = []; d_b = []

for i in range(22):
    a_a.append(list(mov_add['actor%d' % (i+1)]))
    for j in range(len(a_a[i])):
        a_b.append(a_a[i][j])

for i in range(9):
    d_a.append(list(mov_add['director%d' % (i+1)]))
    for j in range(len(d_a[i])):
        d_b.append(d_a[i][j])

a_c = pd.DataFrame(list(set(a_b)), columns=["name"])
d_c = pd.DataFrame(list(set(d_b)), columns =['name'])

new_actors = list(a_c['name'])
new_directors = list(d_c['name'])
actors = list(set(new_actors + old_actors))
directors = list(set(new_directors + old_directors))

actors_df = pd.DataFrame(actors, columns=['name'])
actors_df = actors_df.drop([actors_df.index[0]])
directors_df = pd.DataFrame(directors, columns=['name'])
directors_df = directors_df.drop([directors_df.index[0]])
actors_df.to_csv("asset/new/actors_merged.csv")
directors_df.to_csv("asset/new/directors_merged.csv")