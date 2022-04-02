from func import *
import pandas as pd
import numpy as np

movie_13 = pd.read_csv('asset/movie_13.csv')
movie_14 = pd.read_csv('asset/movie_14.csv')

movie_13.drop(["rank"], axis=1, inplace=True)
movie_14.drop(["rank"], axis=1, inplace=True)

sample1 = movie_13
sample2 = movie_14

a = list(sample1['name'])
directors = []
actors = []
crawl_names(a, directors, actors)
directors = dataFrameMaker(directors, "director")
actors = dataFrameMaker(actors, "actor")
s = sample1.join(directors, how='left')
s = s.join(actors, how='left')
s.to_csv("asset/new/mov_13.csv")

a = list(sample2['name'])
directors = []
actors = []
crawl_names(a, directors, actors)
directors = dataFrameMaker(directors, "director")
actors = dataFrameMaker(actors, "actor")
s = sample1.join(directors, how='left')
s = s.join(actors, how='left')
s.to_csv("asset/new/mov_14.csv")