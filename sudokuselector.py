import pandas as pd
df = pd.read_csv("sud1.csv")

#hardQs = df[df["difficulty"] > 5]
#hardQs = hardQs.iloc[:, 1:3]

hardQs = df
hardQs["puzzle"] = hardQs["puzzle"].apply(lambda x: x.replace(".", "0")) 
print(hardQs)


hardQs.to_csv("sud1.csv", index=False)