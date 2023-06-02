from OPConsistency_db import OPConsistency
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

class Plot(OPConsistency):
    def __init__(self, DB_PATH, DB_PASSWORD, hue, filters={}, Adate='1900-01-01', Adate2='2025-01-01', error=0):
        super().__init__(DB_PATH, DB_PASSWORD, hue, filters, Adate, Adate2, error)

    def plot(self,x='Diff (%)',combined=0, hist=1):
        self.df = self.mkdf().reset_index(drop=True)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        if hist: # plot histogram
            if combined:
                sns.histplot(self.df, x=x, hue=self.hue)
                plt.show()
            else:
                for legend in self.filters[self.hue]:
                    print(legend)
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    print(legend_df)
                    # plot histogram of % difference
                    sns.histplot(data=legend_df, x=x, hue=self.hue)
                    plt.show()
        else: # plot time series
            if combined:
                fig, ax = plt.subplots()
                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                plt.show()
                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                plt.show()
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                plt.show()
            else:
                for legend in self.filters[self.hue]:
                    print(legend)
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    print(legend_df)
                    # plot lineplot
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    plt.show()
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    plt.show()
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    plt.show()