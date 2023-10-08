import numpy as np
import pandas as pd



class BrainEnergy:


    def __init__(self, filename = 'Please Enter File Name', link_type= 'weighted' , windows_size = 20) -> None:
         self.filename = filename
         self.data = self.data_reader()
         self.link_type = link_type
         self.ws = windows_size
         pass


    def data_reader(self):
            file_path = self.filename

            # Read the file and store non-comment lines as a list
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if not line.startswith('#')]

            data55=[]
            for line in lines:
                values = line.strip().split('\t')
                # Append the values to the data list
                data55.append(values)
            # Convert the list of strings to a NumPy array of floats
            dff = pd.DataFrame(data55)
            data = dff.iloc[0:, 0:]
            #data = pd.DataFrame(np.array([list(map(float, line.split())) for line in lines]))
            return data

    def correlation(self, threshold=0):
        data = self.data.astype(float)
        co = data[0:len(data)].corr(method='pearson')
        co = pd.DataFrame(co)
        if self.link_type == 'sign':
             signnet = co.applymap(lambda x: 1 if x > threshold else (-1 if x < -threshold else 0))
             corr = signnet.values
        elif self.link_type == 'weighted': 
             corr = np.array(co)
        return corr
    
    def energy(self):
        """
        data = self.data.astype(float)
        corr = self.correlation()
        energy_dict = {}
        time_point = len(data)
        num_state = len(data[:1].values[0])
        for row in range(1,time_point):
            ene = 0
            count = 0
            for value in range(num_state-1):
                for i in range(value+1, num_state):
                    count += 1
                    ene += corr[value][i] * data[row-1:row][value] * data[row-1:row][i]
            energy_dict[f'{row}th time-point'] = float(ene / count)
        return energy_dict
         """
        
        data = self.data.astype(float)
        corr = self.correlation()
        energy_dict = {}
        time_point, num_state = data.shape
        data_array = data.values
        for row in range(1, time_point):
            ene = 0
            count = 0
            for value in range(num_state-1):
                for i in range(value+1, num_state):
                    count += 1
                    ene += corr[value, i] * data_array[row-1, value] * data_array[row-1, i]
            print(count)
            energy_dict[f'{row}th time-point'] = float((ene*-1) / count)
        return energy_dict
            
              
              
    
