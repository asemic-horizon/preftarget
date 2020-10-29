import streamlit as st
from glob import glob
from shutil import copyfile, move
import numpy as np
import random
from PIL import Image
from itertools import combinations
import os
import elo
st.set_page_config(layout="wide")


inpath = os.environ['IMG_POOL']
elos = os.environ["ELO_JSON"]
prefs = elo.PreferenceStructure(file=elos,path=inpath)

def get_files():
	return glob(inpath+"/*")

def display_img(img):
	global prefs
	try:
		st.image(Image.open(img),use_column_width=True)
		return True
	except:
		prefs.delete(img)
		return False

files = get_files() 

left_column, center_column, right_column = st.beta_columns([4,1,4])

fast = center_column.checkbox("2X")
slow = center_column.checkbox("0.5X")
top = center_column.checkbox("top")
topk = 5 if top else None
velocity = 1
if fast: velocity *= 2
if slow: velocity /= 2


left_img, right_img = prefs.sample_pair(topk)
plusleft = left_column.button("<<",key="plusleft")
plusright = right_column.button(">>",key="plusright")

left_column.write(prefs.rounded_score(left_img))
right_column.write(prefs.rounded_score(right_img))


with left_column: left_ok = display_img(left_img)		
with right_column: right_ok = display_img(right_img)
center_column.write(prefs.expected(left_img,right_img))
if plusleft:
	prefs.update(1,left_img,right_img,velocity)
if plusright:
	prefs.update(-1,left_img,right_img,velocity)