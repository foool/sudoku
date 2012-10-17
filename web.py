# coding: utf-8
import string
import sys, os
import copy
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
render=web.template.render("templates")

urls = (
	'',						'Index',
	'/set',					'Set',
	'/set/',				'Set',
	'/.*',				  	'Index',
	'/sudoku',				'Index',
	'/sudoku/',				'Index'
)
application = web.application(urls, globals()).wsgifunc()

sudoku_map = []

sudoku_nums = {}
sudoku_nums_backup = {}


grid_index = [\
[0,1,2,9,10,11,18,19,20],\
[3,4,5,12,13,14,21,22,23],\
[6,7,8,15,16,17,24,25,26],\
[27,28,29,36,37,38,45,46,47],\
[30,31,32,39,40,41,48,49,50],\
[33,34,35,42,43,44,51,52,53],\
[54,55,56,63,64,65,72,73,74],\
[57,58,59,66,67,68,75,76,77],\
[60,61,62,69,70,71,78,79,80]]



def row_reduction(sudoku_map,i):
	global sudoku_nums;
	for j in xrange(0,9):
		index = i*9 + j
		value = sudoku_map[index]
		if value == 0:
			pass
		else:
			for k in xrange(0,9):
				cur = i*9 + k
				if cur == index:
					pass
				else:
					if value in sudoku_nums[cur]:
						sudoku_nums[cur].remove(value)
					else:
						pass
	return sudoku_map

def col_reduction(sudoku_map,i):
	global sudoku_nums;
	for j in xrange(0,9):
		index = i + j*9
		value = sudoku_map[index]
		if value == 0:
			pass
		else:
			for k in xrange(0,9):
				cur = i + k*9
				if cur == index:
					pass
				else:
					if value in sudoku_nums[cur]:
						sudoku_nums[cur].remove(value)
					else:
						pass
	return sudoku_map

	

def grid_reduction(sudoku_map,i):
	global sudoku_nums;
	for j in xrange(0,9):
		index = grid_index[i][j]
		value = sudoku_map[index]
		if value == 0:
			pass
		else:
			for k in xrange(0,9):
				cur = grid_index[i][k]
				if cur == index:
					pass
				else:
					if value in sudoku_nums[cur]:
						sudoku_nums[cur].remove(value)
					else:
						pass
	return sudoku_map

def single_in_row_col_grid(sudoku_map,i,value):
	row = i/9
	col = i%9
	grid = (row/3)*3 + col/3

	'''check row'''
	for j in xrange(0,9):
		if j == col:
			continue
		else:
			if value in sudoku_nums[row*9+j]:
				break
		if j == 8:
			return 1

	'''check column'''
	for j in xrange(0,9):
		if j == row:
			continue
		else:
			if value in sudoku_nums[j*9+col]:
				break
		if j == 8:
			return 1

	'''check grid'''
	for j in xrange(0,9):
		cur = grid_index[grid][j]
		if cur == i:
			continue
		else:
			if value in sudoku_nums[cur]:
				break
		if j == 8:
			return 1
	return 0

def sudoku_map_reduction(sudoku_map):
	global sudoku_nums
	for i in xrange(0,81):
		if len(sudoku_nums[i]) == 1:
			'''this position has only choice'''
			sudoku_map[i] = sudoku_nums[i][0]
		if len(sudoku_nums[i]) == 0:
			sudoku_map[i] = 0;
		else:
			for value in sudoku_nums[i]:
				'''this is the only choice in row
				   or column or grid of the position'''
				if single_in_row_col_grid(sudoku_map,i,value) == 1:
					sudoku_map[i] = value
					sudoku_nums[i] = [value]
	return sudoku_map

def looper(sudoku_map):
	for i in xrange(0,9):
		row_reduction(sudoku_map,i)
		col_reduction(sudoku_map,i)
		grid_reduction(sudoku_map,i)

		sudoku_map = sudoku_map_reduction(sudoku_map)
	return sudoku_map

def can_do(i,value):
	global sudoku_map
	global sudoku_nums
	global sudoku_nums_backup

	sudoku_map_tmp = copy.deepcopy(sudoku_map)
	sudoku_nums_tmp = copy.deepcopy(sudoku_nums)
	sudoku_nums_backup_tmp = copy.deepcopy(sudoku_nums_backup)

	sudoku_map[i] = value
	sudoku_nums[i] = [value]
	
	for i in xrange(0,7):
		sudoku_nums_backup = copy.deepcopy(sudoku_nums)
		sudoku_map = looper(sudoku_map)
		if 0 not in sudoku_map:
			return 1
		else:
			continue
	sudoku_map = copy.deepcopy(sudoku_map_tmp)
	sudoku_nums = copy.deepcopy(sudoku_nums_tmp)
	sudoku_nums_backup = copy.deepcopy(sudoku_nums_backup_tmp)
	return 0



def hard_try():
	count = 0
	for i in xrange(0,81):
		for value in sudoku_nums[i]:
			count = count + 1
			if count > 100:
				render.error("Can not find the answer!")
				return 0
			if can_do(i,value) == 1:
				return 1
			else:
				pass
	return 0

def main(web_map):
	global sudoku_map
	global sudoku_nums
	global sudoku_nums_backup
	
	sudoku_map = copy.deepcopy(web_map)
	for i in xrange(0,81):
		if sudoku_map[i]==0:
			sudoku_nums[i] = [1,2,3,4,5,6,7,8,9]
		else:
			sudoku_nums[i] = [sudoku_map[i]]
	count = 1
	while 1:
		count = count + 1
		if count > 100:
			return 0
		if cmp(sudoku_nums, sudoku_nums_backup) == 0:
			sudoku_nums_backup = sudoku_nums
			if 0 in sudoku_map:
				if hard_try() == 1:
					return map(str,sudoku_map)
				else:
					return 0
			else:
				return map(str,sudoku_map)
		else:
			sudoku_nums_backup = copy.deepcopy(sudoku_nums)
			sudoku_map = looper(sudoku_map)

class Index:
	def GET(self):
		return render.index("Welcome",0)
	
	def POST(self):
		con = web.input()
		list_of_all = []
		for i in xrange(0,81):
			elem = con.get("n%02u"%i, None)
			if len(elem) == 0:
				list_of_all.append(0)
			elif len(elem) == 1:
				list_of_all.append(ord(elem)-48)
			else:
				return render.error("Out of range (1-9) error!")
		web_map = copy.deepcopy(list_of_all)
		list_of_all = main(web_map)
		if list_of_all == 0:
			return render.error("Can not find the answer!")
		else:
			return render.index(''.join(list_of_all),1)

class Set:
	def GET(self):
		return render.index("Welcome",0)
	
	def	POST(self):
		con = web.input()
		value_set = con.get("textarea", None)
		return render.index(value_set.strip(),0)
		
		
if __name__ == "__main__":
	application.run()