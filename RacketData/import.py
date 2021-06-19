# Import racket data csv

import pandas as pd

df = pd.read_csv("./wilson_data.csv",index_col=0)

print(df.loc["Wilson Clash 100L Racket"])

