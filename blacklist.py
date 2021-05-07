import pandas as pd
from ast import literal_eval


def blacklist_product_product(product_id1, product_id2):
	blacklisted_df = pd.read_csv("./blacklisted_product_product.csv", index_col=0)
	blacklisted_df[['blacklisted']] = blacklisted_df[['blacklisted']].applymap(literal_eval)
	blacklisted_df.loc[blacklisted_df['product id'] == product_id1, 'blacklisted'].values[0].append(product_id2)
	blacklisted_df.to_csv("./blacklisted_product_product.csv")

def blacklist_customer_product(wholesaler_id, product_id):
	blacklisted_df = pd.read_csv("./blacklisted_customer_product.csv", index_col=0)
	blacklisted_df[['blacklisted']] = blacklisted_df[['blacklisted']].applymap(literal_eval)
	blacklisted_df.loc[blacklisted_df['wholesaler id'] == wholesaler_id, 'blacklisted'].values[0].append(product_id)
	blacklisted_df.to_csv("./blacklisted_wholesaler_product.csv")
