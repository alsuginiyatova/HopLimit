import math
import matplotlib.pyplot as plt
from random import randrange

def calc_bandwidth_without_errors(n):
	t = (n + 1) / 2
	h = math.log2(n)
	banw = h / t
	return banw

def calc_bandwidth_with_errors(n):
	t = (n + 1) / 2
	h = 0
	for j in range(1, n + 1):
		h_y_x = 0
		for i in range(1, n + 1):
			h_ex = 0
			if j == i:
				h_ex += 0.6 * math.log2(0.6) * (-1)
			elif j == (i - 1) or j == (i + 1):
				h_ex += 0.2 * math.log2(0.2) * (-1)
			else:
				h_ex += (1/j) * math.log2(1/j) * (-1)
			h_y_x = (-1) * (1/i) * h_ex
		h += ((1 / n) * math.log2(1 / n)) * (-1) - h_y_x
	banw = h / t
	return banw

def calc_bandwidth_with_probability(n):
	t = (n + 1) / 2
	h = 0
	for n_tmp in range(1, n + 1):
	 		h += ((1 / 2 ** n_tmp) * math.log2(1 / 2 ** n_tmp)) * (-1)
	banw = h / t
	return banw

calculate_fn = [calculate_bandwidth_without_errors, calculate_bandwidth_with_errors, calculate_bandwidth_with_probability]

for fn in calculate_fn:
	bandwidth_max = 0
	n_find = 0
	bandwidths = []
	n_x = []
	for n in range(1, 30):
		bandwidth_for_n = fn(n)
		if bandwidth_for_n > bandwidth_max:
			bandwidth_max = bandwidth_for_n
			n_find = n
		bandwidths.append(bandwidth_for_n)
		n_x.append(n)
	plt.suptitle('График зависимости пропускной способности от числа символов (N)')
	plt.xlabel('Число символов (N)')
	plt.ylabel('Пропускная способность')
	plt.plot(n_x, bandwidths)
	plt.grid(True)
	plt.xticks(x, n_x, rotation="vertical")
	plt.scatter(n_find, bandwidth_max, color='red', marker='o')
	plt.show()
	plt.clf()
	print("Максимальная пропускная способность = ", bandwidth_max)
	print("Число N = ", n_find)
	print(bandwidths)
