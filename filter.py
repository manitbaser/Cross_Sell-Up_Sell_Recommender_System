import pandas as pd
import numpy as np
from ast import literal_eval

wholesalers_info = pd.read_csv("./wholesalers_info.csv", index_col="id")
wholesalers_info[['products']] = wholesalers_info[['products']].applymap(literal_eval)
def filter(user_id, recc):
	common = []
	new = []
	if set(recc).intersection(wholesalers_info['products'][user_id]):
		common = list(set(recc).intersection(wholesalers_info['products'][user_id])) 
		new = [item for item in recc if item not in common]
	else: 
		new = recc
	return common, new
