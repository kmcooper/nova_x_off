import pandas as pd
import readability
from nltk.tokenize import word_tokenize
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

submeasure="characters_per_word"

def get_complexity_score(ingredients,measure):
  return_value = -500
  if(ingredients):
    tokenized = word_tokenize(str(ingredients))
    ingredients = tokenized
    read = readability.getmeasures(ingredients,lang='en')
    return_value = round(read['sentence info'][measure],2)
  return return_value

#df = pd.read_csv("test.csv",sep="\t",encoding="utf-8-sig")
df = pd.read_csv("en.openfoodfacts.org.products.USonly.csv",sep="\t",encoding="utf-8-sig")
tmpdf = df[["product_name","nova_group","ingredients_text","code","countries_tags"]]
tmpdf = tmpdf.dropna(subset=["product_name","nova_group","ingredients_text","code","countries_tags"])
tmpdf = tmpdf[tmpdf.countries_tags.isin(['en:united-states'])]
tmpdf['complexity'] = tmpdf["ingredients_text"].apply(get_complexity_score,args=("characters_per_word",))

nova1=tmpdf.loc[tmpdf['nova_group'] == 1.0]
nova2=tmpdf.loc[tmpdf['nova_group'] == 2.0]
nova3=tmpdf.loc[tmpdf['nova_group'] == 3.0]
nova4=tmpdf.loc[tmpdf['nova_group'] == 4.0]
print("1v2:",stats.kruskal(nova1['complexity'],nova2['complexity']))
print("1v3:",stats.kruskal(nova1['complexity'],nova3['complexity']))
print("1v4:",stats.kruskal(nova1['complexity'],nova4['complexity']))
print("2v3:",stats.kruskal(nova2['complexity'],nova3['complexity']))
print("2v4:",stats.kruskal(nova2['complexity'],nova4['complexity']))
print("3v4:",stats.kruskal(nova3['complexity'],nova4['complexity']))
data = [nova1['complexity'],nova2['complexity'],nova3['complexity'],nova4['complexity']]
fig7, ax7 = plt.subplots()
ax7.set_title('Multiple Samples with Different sizes')
ax7.boxplot(data)
plt.show()

nova1['ingredients_text'].str.len().mean()
nova2['ingredients_text'].str.len().mean()
nova3['ingredients_text'].str.len().mean()
nova4['ingredients_text'].str.len().mean()

nova1['ingredients_text'].str.len().median()
nova2['ingredients_text'].str.len().median()
nova3['ingredients_text'].str.len().median()
nova4['ingredients_text'].str.len().median()

nova1['ingredients_text'].str.len().min()
nova2['ingredients_text'].str.len().min()
nova3['ingredients_text'].str.len().min()
nova4['ingredients_text'].str.len().min()

nova1['ingredients_text'].str.len().max()
nova2['ingredients_text'].str.len().max()
nova3['ingredients_text'].str.len().max()
nova4['ingredients_text'].str.len().max()



