# Measures of Reading Ease and NOVA Food Processing Classification on Ingredients Lists in the United States 
This is the GitHub README page for the above titled project submitted to [tbd].

### Data Download and Preprocess

Set up a file directory
```
mkdir nova_x_off
cd nova_x_off/
```

Grab the data from Open Food Facts; our download was performed on June 30, 2022 and downloaded file size before unzip was ~69.5 MB.
```
wget https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz
gunzip en.openfoodfacts.org.products.csv.gz 
```

We are interested in products in the USA only so check to see how USA is labeled
```
cut -f 38  en.openfoodfacts.org.products.csv | sort | uniq
cut -f 38  en.openfoodfacts.org.products.csv | sort | uniq | grep "United States"
head -n 1 en.openfoodfacts.org.products.csv > en.openfoodfacts.org.products.USonly.csv
grep "United States" en.openfoodfacts.org.products.csv >> en.openfoodfacts.org.products.USonly.csv
```

### Data Download and Preprocess

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
tmpdf['readability_lix'] = tmpdf.apply(get_readability_score(tmpdf["ingredients_text"],"LIX"))

```

working script
```
import pandas as pd
import readability
from nltk.tokenize import word_tokenize
import sys
import numpy as np
import matplotlib.pyplot as plt

def get_readability_score(ingredients,measure):
  return_value = -500
  if(ingredients):
    tokenized = word_tokenize(str(ingredients))
    ingredients = tokenized
    read = readability.getmeasures(ingredients,lang='en')
    return_value = round(read['readability grades'][measure],2)
  return return_value

df = pd.read_csv("en.openfoodfacts.org.products.USonly.csv",sep="\t",encoding="utf-8-sig")
tmpdf = df[["product_name","nova_group","ingredients_text","code","countries_tags"]]
tmpdf = tmpdf.dropna(subset=["product_name","nova_group","ingredients_text","code","countries_tags"])
tmpdf = tmpdf[~tmpdf.countries_tags.isin(['en:united-states'])]
tmpdf['readability_lix'] = tmpdf["ingredients_text"].apply(get_readability_score,args=("ARI",))

nova1=tmpdf.loc[tmpdf['nova_group'] == 1.0]
nova2=tmpdf.loc[tmpdf['nova_group'] == 2.0]
nova3=tmpdf.loc[tmpdf['nova_group'] == 3.0]
nova4=tmpdf.loc[tmpdf['nova_group'] == 4.0]
data = [nova1['readability_lix'],nova2['readability_lix'],nova3['readability_lix'],nova4['readability_lix']]
fig7, ax7 = plt.subplots()
ax7.set_title('Multiple Samples with Different sizes')
ax7.boxplot(data)
plt.show()
```

## License
The Python code shared on this page is available for use under the MIT License. 
Please ensure when using data from Open Food Facts or other Python libraries that you are aware that their licenses may differ.

## Contact
If you have questions or concerns please contact Kate Cooper at kmcooper [at] unomaha [d0t] edu.
