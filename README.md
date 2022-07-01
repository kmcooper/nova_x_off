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
```
