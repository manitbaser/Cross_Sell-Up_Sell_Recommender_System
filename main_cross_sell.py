import pandas as pd
import numpy as np
from collections import Counter
from scipy.spatial import distance
from ast import literal_eval


df_wholesalers_products = pd.read_csv("./wholesalers_products.csv", index_col="id")
df_wholesalers_products[list(df_wholesalers_products.columns)] = df_wholesalers_products[list(df_wholesalers_products.columns)].astype(int)
wholesalers = list(df_wholesalers_products.index)
product_vectors = df_wholesalers_products.copy().to_numpy()

wholesalers_info = pd.read_csv("./wholesalers_info.csv", index_col="id")
wholesalers_info[['location', 'products']] = wholesalers_info[['location', 'products']].applymap(literal_eval)

def similarity(vector1, vector2):
  return np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))

def nearest_wholesalers(user_id):
  if wholesalers_info['location'][user_id] == ('nan', 'nan'):
    return []
  dist = {i:distance.euclidean(wholesalers_info['location'][user_id], wholesalers_info['location'][i]) for i in wholesalers_info.index if wholesalers_info['location'][i]!=('nan', 'nan')}
  dist.pop(user_id)
  nearest_ids = list(sorted(dist.items(), key = lambda kv:(kv[1], kv[0])))[:20]
  return nearest_ids

def groupements_sort(user_id, nearest_ids):
  matching_both = []
  matching_groupements = []
  matching_sub_groupements = []
  no_match = []
  for i,j in nearest_ids:
    groupement_bool = wholesalers_info['groupement'][user_id] == wholesalers_info['groupement'][i]
    sub_groupement_bool = wholesalers_info['subgroupement'][user_id] == wholesalers_info['subgroupement'][i]
    if (groupement_bool and sub_groupement_bool):
      matching_both.append((i,j))
    elif (groupement_bool and not sub_groupement_bool):
      matching_groupements.append((i,j))
    elif (not groupement_bool and sub_groupement_bool):
      matching_sub_groupements.append((i,j))
    else:
      no_match.append((i,j))
  combined = matching_both + matching_groupements + matching_sub_groupements + no_match
  return [i for i,j in combined[:10]]

def find_top_ids(user_id):
  user_index = wholesalers.index(user_id)

  user_product_vector = product_vectors[user_index]
  product_similarity_list = [similarity(user_product_vector, vector) for vector in product_vectors]
  product_similarity_list[user_index] = 0.0
  product_similar_user_index = list(np.argsort(product_similarity_list)[-20:][::-1])
  product_similar_user_id = [wholesalers[i] for i in product_similar_user_index]

  location_pricing_similar_user_id = groupements_sort(user_id, nearest_wholesalers(user_id))

  return product_similar_user_id, location_pricing_similar_user_id

def recommend(user_id, user_product, product_similar_user_id, location_pricing_similar_user_id):
  df = pd.read_csv("./blacklisted_product_product.csv", index_col=0)
  df[['blacklisted']] = df[['blacklisted']].applymap(literal_eval)
  blacklist_product_product_list = df.loc[df['product id'] == user_product, 'blacklisted'].values[0]

  df = pd.read_csv("./blacklisted_wholesaler_product.csv", index_col=0)
  df[['blacklisted']] = df[['blacklisted']].applymap(literal_eval)
  blacklist_wholesaler_product_list = df.loc[df['wholesaler id'] == user_id, 'blacklisted'].values[0]

  arr1 = []
  for id in product_similar_user_id:
    arr1 = arr1 + wholesalers_info['products'][id]
  arr1 = [i for i in arr1 if i not in blacklist_wholesaler_product_list+blacklist_product_product_list]
  arr1 = [i for i in arr1 if i != user_product]
  rec1 = [i for i,j in Counter(arr1).most_common(3)]

  arr2 = []
  for id in location_pricing_similar_user_id:
    arr2 = arr2 + wholesalers_info['products'][id]
  arr2 = [i for i in arr2 if i not in blacklist_wholesaler_product_list+blacklist_product_product_list]
  arr2 = [i for i in arr2 if i != user_product]
  rec2 = [i for i,j in Counter(arr2).most_common(3)]
  return rec1, rec2

def cross_sell(user_id, user_product):
  if(not user_id in wholesalers):
    return["User not in database."]
  else:
    product_similar_user_id, location_pricing_similar_user_id = find_top_ids(user_id)
    return recommend(user_id, user_product, product_similar_user_id, location_pricing_similar_user_id)
