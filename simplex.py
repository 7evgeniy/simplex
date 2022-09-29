#!/usr/bin/python3

import sympy as sp

sp.init_printing()

# составить симплексную таблицу на основе ограничений:
def make(columnList):
	cols = len(columnList)
	rows = len(columnList[0])
	for i in range(1, cols):
		if len(columnList[i]) != rows:
			return None
	matrix = sp.Matrix(rows, cols-1, lambda i, j: columnList[j][i])
	matrix = matrix.row_join(sp.Matrix([[0 for i in range(rows-1)], sp.eye(rows-1)]))
	matrix = matrix.row_join(sp.Matrix(columnList[cols-1]))
	return matrix

# Смысл используемых переменных:
# matrix : тип sp.Matrix + следующие атрибуты:
#     .free : число: столбец, который должен войти в базис;
#     .nonfree : число: столбец, который должен выйти из базиса.
# freeList : список чисел: столбцы, входящие в базис.

# выйдет из базиса: → matrix.nonfree
def compute_nonfree(matrix, freeList):
	minimum = 0
	for j in freeList:
		if matrix[0, j] < minimum:
			matrix.nonfree = j
			minimum = matrix[0, j]
	return True if minimum else False

# войдёт в базис: ⇒ matrix.free
def compute_free(matrix, freeList):
	upd = False
	last = matrix.cols - 1
	for i in range(1, matrix.rows):
		if matrix[i, matrix.nonfree] > 0:
			if (not upd) or matrix[i, last] / matrix[i, matrix.nonfree] < minimum:
				minimum = matrix[i, last] / matrix[i, matrix.nonfree]
				matrix.free = i
				upd = True
	return upd

def recompute_freeList(matrix, freeList):
	for j in range(matrix.cols-1):
		if j not in freeList and matrix[matrix.free, j] == 1:
			break     # разыскать новый базисный столбец в матрице → j
	return [i if i != matrix.nonfree else j for i in freeList]

def update_matrix(matrix, free, nonfree):
	coef = matrix[free, nonfree]
	for j in range(matrix.cols):
		matrix[free, j] /= coef
	for i in range(0, matrix.rows):
		if i != free:
			coef = matrix[i, nonfree]
			for j in range(matrix.cols):
				matrix[i, j] -= coef * matrix[free, j]
	sp.pprint(matrix); print(); print()

def simplex(matrix, freeList):
	sp.pprint(matrix); print(); print()
	while True:
		if not compute_nonfree(matrix, freeList):
			return True
		if not compute_free(matrix, freeList):
			return False
		freeList = recompute_freeList(matrix, freeList)
		update_matrix(matrix, matrix.free, matrix.nonfree)
