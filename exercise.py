#!/usr/bin/env python
""" Solve polynomials exercise on Yammer.
"""

import csv
import numpy as np
from numpy.polynomial.polynomial import polyval

step2 = np.roots((1, 3, 1))
print step2

step3 = np.roots((3, 2, 1))
print step3

# Create the coefficient sets.  Use meshgrid to do this quickly
c = np.arange(-100, 101, 1)
grid = np.meshgrid(c, c, c)

# Reshape the grid to be 2D: 1st dimension is coefficients (a,b,c) and second
# is the set number. 201^3 = 8,120,601 combinations.
grid = np.array(grid)
grid = grid.reshape(3, 8120601)

# Prime numbers up to 200.  Should be sufficient to capture all non-trivial
# solutions.  As the prime number increases, the number of non-trivial
# solutions decreases to zero.  The trivial solution is a, b & c = 0.
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
          59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107, 109, 113, 127,
          131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
          193, 197, 199]

# Create empty lists to store results.
solutions = []
solution_primes = []

# Loop over all prime numbers in the above list and determine the polynomial
# values for all coefficient combinations for each.  That is 8,120,601
# polynomial calculations per prime number but Python can handle it!
for p in primes:
    # Use the polyval function from the numpy.polynomial package to solve all
    # polynomials at once for each prime number.
    ys = polyval(p, grid, tensor=True)

    # Use the numpy nonzero function to get the array indices of all
    # polynomial solutions equal to zero.
    ix = np.nonzero(ys == 0)[0]

    # Get the corresponding coefficients (a, b, c) from the grid.
    coeffs = grid[:, ix].T

    if coeffs.shape[0] > 1:
        # Save the non-trivial solutions (and the corresponding prime number;
        # we'll need this for output).
        solutions.extend(coeffs.tolist())
        solution_primes.extend([p]*coeffs.shape[0])
    else:
        # Only the trivial (0, 0, 0) solution exists so we've exhausted
        # all prime number possibilities.  Stop the loop.
        break

# Save solutions to CSV file.
fout = open('exercise.csv', 'wb')
cout = csv.writer(fout)
cout.writerow(('a', 'b', 'c', 'Prime', 'Solution'))
for s, p in zip(solutions, solution_primes):
    # Ignore trivial solutions when writing output.
    if sum(s) != 0:
        cout.writerow(s[-1::-1] + [p] + [polyval(p, s)])
fout.close()
