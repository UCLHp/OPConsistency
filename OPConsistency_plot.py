from OPConsistency_db import OPConsistency
import tkinter as tk
import seaborn as sns
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np


class Plot(OPConsistency):
    def __init__(self, DB_PATH, DB_PASSWORD, hue, filters={}, Adate='1900-01-01', Adate2='2025-01-01', error=0):
        super().__init__(DB_PATH, DB_PASSWORD, hue, filters, Adate, Adate2, error)
    
    def _show_plot(self, fig):
        # Create a root window and hide it
        root = tk.Tk()
        root.withdraw()
        # Create a top-level window
        window = tk.Toplevel(root)
        window.title("Plot Window")
        # Create a canvas and draw the plot on the window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # Define a function that quits the root window if no top-level windows are open
        def quit_root():
            # Get a list of all the children of the root window
            children = root.winfo_children()
            # Loop through the children and check if any of them are top-level windows
            for child in children:
                # If the child is a top-level window and it exists, return without quitting the root window
                if isinstance(child, tk.Toplevel) and child.winfo_exists():
                    return
            # If no top-level windows are found, quit the root window
            root.quit()
        # Bind the function to the destroy event of the top-level window
        window.bind("<Destroy>", lambda event: quit_root())
        # Start the main loop
        root.mainloop()

    def plot(self,x='Diff (%)',combined=0, save=0, hist=1):
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
                if save: plt.savefig('{}_hist.png'.format(', '.join(self.filters[self.hue])))
                print(fig)
                #self._show_plot(fig=fig)
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
                    if save: plt.savefig('{}_hist.png'.format(legend))
                    #self._show_plot(fig=fig)
                    plt.show()
                    plt.close()
        else: # plot time series
        
            self.warning_df = self.df[((self.df['Diff (%)'] >= 0.5) & (self.df['Diff (%)'] < 2)) | ((self.df['Diff (%)'] <= -0.5) & (self.df['Diff (%)'] > -2))]
            self.fail_df = self.df[(self.df['Diff (%)'] >= 2) | (self.df['Diff (%)'] <= -2)]
            if not self.warning_df.empty:
                print('\nwarning:\n')
                print(self.warning_df)
            if not self.fail_df.empty:
                print('\nfail:\n')
                print(self.fail_df)
        
            if combined:
                # fig, ax = plt.subplots()
                # sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                # sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                # ax.set_title(title, wrap=True)
                # sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                # plt.tight_layout()
                # if save:plt.savefig('{}_combined.png'.format(', '.join(self.filters[self.hue])))
                # self._show_plot(fig=fig)
                # plt.show()
                # plt.close()

                fig, ax = plt.subplots()
                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                ax.axhline(0.5, color='y')
                ax.axhline(-0.5, color='y')
                if (self.df['Diff (%)'] >= 1.8).any():
                    ax.axhline(2, color='r')
                if (self.df['Diff (%)'] <= -1.8).any():
                    ax.axhline(-2, color='r')
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                if save: plt.savefig('{}_scatter.png'.format(', '.join(self.filters[self.hue])))
                #self._show_plot(fig=fig)
                plt.show()
                plt.close()
                fig, ax = plt.subplots()
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue)
                ax.axhline(0.5, color='y')
                ax.axhline(-0.5, color='y')
                if (self.df['Diff (%)'] >= 1.8).any():
                    ax.axhline(2, color='r')
                if (self.df['Diff (%)'] <= -1.8).any():
                    ax.axhline(-2, color='r')
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                if save: plt.savefig('{}_line.png'.format(', '.join(self.filters[self.hue])))
                #self._show_plot(fig=fig)
                plt.show()
                plt.close()
                
                # # Prepare for FFT plot
                # fig, ax = plt.subplots()
                # for legend in self.filters[self.hue]:
                #     legend_df = self.df[self.df[self.hue].astype(str) == legend]
                #     # Perform FFT on the data
                #     averaged_df = legend_df.groupby('Date')['Diff (%)'].mean().reset_index()
                #     fft_result = np.fft.rfft(averaged_df['Diff (%)'])
                    
                #     # Calculate the frequencies corresponding to the FFT result
                #     time_values = pd.to_numeric(averaged_df['Date'].values)
                #     sampling_rate = 1 / np.mean(np.diff(time_values))
                #     frequencies = np.fft.rfftfreq(len(averaged_df), 1 / sampling_rate)
                #     # Plot the FFT result
                #     plt.plot(frequencies, np.abs(fft_result), label=legend)
                # plt.xlabel('Frequency')
                # plt.ylabel('Amplitude')
                # plt.title('FFT Analysis')
                # plt.legend()
                # ax.set_title(title, wrap=True)
                # plt.subplots_adjust(right=0.25)
                # plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
                # plt.tight_layout()
                # if save: plt.savefig('{}_FFT.png'.format(', '.join(self.filters[self.hue])))
                # self._show_plot(fig=fig)
                # plt.show()
                # plt.close()

            else:
                for legend in self.filters[self.hue]:
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    # plot lineplot
                    # fig, ax = plt.subplots()
                    # sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue, alpha=0.2)
                    # sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    # ax.set_title(title, wrap=True)
                    # sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    # plt.tight_layout()
                    # if save: plt.savefig('{}_combined.png'.format(legend))
                    # self._show_plot(fig=fig)
                    # plt.show()
                    # plt.close()
                    
                    fig, ax = plt.subplots()
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    ax.axhline(0.5, color='y')
                    ax.axhline(-0.5, color='y')
                    if (legend_df['Diff (%)'] >= 1.8).any():
                        ax.axhline(2, color='r')
                    if (legend_df['Diff (%)'] <= -1.8).any():
                        ax.axhline(-2, color='r')
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    if save: plt.savefig('{}_scatter.png'.format(legend))
                    #self._show_plot(fig=fig)
                    plt.show()
                    plt.close()
                    fig, ax = plt.subplots()
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue)
                    ax.axhline(0.5, color='y')
                    ax.axhline(-0.5, color='y')
                    if (legend_df['Diff (%)'] >= 1.8).any():
                        ax.axhline(2, color='r')
                    if (legend_df['Diff (%)'] <= -1.8).any():
                        ax.axhline(-2, color='r')
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    if save: plt.savefig('{}_line.png'.format(legend))
                    #self._show_plot(fig=fig)
                    plt.show()
                    plt.close()
                    
                    # # Perform FFT on the data
                    # averaged_df = legend_df.groupby('Date')['Diff (%)'].mean().reset_index()
                    # fft_result = np.fft.rfft(averaged_df['Diff (%)'])
                    
                    # # Calculate the frequencies corresponding to the FFT result
                    # time_values = pd.to_numeric(averaged_df['Date'].values)
                    # sampling_rate = 1 / np.mean(np.diff(time_values))
                    # frequencies = np.fft.rfftfreq(len(averaged_df), 1 / sampling_rate)
                    
                    # # Plot the FFT result
                    # fig, ax = plt.subplots()
                    # plt.plot(frequencies, np.abs(fft_result), label=legend)
                    # plt.xlabel('Frequency')
                    # plt.ylabel('Amplitude')
                    # plt.title('FFT Analysis')
                    # plt.legend()
                    # ax.set_title(title, wrap=True)
                    # plt.subplots_adjust(right=0.25)
                    # plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
                    # plt.tight_layout()
                    # if save: plt.savefig('{}_FFT.png'.format(legend))
                    # self._show_plot(fig=fig)
                    # plt.show()
                    # plt.close()


