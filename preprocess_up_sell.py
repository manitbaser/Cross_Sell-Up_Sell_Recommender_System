import pandas as pd
import numpy as np


data = pd.read_excel('./Data.xlsx')

initial_size = len(data)
data = data[pd.notnull(data['Degre Alc'])]
final_size = len(data)

data.fillna('nan', inplace=True)

products = list(set(data['Material']))
product_info = [{'id':i,
				 'degalc': int(list(data[data['Material'] == i]['Degre Alc'])[0]),
				 'brand': list(data[data['Material'] == i]['Brand'])[0],
				 'subrand': list(data[data['Material'] == i]['Subrand'])[0],
				 'segment': list(data[data['Material'] == i]['SEGMENTS : Pils / Spécialités / Superspécialités/Bouteille Young adult'])[0],
				 'segmentle': list(data[data['Material'] == i]['Segment LE'])[0],
				 'size': list(data[data['Material'] == i]['Container Size'])[0]} for i in products]

df_products_info = pd.DataFrame(product_info).set_index("id")
degalcs = list(set([int(i) for i in data['Degre Alc']]))
brands = [x for x in list(set(data['Brand'])) if x!='nan']
sub_brands = [x for x in list(set(data['Subrand'])) if x!='nan']
segments = [x for x in list(set(data['SEGMENTS : Pils / Spécialités / Superspécialités/Bouteille Young adult'])) if x!='nan']
segmentles = [x for x in list(set(data['Segment LE'])) if x!='nan']
sizes = [x for x in list(set(data['Container Size'])) if x!='nan']

df_products = pd.DataFrame(columns = ['id']+degalcs+brands+sub_brands+segments+segmentles+sizes)
for i in products:
  products_row = dict.fromkeys(['id']+degalcs+brands+sub_brands+segments+segmentles+sizes, 0)
  products_row['id'] = i
  if (df_products_info['degalc'][i] != 'nan'):
    products_row[df_products_info['degalc'][i]] = 1
  if (df_products_info['brand'][i] != 'nan'):
    products_row[df_products_info['brand'][i]] = 1
  if (df_products_info['subrand'][i] != 'nan'):
    products_row[df_products_info['subrand'][i]] = 1
  if (df_products_info['segment'][i] != 'nan'):
    products_row[df_products_info['segment'][i]] = 1
  if (df_products_info['segmentle'][i] != 'nan'):
    products_row[df_products_info['segmentle'][i]] = 1
  if (df_products_info['size'][i] != 'nan'):
    products_row[df_products_info['size'][i]] = 1
  df_products = df_products.append(products_row, ignore_index = True)


df_products.set_index('id').to_csv("./products_info.csv")