The code works as follows:

#Run as: 
    python sudoku.py test.csv 
or as
    python sudoku.py test.csv out.csv

If no output file is specified, then an default output.csv file is generated with the output in csv, row-wise format.

#Notation:
A Sudoku puzzle is a grid of 81 squares; label the columns 1-9, the rows A-I, and call a collection of nine squares (column, row, or box) a unit and the squares that share a unit the peers. A puzzle leaves some squares blank and fills others with digits. 

for example:

 A1 A2 A3| A4 A5 A6| A7 A8 A9    
 B1 B2 B3| B4 B5 B6| B7 B8 B9    
 C1 C2 C3| C4 C5 C6| C7 C8 C9    
---------+---------+---------    
 D1 D2 D3| D4 D5 D6| D7 D8 D9    
 E1 E2 E3| E4 E5 E6| E7 E8 E9    
 F1 F2 F3| F4 F5 F6| F7 F8 F9    
---------+---------+---------    
 G1 G2 G3| G4 G5 G6| G7 G8 G9    
 H1 H2 H3| H4 H5 H6| H7 H8 H9    
 I1 I2 I3| I4 I5 I6| I7 I8 I9    