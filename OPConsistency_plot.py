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
        root = tk.Tk()
        root.withdraw()
        window = tk.Toplevel(root)
        window.title("Plot Window")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        def quit_root():
            children = root.winfo_children()
            for child in children:
                if isinstance(child, tk.Toplevel) and child.winfo_exists():
                    return
            root.quit()

        window.bind("<Destroy>", lambda event: quit_root())
        root.mainloop()

    def plot(self, x='Diff (%)', combined=0, save=0, hist=1):
        self.df = self.mkdf().reset_index(drop=True)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        title = '\n'
        for key, value in self.filters.items():
            title += f"{key}: {', '.join(value)}\n"
        title += 'From {} to {}\n'.format(self.Adate, self.Adate2)

        if hist:  # plot histogram
            if combined:
                fig, ax = plt.subplots()
                sns.histplot(self.df, x=x, hue=self.hue)
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                if save:
                    plt.savefig('{}_hist.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()
            else:
                for legend in self.filters[self.hue]:
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    fig, ax = plt.subplots()
                    sns.histplot(data=legend_df, x=x, hue=self.hue)
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    if save:
                        plt.savefig('{}_hist.png'.format(legend))
                    plt.show()
                    plt.close()
        else:  # plot time series
            self.warning_df = self.df[((self.df['Diff (%)'] >= 0.5) & (self.df['Diff (%)'] < 2)) |
                                      ((self.df['Diff (%)'] <= -0.5) & (self.df['Diff (%)'] > -2))]
            self.fail_df = self.df[(self.df['Diff (%)'] >= 2) | (self.df['Diff (%)'] <= -2)]
            if not self.warning_df.empty:
                print('\nwarning:\n')
                print(self.warning_df)
            if not self.fail_df.empty:
                print('\nfail:\n')
                print(self.fail_df)

            # Dynamically create a palette with enough colors
            unique_hue_values = self.df[self.hue].nunique()
            palette = sns.hls_palette(n_colors=unique_hue_values, l=.5, s=1)
            
            if combined:
                fig, ax = plt.subplots()
                sns.scatterplot(self.df, x='Date', y='Diff (%)', hue=self.hue, palette=palette)
                ax.axhline(0.5, color='y')
                ax.axhline(-0.5, color='y')
                if (self.df['Diff (%)'] >= 1.8).any():
                    ax.axhline(2, color='r')
                if (self.df['Diff (%)'] <= -1.8).any():
                    ax.axhline(-2, color='r')
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                if save:
                    plt.savefig('{}_scatter.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()

                fig, ax = plt.subplots()
                sns.lineplot(self.df, x='Date', y='Diff (%)', hue=self.hue, palette=palette)
                ax.axhline(0.5, color='y')
                ax.axhline(-0.5, color='y')
                if (self.df['Diff (%)'] >= 1.8).any():
                    ax.axhline(2, color='r')
                if (self.df['Diff (%)'] <= -1.8).any():
                    ax.axhline(-2, color='r')
                ax.set_title(title, wrap=True)
                sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                plt.tight_layout()
                if save:
                    plt.savefig('{}_line.png'.format(', '.join(self.filters[self.hue])))
                plt.show()
                plt.close()

            else:
                for legend in self.filters[self.hue]:
                    legend_df = self.df[self.df[self.hue].astype(str) == legend]
                    
                    fig, ax = plt.subplots()
                    sns.scatterplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue, palette=palette)
                    ax.axhline(0.5, color='y')
                    ax.axhline(-0.5, color='y')
                    if (legend_df['Diff (%)'] >= 1.8).any():
                        ax.axhline(2, color='r')
                    if (legend_df['Diff (%)'] <= -1.8).any():
                        ax.axhline(-2, color='r')
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    if save:
                        plt.savefig('{}_scatter.png'.format(legend))
                    plt.show()
                    plt.close()

                    fig, ax = plt.subplots()
                    sns.lineplot(data=legend_df, x='Date', y='Diff (%)', hue=self.hue, palette=palette)
                    ax.axhline(0.5, color='y')
                    ax.axhline(-0.5, color='y')
                    if (legend_df['Diff (%)'] >= 1.8).any():
                        ax.axhline(2, color='r')
                    if (legend_df['Diff (%)'] <= -1.8).any():
                        ax.axhline(-2, color='r')
                    ax.set_title(title, wrap=True)
                    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
                    plt.tight_layout()
                    if save:
                        plt.savefig('{}_line.png'.format(legend))
                    plt.show()
                    plt.close()
