import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import numpy as np
df = pd.read_excel('./Data.xlsx')

def common_qty(user_id, product_id):
	user_history= df.loc[df['Ship-to nu'] == user_id]
	matching_df = user_history.loc[user_history['Material'] == product_id]
	qty_history = list(matching_df['HL delivered'])
	index = range(len(qty_history))
	qty_data = pd.Series(qty_history, index)
	if(qty_data.shape[0]<3):
		qty = np.mean(qty_history)
	else:
		fit = SimpleExpSmoothing(qty_data).fit()
		qty = float(fit.forecast(1))
	if qty>0.0:
		return round(qty, 2)
	else:
		return float('NaN')

