from OPConsistency_db import OPConsistency
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

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
                
                # if scatter triggered the warning then mark it as red and set variable
                
                
                # similarly for line (avg of points)
                
                # finally count total amounts of warnings triggered and labels[-1] to -i = ''
                
                plt.show()

                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                plt.show()
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                plt.show()
                
                # Prepare for FFT plot
                for legend in self.filters[self.hue]:
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    # Perform FFT on the data
                    averaged_df = legend_df.groupby('Date')['Diff (%)'].mean().reset_index()
                    fft_result = np.fft.rfft(averaged_df['Diff (%)'])
                    
                    # Calculate the frequencies corresponding to the FFT result
                    time_values = pd.to_numeric(averaged_df['Date'].values)
                    sampling_rate = 1 / np.mean(np.diff(time_values))
                    frequencies = np.fft.rfftfreq(len(averaged_df), 1 / sampling_rate)
                    # Plot the FFT result
                    plt.plot(frequencies, np.abs(fft_result), label=legend)
                plt.legend()
                plt.show()

            else:
                for legend in self.filters[self.hue]:
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    # plot lineplot
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    plt.show()
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    plt.show()
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    plt.show()
                    
                    # Perform FFT on the data
                    averaged_df = legend_df.groupby('Date')['Diff (%)'].mean().reset_index()
                    fft_result = np.fft.rfft(averaged_df['Diff (%)'])
                    
                    # Calculate the frequencies corresponding to the FFT result
                    time_values = pd.to_numeric(averaged_df['Date'].values)
                    sampling_rate = 1 / np.mean(np.diff(time_values))
                    frequencies = np.fft.rfftfreq(len(averaged_df), 1 / sampling_rate)
                    
                    # Plot the FFT result
                    plt.plot(frequencies, np.abs(fft_result), label=legend)
                    plt.xlabel('Frequency')
                    plt.ylabel('Amplitude')
                    plt.title('FFT Analysis')
                    plt.legend()
                    plt.show()


