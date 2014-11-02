import csv, sys, collections

# Cross Product of elements in A and B
def get_cp(A, B):
	return [el_A + el_B for el_A in A for el_B in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = get_cp(rows, cols)

# Define a unit, peer here
unitlist = ([get_cp(rows, c) for c in cols] + 
	[get_cp(r, cols) for r in rows] + 
	[get_cp(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

units = dict((s, [u for u in unitlist if s in u]) 
	for s in squares)

peers = dict((s, set(sum(units[s],[]))-set([s]))
	for s in squares)

# Insert unit tests here.
# Add some more. Maybe related to the question ?
def test():
	assert len(squares) == 81
	assert len(unitlist) == 27
	assert all(len(units[s]) == 3 for s in squares)
	assert all(len(peers[s]) == 20 for s in squares)
	assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
	['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
	['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
	assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
								'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
								'A1', 'A3', 'B1', 'B3'])
	print 'All tests pass.'

# Now, parsing the grid:

def get_grid_struct(grid):
	
	chars = [c for c in grid if c in digits or c in '0.']

	# Simple test.
	assert len(chars) == 81
	
	return dict(zip(squares, chars))

def input_parse_grid(grid):
	# Generate a list of possible values for all squares
	val = dict((s, digits) for s in squares)
	
	# Now going through the dict returned from get_grid_struct and comparing with all possible values for each square using val
	for s,d in get_grid_struct(grid).items():
		# If d is not in digits, then d is already assigned
		# If assign returns false, unable to assign
		if d in digits and not assign(val, s, d):
			return False 
			# (Fail if we can't assign d to square s.)
	return val

# Constant Propagation

# Eliminate all the other values (except d) from values[s] and propagate.
# Return values, except return False if a contradiction is detected.
def assign(val, s, d):
	# using other_values to keep a track of where we are in the elimination process for this digit
	# other_values are the values left after elimination of d from square 's' because d has been placed in one of its peers.
	other_values = val[s].replace(d, '')
	if all(eliminate(val, s, d_other) for d_other in other_values):
		return val
	else:
		return False

# Now, the elimination procedure from the peers of the square
# Eliminate d from values[s]; propagate when values or places <= 2.
# Return values, except return False if a contradiction is detected.
def eliminate(val, s, d):
	if d not in val[s]:
		return val 
		# Already eliminated
	val[s] = val[s].replace(d,'')
	# If a square s is reduced to one value d_other, then eliminate d_other from the peers.
	if len(val[s]) == 0:
		return False 
		# Contradiction: removed last value
	elif len(val[s]) == 1:
		d_other = val[s]
		if not all(eliminate(val, s_other, d_other) for s_other in peers[s]):
			return False
	# If a unit u is reduced to only one place for a value d, then put it there.
	for u in units[s]:
		dplaces = [s for s in u if d in val[s]]
	if len(dplaces) == 0:
		return False 
		# Contradiction: no place for this value
	elif len(dplaces) == 1:
		# d can only be in one place in unit; assign it there
			if not assign(val, dplaces[0], d):
				return False
	return val

# Display the puzzle as a 2-D grid.
def display(val):
	width = 1+max(len(val[s]) for s in squares)
	line = '+'.join(['-'*(width*3)]*3)
	for r in rows:
		print ''.join(val[r+c].center(width)+('|' if c in '36' else '') for c in cols)
		if r in 'CF': print line
	print

# Return some element of seq that is true.
def some(seq):
	for e in seq:
		if e: 
			return e
	return False

# Using depth-first search and propagation, try all possible values.
def search(val):
	if val is False:
		return False 
		# Failed earlier
	if all(len(val[s]) == 1 for s in squares): 
		return val ## Solved!
	# Chose the unfilled square s with the fewest possibilities
	n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
	return some(search(assign(values.copy(), s, d)) 
		for d in values[s])

def solve(grid): return search(input_parse_grid(grid))

def input_file(filename):
	fin = open(filename, "r")
	reader = csv.reader(fin)
	grid = ""
	for row in reader:
		for element in row:
			grid += element
	return grid

def output_file(grid, filename):
	fout = open(filename, 'w')
	writer = csv.writer(fout, delimiter = ',')
	line = []
	for label, val in grid.items():
		line.append(val)
		if label.endswith('9'):
			writer.writerow(line)
			line = []

if __name__ == '__main__':
	grid = input_file(sys.argv[1])
	temp_grid = solve(grid)
	solved_grid = collections.OrderedDict(sorted(temp_grid.items()))
	if len(sys.argv) == 2:
		output_file(solved_grid, 'output.csv')
	else:
		output_file(solved_grid, sys.argv[2])