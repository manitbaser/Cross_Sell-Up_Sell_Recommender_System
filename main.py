from main_cross_sell import *
from main_up_sell import *
from filter import *
from quantity import *
def main_recommend(user_id, user_product, user_qty):

	recc1, recc2 = cross_sell(user_id, user_product)
	recc3 = up_sell(user_id, user_product)

	common1, new1 = filter(user_id, recc1)
	common2, new2 = filter(user_id, recc2)
	common3, new3 = filter(user_id, recc3)

	common1 = [(common_qty(user_id, i),i) for i in common1]
	common2 = [(common_qty(user_id, i),i) for i in common2]
	common3 = [(user_qty, i) for i in common3]
	new3 = [(user_qty, i) for i in new3]


	return [new1, new2, new3, common1, common2, common3]
