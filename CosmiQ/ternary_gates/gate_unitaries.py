"""Definition of predefined gate matrices and related utility functions."""

import numpy as np
import sympy

def x_01():
	return sympy.Matrix(
		[
			[0, 1, 0],
			[1, 0, 0],
			[0, 0, 1]
		]
	)

def x_02():
	return sympy.Matrix(
		[
			[0, 0, 1],
			[0, 1, 0],
			[1, 0, 0]
		]
	)

def x_12():
	return sympy.Matrix(
		[
			[1, 0, 0],
			[0, 0, 1],
			[0, 1, 0]
		]
	)

def h_01():
	return sympy.Matrix(
		[
			[1/np.sqrt(2),  1/np.sqrt(2), 0],
			[1/np.sqrt(2), -1/np.sqrt(2), 0],
			[0, 0, 1]
		]
	)

def h_02():
	return sympy.Matrix(
		[
			[1/np.sqrt(2),  0, 1/np.sqrt(2)],
			[0, 1, 0],
			[1/np.sqrt(2), 0, -1/np.sqrt(2)]
		]
	)

def h_12():
	return sympy.Matrix(
		[
			[1, 0, 0],
			[0, 1/np.sqrt(2), 1/np.sqrt(2)],
			[0, 1/np.sqrt(2), -1/np.sqrt(2)]
		]
	)

def walsh_h():
	return sympy.Matrix(
		[
			[1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)],
			[1/np.sqrt(3), np.exp(1j*2*np.pi/3), np.exp(-1j*2*np.pi/3)],
			[1/np.sqrt(3), np.exp(-1j*2*np.pi/3), np.exp(1j*2*np.pi/3)]
		]
	)
	
