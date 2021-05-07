import pandas as pd
import math
import numpy as np
from ast import literal_eval

df_products = pd.read_csv("./products_info.csv", index_col="id")
products = list(df_products.index)
product_vectors = df_products.copy().to_numpy()

def similarity(vector1, vector2):
  return np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))

def find_top_ids(user_id, user_product):
  products = list(df_products.index)
  product_vectors = df_products.copy().to_numpy()

  df = pd.read_csv("./blacklisted_product_product.csv", index_col=0)
  df[['blacklisted']] = df[['blacklisted']].applymap(literal_eval)
  blacklist_product_product_list = df.loc[df['product id'] == user_product, 'blacklisted'].values[0]

  df = pd.read_csv("./blacklisted_wholesaler_product.csv", index_col=0)
  df[['blacklisted']] = df[['blacklisted']].applymap(literal_eval)
  blacklist_wholesaler_product_list = df.loc[df['wholesaler id'] == user_id, 'blacklisted'].values[0]

  indices_to_remove = [i for i in range(len(products)) if products[i] in blacklist_product_product_list+blacklist_wholesaler_product_list]
  products = [products[i] for i in range(len(products)) if i not in indices_to_remove]
  product_vectors = [product_vectors[i] for i in range(len(product_vectors)) if i not in indices_to_remove]

  product_index = products.index(user_product)
  product_vector = product_vectors[product_index]
  product_similarity_list = [similarity(product_vector, vector) for vector in product_vectors]
  product_similarity_list[product_index] = 0.0
  similar_product_index = list(np.argsort(product_similarity_list)[-3:][::-1])
  product_similar_user_id = [products[i] for i in similar_product_index]

  return product_similar_user_id

def up_sell(user_id, user_product):
  if(not user_product in products):
    return["Product not in database."]
  else:
    return(find_top_ids(user_id, user_product))