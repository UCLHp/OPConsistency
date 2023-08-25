from OPConsistency_db import OPConsistency
import seaborn as sns
import matplotlib
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np


class Plot(OPConsistency):
    def __init__(self, DB_PATH, DB_PASSWORD, hue, filters={}, Adate='1900-01-01', Adate2='2025-01-01', error=0):
        super().__init__(DB_PATH, DB_PASSWORD, hue, filters, Adate, Adate2, error)
    
    def _warning_cond(self, df, scatter, line): # set warning conditions
        warning_df = pd.DataFrame(columns=df.columns)
        
        return warning_df
    
    def _warning_plot(self, df, scatter, line): # plot warning
        if scatter:
            pass

    def plot(self,x='Diff (%)',combined=0, hist=1):
        self.df = self.mkdf().reset_index(drop=True)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        title = '\n'
        for key, value in self.filters.items():
            title += f"{key}: {', '.join(value)}\n"
        title += 'From {} to {}\n'.format(self.Adate, self.Adate2)
        if hist: # plot histogram
            if combined:
                fig, ax = plt.subplots()
                sns.histplot(self.df, x=x, hue=self.hue)
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                plt.savefig('{}_hist.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()
            else:
                for legend in self.filters[self.hue]:
                    print(legend)
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    print(legend_df)
                    # plot histogram of % difference
                    fig, ax = plt.subplots()
                    sns.histplot(data=legend_df, x=x, hue=self.hue)
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    plt.savefig('{}_hist.png'.format(legend))
                    plt.show()
                    plt.close()
        else: # plot time series
            if combined:
                fig, ax = plt.subplots()
                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                plt.savefig('{}_combined.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()

                fig, ax = plt.subplots()
                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                plt.savefig('{}_scatter.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()
                fig, ax = plt.subplots()
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                plt.savefig('{}_line.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()
                
                # Prepare for FFT plot
                fig, ax = plt.subplots()
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
                plt.xlabel('Frequency')
                plt.ylabel('Amplitude')
                plt.title('FFT Analysis')
                plt.legend()
                ax.set_title(title, wrap=True)
                plt.subplots_adjust(right=0.25)
                plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
                plt.tight_layout()
                plt.savefig('{}_FFT.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()

            else:
                for legend in self.filters[self.hue]:
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    # plot lineplot
                    fig, ax = plt.subplots()
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    plt.savefig('{}_combined.png'.format(legend))
                    plt.show()
                    plt.close()
                    fig, ax = plt.subplots()
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    plt.savefig('{}_scatter.png'.format(legend))
                    plt.show()
                    plt.close()
                    fig, ax = plt.subplots()
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    plt.savefig('{}_line.png'.format(legend))
                    plt.show()
                    plt.close()
                    
                    # Perform FFT on the data
                    averaged_df = legend_df.groupby('Date')['Diff (%)'].mean().reset_index()
                    fft_result = np.fft.rfft(averaged_df['Diff (%)'])
                    
                    # Calculate the frequencies corresponding to the FFT result
                    time_values = pd.to_numeric(averaged_df['Date'].values)
                    sampling_rate = 1 / np.mean(np.diff(time_values))
                    frequencies = np.fft.rfftfreq(len(averaged_df), 1 / sampling_rate)
                    
                    # Plot the FFT result
                    fig, ax = plt.subplots()
                    plt.plot(frequencies, np.abs(fft_result), label=legend)
                    plt.xlabel('Frequency')
                    plt.ylabel('Amplitude')
                    plt.title('FFT Analysis')
                    plt.legend()
                    ax.set_title(title, wrap=True)
                    plt.subplots_adjust(right=0.25)
                    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
                    plt.tight_layout()
                    plt.savefig('{}_FFT.png'.format(legend))
                    plt.show()
                    plt.close()


