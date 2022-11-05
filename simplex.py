#!/usr/bin/python3

import sympy as sp

sp.init_printing()

# Смысл используемых переменных:
# matrix : тип sp.Matrix + следующие атрибуты:
#     .free : число: столбец, который должен войти в базис;
#     .nonfree : число: столбец, который должен выйти из базиса.
#     .freeList : список чисел: столбцы, входящие в базис.

# войдёт в базис (столбец); а пока — вне базиса: → matrix.nonfree
def compute_nonfree(matrix):
	minimum = 0
	for j in range(1, matrix.cols):
		if not (j in matrix.freeList) and matrix[0, j] < minimum:
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
# на входе — симплексная таблица со списком базисных столбцов
# на выходе — симплексная таблица по результатам преобразований
def simplex(matrix):
	sp.pprint(matrix); print(); print()
	while True:
		if not compute_nonfree(matrix):            # в базис войдёт (столбец)
			return matrix
		if not compute_free(matrix):               # из базиса выйдет (строка)
			return None
		matrix.freeList[matrix.free-1] = matrix.nonfree
		update_matrix(matrix, matrix.free, matrix.nonfree)

# способ вывода симплекс-таблицы matrix: через Gui.
# процедура возвращает виджет w, показывающий симплекс-таблицу.

from PyQt5 import QtWidgets
import numpy as np

def get_table(matrix, names):
	r, c = matrix.rows, matrix.cols
	w = QtWidgets.QTableWidget(r+1, c+1)
	for i, j in np.ndindex(r, c):
		w.setItem(i+1, j+1, QtWidgets.QTableWidgetItem(str(matrix[i, j])))
	for j in range(c-1):
		w.setItem(0, j+2, QtWidgets.QTableWidgetItem(names[j]))
	for i in range(r-1):
		w.setItem(i+2, 0, QtWidgets.QTableWidgetItem(names[matrix.freeList[i]-1]))
	w.setItem(0, 1, QtWidgets.QTableWidgetItem('!'))
	w.setItem(1, 0, QtWidgets.QTableWidgetItem('!'))
	return w
