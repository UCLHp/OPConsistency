from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import pypyodbc
from OPConsistency_plot import Plot

class GUI(Plot):
    def __init__(self, DB_PATH, DB_PASSWORD, hue=None, filters={}, Adate='1900-01-01', Adate2='2025-01-01', error=0):
        super().__init__(DB_PATH, DB_PASSWORD, hue, filters, Adate, Adate2, error)
        
    def _fetch_str(self, sql): # pulling data from the database for the GUI
        try: # connecting to the database
            new_connection = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;PWD=%s'%(self.DB_PATH,self.DB_PASSWORD)   
            conn = pypyodbc.connect(new_connection)
            cursor = conn.cursor()
        except: # dealing with errors while connecting to the database
            cursor.close()
            conn = None # close database connection
            self.error='conn_error'
            return self.error
        
        try: # executing sql
            cursor.execute(sql)
            records = cursor.fetchall()
            conn.commit()
        except: # dealing with errors while executing sql
            self.error='fetch_error'
            return self.error
        finally: # executed regardless of whether an error has occured
            cursor.close()
            conn = None # close database connection
        
        records_liststr = []
        for r in records:
            records_str = [str(value) for value in r]
            records_liststr.append(records_str)
            
        return records_liststr
            
    def _calendar(self, startend, Adate_datetext): # the calendar for date selection
        def cal_done(close):
            if startend: # end date
                self.Adate2 = '2025-01-01' if close else cal.selection_get()
                Adate_datetext[1].config(text=self.Adate2)
            else: # start date
                self.Adate = '1900-01-01' if close else cal.selection_get()
                Adate_datetext[0].config(text=self.Adate)
            top.destroy()
            root.quit()

        root = Tk()
        root.withdraw() # keep the root window from appearing

        top = Toplevel(root)
        top.iconbitmap("pig.ico")
        top.protocol("WM_DELETE_WINDOW", lambda: cal_done(1))

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="heart")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=lambda: cal_done(0)).pack()

        #selected_date = None
        root.mainloop()

    # Function to toggle the state of suboptions
    def _toggle_suboptions(self, col, hue_triggered): # enabling or disabling suboptions based on their master checkbox
        if hue_triggered:
            self.check_dict[col][0].state(['selected'])
            self.var_dict[col][0].set(1)
            
        state = self.check_dict[col][0].instate(['selected'])
        for suboption in self.check_dict[col][1:]:
            suboption.configure(state=NORMAL) if state else suboption.configure(state=DISABLED)
            
    def _plot(self): # preparing parameters for the plot
        self.hue = self.hue_combobox.get()
        if self.hue:
            plot = 1
            for col in self.option_dict:
                if self.var_dict[col][0].get():
                    if all(i.get() == 0 for i in self.var_dict[col][1:]):
                        plot = 0
                        messagebox.showwarning("Oink!", "A filter is selected but nothing is included. To include all elements in the filter, just deselect the filter.")
                    else:
                        self.filters[self.alias[col]]=[]
                        for i in range(len(self.option_dict[col][1:])):
                            if self.var_dict[col][i+1].get(): self.filters[self.alias[col]] += self.option_dict[col][i+1]
            if plot: self.hist(combined=1 if self.combined_checkbox.instate(['selected']) else 0)
        else:
            messagebox.showwarning("Oink!", "The hue is not selected")
    
    def _close_window(self, root): # for closing the app when the GUI window is closed
        root.destroy()
        root.quit()
                    
    
    def GUI(self): # the method called in OPConsistency_main to deal with the GUI and everything else
        order = ['Energy', 'MachineName', 'GA', 'Electrometer', 'Chamber', 'Adate', '']
        self.alias = {'': '', 'Energy': 'Energy', 'MachineName': 'Gantry', 'GA': 'Gantry angle', 'Electrometer': 'Electrometer', 'Chamber': 'Chamber', 'Adate': 'Date'}
        B = ['Energy']

        # Creating root window
        root = Tk()
        root.title('🐷🐖🐽 Oinkput Consistency Plot GUI 🐽🐖🐷')
        root.iconbitmap("pig.ico")
        
        # Creating a frame for each section
        self.frame_dict={}
        for col in order:
            self.frame_dict[col] = ttk.LabelFrame(root, text=self.alias[col])
        
        # Packing the frames in a grid layout
        i = 0
        for i in range(len(order)):
            self.frame_dict[order[i]].grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
        
        #
        # Make option_dict here with first element the label and then suboptions
        #
        self.option_dict = {}
        self.var_dict = {}
        self.check_dict = {}
        for col in order:
            
            if col not in ['', 'Adate']:
                sql = '''
                    SELECT DISTINCT {}
                    FROM {}
                    '''.format(col, 'OutputConsResults' if col in B else 'OutputConsSession')
                self.option_dict[col] = [col] + self._fetch_str(sql)
                self.var_dict[col] = [IntVar() for _ in range(len(self.option_dict[col]))]
                self.check_dict[col] = [ttk.Checkbutton(self.frame_dict[col], text=str(self.option_dict[col][i])[2:-2] if i else self.alias[self.option_dict[col][i]], variable=self.var_dict[col][i]) for i in range(len(self.option_dict[col]))]
                for i in range(len(self.check_dict[col])): self.check_dict[col][i].grid(row=i, column=0, padx=5, pady=5, sticky="w")
                
                for i in range(len(self.check_dict[col])): self.check_dict[col][i].grid(row=1+(i-1)%5 if i else 0, column=(i-1)//5 if i else 0, padx=15 if i else 5, pady=5, sticky="w")
                
                # handling suboptions
                for suboption in self.check_dict[col][1:]:
                    suboption.configure(state=DISABLED)
                self.check_dict[col][0].configure(command=lambda c=col: self._toggle_suboptions(c, 0))
                
            elif not col: # hue and plot
                hue_label = Label(self.frame_dict[col], text='Hue')
                hue_label.grid(row=0, column=0)
                hue_list = []
                for col2 in order:
                    if col2 not in ['Adate', '']: hue_list.append(self.alias[col2])
                self.hue_combobox = ttk.Combobox(self.frame_dict[col], values=hue_list, state='readonly')
                self.hue_combobox.grid(row=1, column=0)
            
                blank = Label(self.frame_dict[col], text='')
                blank.grid(row=2, column=0)
            
                # default select hue checkbox
                self.hue_combobox.bind('<<ComboboxSelected>>', lambda e: self._toggle_suboptions([i for i in self.alias if self.alias[i]==self.hue_combobox.get()][0], 1))
            
                # combine plots checkbutton
                self.combined_checkbox = ttk.Checkbutton(self.frame_dict[col], text='Combine all plots onto the same axis')
                self.combined_checkbox.state(['!alternate'])
                self.combined_checkbox.grid(row=3, column=0)
            
                # plot button
                self.plot_button = ttk.Button(self.frame_dict[col], text='🐖 Plot 🐖', command= self._plot)
                self.plot_button.grid(row=4, column=0)
                
            else: # Adate
                Adate_datetext = ['1900-01-01', '2025-01-01']
                Adate_button = ['Start Date', 'End Date']
                Adate_datetext[0] = Label(self.frame_dict[col], text=Adate_datetext[0])
                Adate_datetext[0].grid(row=0, column=0)
                Adate_button[0] = ttk.Button(self.frame_dict[col], text=Adate_button[0], command=lambda: self._calendar(0, Adate_datetext))
                Adate_button[0].grid(row=1, column=0)
                blank = Label(self.frame_dict[col], text='')
                blank.grid(row=2, column=0)
                Adate_datetext[1] = Label(self.frame_dict[col], text=Adate_datetext[1])
                Adate_datetext[1].grid(row=3, column=0)
                Adate_button[1] = ttk.Button(self.frame_dict[col], text=Adate_button[1], command=lambda: self._calendar(1, Adate_datetext))
                Adate_button[1].grid(row=4, column=0)
                
        
        # set initial states of checkbuttons
        for self.check_list in self.check_dict.values():
            for check in self.check_list:
                check.state(['!alternate'])
        
        # Running the main loop
        root.protocol("WM_DELETE_WINDOW", lambda: self._close_window(root))
        root.mainloop()