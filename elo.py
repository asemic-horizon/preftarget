# PREFERENCE ELO SCORE AS REGRESSION TARGET
import json, os
from glob import glob
import numpy as np
from scipy.special import ndtr #bell curve
from operator import itemgetter

def rbf(x1,x2): 
	return ndtr(x1-x2)

class PreferenceStructure:
	def __init__(self, file, path):
		self.file = file; self.path = path
		if os.path.exists(file):
			with open(file,"r") as fp:
				self.scores = json.load(fp)
		else:
			self.scores = dict()

		self.itemlist = glob(path+"/*")
		for item in self.itemlist:
			if item not in self.scores:
				self.scores[item] = 0
		self.serialize()

	def update_item(self,transfer_value,item,velocity):
		if item in self.scores:
			self.scores[item] += velocity * transfer_value
		else:
			self.scores[item] = velocity * transfer_value
	def expected(self, item_1, item_2):
		return rbf(self.scores[item_1], self.scores[item_2])
	def update(self,net_value,item_1, item_2, velocity = 1):
		expected = self.expected(item_1,item_2)
		transfer_value = net_value - expected
		self.update_item(transfer_value,item_1,velocity)
		self.update_item(-transfer_value,item_2,velocity)
		self.serialize()
	def rounded_score(self,item):
		return int(1000*self.scores[item])
	def sample_pair(self, topk=None):
		if topk:
			candidates = sorted(self.scores.items(), key = itemgetter(1), reverse = True)
			candidates = [u for u, v in candidates][:topk] #funky chicken
		else:
			candidates = self.scores.keys()
		candidates = list(candidates) 	
		return np.random.choice(candidates,2,replace=False)		
	def delete(self,item):
		os.remove(f"{self.path}/{item}")
		self.scores.pop(item)
		self.serialize()
		
	def serialize(self):
		with open(self.file, "w") as fp:
			json.dump(self.scores,fp)


