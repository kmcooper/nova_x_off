# Measures of Reading Ease and NOVA Food Processing Classification on Ingredients Lists in the United States 
This is the GitHub README page for the above titled project submitted to [tbd].

### Data Download and Do a little Preprocessing

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

### Import Libraries
```
import pandas as pd
import readability
from nltk.tokenize import word_tokenize
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statannot import add_stat_annotation
```

### Analyze Ingredients by NOVA x Group 
The code below generates Figure 1a, 1b, and Figure 2 from the manuscript.
Define what submeasure to grab from the `readability` library and define it as `submeasure`, then grab the score for that submeasure for all ingredients lists in all products in the dataset:
```
submeasure="syll_per_word"
def get_complexity_score(ingredients,measure):
  return_value = -500
  if(ingredients):
    tokenized = word_tokenize(str(ingredients))
    ingredients = tokenized
    read = readability.getmeasures(ingredients,lang='en')
    return_value = round(read['sentence info'][measure],2)
  return return_value

## Read in the CSV file with US only products
## Grab only relevant columns to reduce space
## Drop rows with empty values needed for analysis
## Drop rows that aren't listed as sold in the United States
## Then get the complexity score of the desired submeasure
df = pd.read_csv("en.openfoodfacts.org.products.USonly.csv",sep="\t",encoding="utf-8-sig")
tmpdf = df[["product_name","nova_group","ingredients_text","code","countries_tags"]]
tmpdf = tmpdf.dropna(subset=["product_name","nova_group","ingredients_text","code","countries_tags"])
tmpdf = tmpdf[tmpdf.countries_tags.isin(['en:united-states'])]
tmpdf['complexity'] = tmpdf["ingredients_text"].apply(get_complexity_score,args=(submeasure,))

## Group the temporary dataframe by NOVA groups
nova1=tmpdf.loc[tmpdf['nova_group'] == 1.0]
nova2=tmpdf.loc[tmpdf['nova_group'] == 2.0]
nova3=tmpdf.loc[tmpdf['nova_group'] == 3.0]
nova4=tmpdf.loc[tmpdf['nova_group'] == 4.0]

##########################
#
# The code below generates
# Figure 1a
#
##########################
#nova2['complexity'],nova3['complexity'],nova4['complexity'])),columns =['NOVA 1', 'NOVA 2','NOVA 3', 'NOVA 4'])
x="nova_group"
y="complexity"
tmpdf['nova_group'].replace(1.0,"1",inplace=True)
tmpdf['nova_group'].replace(2.0,"2",inplace=True)
tmpdf['nova_group'].replace(3.0,"3",inplace=True)
tmpdf['nova_group'].replace(4.0,"4",inplace=True)
order=['1','2','3','4']
ax = sns.boxplot(data=tmpdf, x=x, y=y, order=order,showfliers=True)
ax.set_xlabel("NOVA Group")
ax.set_ylabel(submeasure)
test_results = add_stat_annotation(ax, data=tmpdf, x=x, y=y, order=order,
                                   box_pairs=[("1", "2"), ("2", "3"), ("3", "4"),("1","4")],
                                   test='Mann-Whitney', text_format='star',
                                   loc='inside', verbose=2)
for res in test_results:
    print(res)
plt.show()

##########################
#
# The code below generates
# Figure 1b
#
##########################
ax = sns.violinplot(data=tmpdf,x=x,y=y,order=order)
ax.set_xlabel("NOVA Group")
ax.set_ylabel(submeasure)
plt.show()

##########################
#
# The code below generates
# Figure 2
#
##########################
submeasure="complex_words"
tmpdf['complexity'] = tmpdf["ingredients_text"].apply(get_complexity_score,args=(submeasure,))
#nova2['complexity'],nova3['complexity'],nova4['complexity'])),columns =['NOVA 1', 'NOVA 2','NOVA 3', 'NOVA 4'])
x="nova_group"
y="complexity"
tmpdf['nova_group'].replace(1.0,"1",inplace=True)
tmpdf['nova_group'].replace(2.0,"2",inplace=True)
tmpdf['nova_group'].replace(3.0,"3",inplace=True)
tmpdf['nova_group'].replace(4.0,"4",inplace=True)
order=['1','2','3','4']
ax = sns.boxplot(data=tmpdf, x=x, y=y, order=order,showfliers=True)
ax.set_xlabel("NOVA Group")
ax.set_ylabel(submeasure)
test_results = add_stat_annotation(ax, data=tmpdf, x=x, y=y, order=order,
                                   box_pairs=[("1", "2"), ("2", "3"), ("3", "4"),("1","4")],
                                   test='Mann-Whitney', text_format='star',
                                   loc='inside', verbose=2)
for res in test_results:
    print(res)
plt.show()
```

### Table 1 Measures
Gather mean, median, minimum, maximum from all 4 NOVA groups, then perform one-way ANOVA with post hoc Tukey test to identify where differences are.
```
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

## One way ANOVA with Tukey post hoc
fvalue, pvalue = stats.f_oneway(nova1['ingredients_text'].str.len(),
                                nova2['ingredients_text'].str.len(), 
                                nova3['ingredients_text'].str.len(),
                                nova4['ingredients_text'].str.len())
print("F-stat=",fvalue)
print("P-value=",pvalue)

post_hoc_tukey=pairwise_tukeyhsd(endog=tmpdf['ingredients_text'].str.len(),groups=tmpdf['nova_group'],alpha=0.05)
post_hoc_tukey=pairwise_tukeyhsd(tmpdf['ingredients_text'].str.len(),groups=tmpdf['nova_group'],alpha=0.05)
print(post_hoc_tukey)
```
### Table 2 Measures
Count how many rows per NOVA group contain the substring "organic", then count total rows per NOVA group and calculate the percentage of ingredients texts that contain the word organic
```
nova1['ingredients_text'].str.count("organic").sum()
nova1['ingredients_text'].count().sum()
nova1['ingredients_text'].str.count("organic").sum()/nova1['ingredients_text'].count().sum()

nova2['ingredients_text'].str.count("organic").sum()
nova2['ingredients_text'].count().sum()
nova2['ingredients_text'].str.count("organic").sum()/nova2['ingredients_text'].count().sum()

nova3['ingredients_text'].str.count("organic").sum()
nova3['ingredients_text'].count().sum()
nova3['ingredients_text'].str.count("organic").sum()/nova3['ingredients_text'].count().sum()

nova4['ingredients_text'].str.count("organic").sum()
nova4['ingredients_text'].count().sum()
nova4['ingredients_text'].str.count("organic").sum()/nova4['ingredients_text'].count().sum()
```

## License
The Python code shared on this page is available for use under the MIT License. 
Please ensure when using data from Open Food Facts or other Python libraries that you are aware that their licenses may differ.

## Contact
If you have questions or concerns please contact Kate Cooper at kmcooper [at] unomaha [d0t] edu.
