import pypyodbc
import pandas as pd

# output consistency class
class OPConsistency:
    def __init__(self, DB_PATH, DB_PASSWORD, hue=None, filters={}, Adate='1900-01-01', Adate2='2025-01-01', error=0):
        self.DB_PATH = DB_PATH
        self.DB_PASSWORD = DB_PASSWORD
        self.error = error
        self.filters = filters
        self.Adate = Adate
        self.Adate2 = Adate2
        self.hue = hue
    
    def _connect_to_db(self):
        '''connect to database and return connection'''
        new_connection = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;PWD=%s'%(self.DB_PATH,self.DB_PASSWORD)   
        conn = pypyodbc.connect(new_connection)
        return conn
    

    def _ref_to_df(self):
        # Create empty list to store conditions
        conditions = []

        # Add condition for gantry
        if 'Gantry' in self.filters:
            gantry_condition = "A.[MachineName] IN ({})".format(", ".join("'%s'" % g for g in self.filters['Gantry']))
            conditions.append(gantry_condition)
        
        if 'Energy' in self.filters:
            energy_condition = "A.[Energy] IN ({})".format(", ".join(str(e) for e in self.filters['Energy']))
            conditions.append(energy_condition)
        
        # Combine all conditions into a single WHERE clause
        where_clause = " AND ".join(conditions)
        print(where_clause)
        
        '''pull reference data from database and return dataframe'''
        sql =   '''
                Select A.Energy
                    , A.RefDose
                From OutputConsRef As A
                Inner Join (
                    Select Energy
                        , [MachineName]
                        , Max(RefDate) As MRefDate
                    From OutputConsRef
                    Group By Energy, [MachineName]) As B
                On A.Energy = B.Energy
                And A.[MachineName] = B.[MachineName]
                And A.RefDate = B.MRefDate
                {0}
            '''.format("WHERE " + where_clause if where_clause else "")
        
        print(sql)
        try:
            conn = self._connect_to_db()
            cursor = conn.cursor()
        except:
            cursor.close()
            conn = None # close database connection
            self.error='conn_error'
            return self.error
        try:
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()
            conn.commit()
        except Exception as e:
            print(str(e))
            cursor.close()
            conn = None # close database connection
            self.error='Ref_error'
            return self.error

        # convert reference data to pandas dataframe
        cols = ['Energy','RefGy']
        df_ref = pd.DataFrame(list(records), columns=cols)
        print(df_ref)
        return df_ref
    

    def _data_to_df(self):
        # pull output measurements from DB
        # Create empty list to store conditions
        conditions = []

        # Add condition for gantry
        if 'Gantry' in self.filters:
            gantry_condition = "A.[MachineName] IN ({})".format(", ".join("'%s'" % g for g in self.filters['Gantry']))
            conditions.append(gantry_condition)

        # Add condition for qnatry angle
        if 'Gantry angle' in self.filters:
            angle_condition = "A.[GA] IN ({})".format(", ".join(str(a) for a in self.filters['Gantry angle']))
            conditions.append(angle_condition)
        
        if 'Energy' in self.filters:
            energy_condition = "B.[Energy] IN ({})".format(", ".join(str(e) for e in self.filters['Energy']))
            conditions.append(energy_condition)
            
        if 'Electrometer' in self.filters:
            electrometer_condition = "A.[Electrometer] IN ({})".format(", ".join("'%s'" % g for g in self.filters['Electrometer']))
            conditions.append(electrometer_condition)
            
        if 'Chamber' in self.filters:
            chamber_condition = "A.[Chamber] IN ({})".format(", ".join("'%s'" % g for g in self.filters['Chamber']))
            conditions.append(chamber_condition)


        # Add condition for query_date and query_date2
        date_condition = "(A.Adate BETWEEN #{}# AND #{}#)".format(self.Adate, self.Adate2)
        conditions.append(date_condition)

        # Combine all conditions into a single WHERE clause
        where_clause = " AND ".join(conditions)
        print(where_clause)

        # Build SQL query with WHERE clause
        sql = '''
            SELECT  A.Adate
                , A.[MachineName]
                , A.[GA]
                , A.[Electrometer]
                , A.[Chamber]
                , A.[kQ]
                , A.[ks]
                , A.[kelec]
                , A.[kpol]
                , A.[NDW]
                , A.[TPC]
                , B.Energy
                , B.[R]
            FROM OutputConsSession A
            INNER JOIN OutputConsResults B
            ON A.Adate = B.ADate
            {0}
            '''.format("WHERE " + where_clause if where_clause else "")
        
        
        try: # connecting to the database
            conn = self._connect_to_db()
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
            self.error='Session_Results_error'
            return self.error
        finally: # executed regardless of whether an error has occured
            cursor.close()
            conn = None # close database connection

        # convert data to pandas dataframe
        cols = [
                'Date',
                'Gantry',
                'Gantry angle',
                'Electrometer',
                'Chamber',
                'kQ',
                'ks',
                'kelec',
                'kpol',
                'NDW',
                'TPC',
                'Energy',
                'R'
            ]
        df = pd.DataFrame(list(records), columns=cols)
        
        # calculate dose for output measurements
        df['RGy'] = df['R'] * df['kelec']*df['TPC']*df['ks']*df['NDW']*df['kpol']*df['kQ']*1.1/1000000000

        # round off timestamps to the nearest day for neater plotting of timeseries
        print('date:\n\n')
        print(max(df['Date']))
        df['Date'] = df['Date'].dt.floor('1d')
        df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')
        
        # drop unwranted columns
        df = df.drop(columns=['kQ','ks','kelec','kpol','NDW','TPC'])
        return df
    
    def mkdf(self): # the method called in OPConsistency_plot
        df_ref = self._ref_to_df()
        df = self._data_to_df()
        if self.error: return self.error
        
        # join reference dataframe to outputs dataframe
        try:
            df_join = df
            print(df_join)
            df_join = df_join.join(df_ref.set_index('Energy'), on='Energy')
        except: # dealing with errors while joining reference dataframe to outputs dataframe
            self.error = 'join_table_error'
            return self.error

        # calculate percent difference between measurements and reference doses
        df_join['Diff (%)'] = (df_join['RGy'].astype(float)-df_join['RefGy'])/df_join['RefGy']*100
        
        return df_join
