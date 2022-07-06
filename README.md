```
mkdir nova_x_off
cd nova_x_off/
wget https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz
# CSV downloaded on June 30, 2022
# File size ~69.5MB
gunzip en.openfoodfacts.org.products.csv.gz 
# We are interested in the USA only so check to see how USA is labeled
cut -f 38  en.openfoodfacts.org.products.csv | sort | uniq
cut -f 38  en.openfoodfacts.org.products.csv | sort | uniq | grep "United States"
head -n 1 en.openfoodfacts.org.products.csv > en.openfoodfacts.org.products.USonly.csv
grep "United States" en.openfoodfacts.org.products.csv >> en.openfoodfacts.org.products.USonly.csv
```

python extract 
```
# Options for readability measures are
# Kincaid
# ARI
# Coleman-Liau
# FleshReadingEase
# GunningFogIndex
# LIX
# SMOGIndex
# RIX
# DaleChallIndex

import pandas as pd
import readability
from nltk.tokenize import word_tokenize
import sys
measure_type="LIX"
ingredients_list = "taco, burrito, fritos"
def get_readability_score(ingredients,measure):
  tokenized = word_tokenize(ingredients)
	ingredients = tokenized
	read = readability.getmeasures(ingredients,lang='en')
  return round(read['readability grades'][measure],2)
```
script
```

df = pd.read_csv("en.openfoodfacts.org.products.USonly.csv",sep="\t")
tmpdf = df[["product_name","nova_group","ingredients_text","code","countries_tags"]]
tmpdf = tmpdf.dropna(subset=["product_name","nova_group","ingredients_text","code","countries_tags"])
tmpdf = tmpdf[~tmpdf.countries_tags.isin(['en:united-states'])]
```
