from OPConsistency_GUI import GUI

'''
Import the class GUI from OPConsistency_GUI for creating an instance G which contains the method GUI for showing up the GUI 
(and subsequent data extraction, analysis and plots)

In OPConsistency_GUI, Plot is imported from OPConsistency_plot, which plots the graph with the method hist.

In OPConsistency_plot, OPConsistency is imported from OPConsistency_db to extract and analyse data and selecting data with SQL.

In OPConsistency_db, the mkdf method is available (which is used in the hist method in OPConsistency_plot) to organize
extracted data from database to a pandas dataframe.
'''


# DB_PATH = "O:\protons\Work in Progress\Marcus\Asset_QA_Database\PracticAssetsDatabaseFeb23_be.accdb"
DB_PATH = r"\\9.40.120.20\\rtassetBE\AssetsDatabase_be.accdb"
# DB_PASSWORD = "Pr0ton5%"
DB_PASSWORD = "JoNiSi"
G = GUI(DB_PATH, DB_PASSWORD)
G.GUI()