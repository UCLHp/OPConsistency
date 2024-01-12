# OPConsistency
OPConsistency consists of multiple modules that work together to create an application called OPConsistency. Here is a summary of the code:

1. OPConsistency_db module: This module contains the OPConsistency class, which handles database operations and data manipulation. It connects to a Microsoft Access database, retrieves reference data, and extracts output measurements based on specified filters and date range. The extracted data is converted into pandas DataFrames for further analysis.

2. OPConsistency_plot module: This module imports the OPConsistency class from OPConsistency_db. It defines the Plot class, which extends OPConsistency. The Plot class performs data analysis and provides methods for plotting histograms and time series plots (line and scatterplots) based on the extracted data.

3. OPConsistency_GUI module: This module imports the Plot class from OPConsistency_plot. It defines the GUI class, which utilizes the Tkinter library to create a graphical user interface (GUI) for the OPConsistency application. The GUI allows users to select filters, specify date ranges, and plot histograms based on the available data. It also includes various widgets and functionality, such as checkboxes, buttons, and a calendar for date selection.

4. OPConsistency_main module: This is the main entry point of the OPConsistency application. It imports the GUI class from OPConsistency_GUI. The DB_PATH and DB_PASSWORD variables are set to the path of the Microsoft Access database file and the corresponding password. An instance of the GUI class is created, and the GUI method is called to display the GUI and allow user interaction.

Overall, the code enables users to interact with a GUI to select filters, specify date ranges, and generate histograms and time series plots (line and scatterplots) based on the data extracted from a Microsoft Access database. The application provides a visual representation of the data for analysis and exploration. 

Note: Never press the 'Kill the piggy' button or else...
