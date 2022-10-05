#!/usr/bin/python3

import sympy as sp

sp.init_printing()

# Смысл используемых переменных:
# matrix : тип sp.Matrix + следующие атрибуты:
#     .free : число: столбец, который должен войти в базис;
#     .nonfree : число: столбец, который должен выйти из базиса.
# freeList : список чисел: столбцы, входящие в базис.

# войдёт в базис (столбец); а пока — вне базиса: → matrix.nonfree
def compute_nonfree(matrix, freeList):
	minimum = 0
	for j in range(1, matrix.cols):
		if not (j in freeList) and matrix[0, j] < minimum:
			matrix.nonfree = j
			minimum = matrix[0, j]
	return True if minimum else False

# выйдет из базиса (строка); а пока — в базисе: ⇒ matrix.free
def compute_free(matrix):
	upd = False
	for i in range(1, matrix.rows):
		if matrix[i, matrix.nonfree] > 0:
			if (not upd) or matrix[i, 0] / matrix[i, matrix.nonfree] < minimum:
				minimum = matrix[i, 0] / matrix[i, matrix.nonfree]
				matrix.free = i
				upd = True
	return upd

def update_matrix(matrix, free, nonfree):
	coef = matrix[free, nonfree]
	for j in range(matrix.cols):
		matrix[free, j] /= coef
	for i in range(0, matrix.rows):
		if i != free:
			coef = matrix[i, nonfree]
			for j in range(matrix.cols):
				matrix[i, j] -= coef * matrix[free, j]
	print("out: {}, in: {}".format(free, nonfree))
	sp.pprint(matrix); print(); print()

# симплекс-метод расписан в этой процедуре.
# на входе — симплексная таблица и список базисных столбцов
# на выходе — симплексная таблица по результатам преобразований
def simplex(matrix, freeList):
	sp.pprint(matrix); print(); print()
	while True:
		if not compute_nonfree(matrix, freeList):  # в базис войдёт (столбец)
			return matrix
		if not compute_free(matrix):               # из базиса выйдет (строка)
			return None
		freeList[matrix.free-1] = matrix.nonfree
		update_matrix(matrix, matrix.free, matrix.nonfree)

def solve(rowList, height, width):
	m = sp.zeros(height, width + height - 1)
	for i in range(len(rowList)):
		for j in range(len(rowList[i])):
			m[i, j] = rowList[i][j]
		if i > 0:
			m[i, width+i-1] = 1
	return simplex(m, list(range(width, width+height-1)))
