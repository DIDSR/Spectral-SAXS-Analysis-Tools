This folder contains an Open-Source Data Analysis Software for Spectroscopic Photon Counting
By: Andrew Xu, Eshan Dahal, Aldo Badano


Purpose: This code was written to standardize and accelerate the processing of spectral photon counting detector data. The script serves as a tool for extracting the
momentum transfer information from a raw scattering profile and allow the user to quickly verify the success of a spectral SAXS measurement.


Structure: There are three python files: function, main, and hxtV3Read.
"function.py" contains all the data analysis and plotting, "main.py" contains the user interface components,
and "hxtV3Read.py" contains the hexitech file reading code. To run the program, the user must run 'main.py'.


Input: Once the program is run, it will prompt the user to browse two files for analysis and 4 inputs:
1. Bin Start: The bin layer(z-axis) the program will begin analysis on
2. Bin End: The bin layer(z-axis) the program will end analysis on
3. Bin Width: The bin layer(z-axis) interval the program will do analysis on, which is bin start to bin end.
4. Energy Window: The bin layer(z-axis) interval the program will do analysis and put onto 3d graphs.


Output: 6 graphs will be produced from the inputs:
Graph #1: A color mesh of the counts for each pixel of each Energy window interval created
Graph #2: A color mesh of the counts for each pixel of the overall interval (bin start to bin end)
Graph #3: A reference graph for graph #2
Graph #4: 3D Graph of the combined counts of every possible interval created through energy window
Graph #5: The difference in counts for each pixel between the sample and the background data
Graph #6: The counts for both the sample and background data (2 lines).


How Different Inputs will Change the Way the Program Analyzes the Data:
-----------------------
For the following inputs, Bin Start will always equal 30 and Bin End will equal 45.
The numbers in [] represents which the layers the program will analyze the data on and sum together.
Each [] represents a line/graph in the 3D graphs(#1, #4)
-----------------------
Bin Width: 1, Energy Window: 1
Overall Analysis and Graphs (#2, #5, #6): [30, 31, 32..... 45]
Interval Analysis and Graphs(#1, #4): [30], [31], [32]..... [45] --> 16 Lines/Graphs
-----------------------
Bin Width: 1, Energy Window: 5
Overall Analysis and Graphs: [30, 31, 32..... 45]
Interval Analysis and Graphs: [30, 31, 32, 33, 34], [35, 36.. 39], [40, 41.. 44], [45, 46.. 49] --> 4 Lines/Graphs
-----------------------
Bin Width: 1, Energy Window: 15
Overall Analysis and Graphs: [30, 31, 32..... 45]
Interval Analysis and Graphs: [30, 31, 32..... 44], [45, 46, 47..... 59] --> 2 Line/Graph
-----------------------
Bin Width: 1, Energy Window: 16
Overall Analysis and Graphs: [30, 31, 32..... 45]
Interval Analysis and Graphs: [30, 31, 32..... 45]  --> 1 Line/Graph
-----------------------
Bin Width: 2, Energy Window: 5
Overall Analysis and Graphs: [30, 32, 34..... 44]
Interval Analysis and Graphs: [30, 32, 34], [35, 37, 39], [40, 42, 44], [45, 47, 49] --> 4 Lines/Graphs


Sample Input and Output:
-----------------------
Background File: "2020_aug31_1mA_300s_syringe_empty.hxt"
Sample File: "2020_aug31_1mA_300s_caffeine.hxt"
Bin Start: 30
Bin End: 45
Bin Width: 1
Energy Window: 5
-----------------------
The Outputted Graphs are in the "Figures" folder.