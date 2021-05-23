import pandas as pd
import numpy as np

data = pd.read_excel('./Data.xlsx')

initial_size = len(data)
# data = data[pd.notnull(data['Longitude'])]
data['Longitude'] = data['Longitude'].fillna('nan')
data['Latitude'] = data['Latitude'].fillna('nan')
final_size = len(data)

wholesalers = list(set(data['Ship-to nu']))
wholesalers_products = {i:list(set(data[data['Ship-to nu'] == i]['Material'])) for i in wholesalers}
products = list(set(data['Material']))
wholesalers_info = [{'id':i, 
					 'location':(data.loc[data['Ship-to nu'] == i,'Latitude'].iloc[0], data.loc[data['Ship-to nu'] == i, 'Longitude'].iloc[0]), 
					 'products': list(set(data[data['Ship-to nu'] == i]['Material'])), 
					 'groupement':list(data[data['Ship-to nu'] == i]['Groupement'])[0], 
					 'subgroupement': list(data[data['Ship-to nu'] == i]['Sous groupement'])[0]} for i in wholesalers]
(pd.DataFrame(wholesalers_info).set_index('id')).to_csv("./wholesalers_info.csv")

df_wholesalers_products = pd.DataFrame(columns = ['id']+products)
for i in wholesalers:
  wholesaler_products_row = dict.fromkeys(['id']+products, 0)
  wholesaler_products_row['id'] = i
  for j in wholesalers_products[i]:
    wholesaler_products_row[j] = 1
  df_wholesalers_products = df_wholesalers_products.append(wholesaler_products_row, ignore_index = True)
df_wholesalers_products.set_index('id').to_csv("./wholesalers_products.csv")

