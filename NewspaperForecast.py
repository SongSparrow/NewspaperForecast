import pandas as pd
import matplotlib.pyplot as plt

m = 0.3
n = 0.3
k = 0.4

M = 100
N = 100
K = 100

train_set = pd.read_csv("raw_news_data.csv")


def train():
    train_set_title = train_set["title"]
    train_set_writer = train_set["writer"]
    train_set_date = train_set["date"]
    train_set_tags = train_set["tags"]
