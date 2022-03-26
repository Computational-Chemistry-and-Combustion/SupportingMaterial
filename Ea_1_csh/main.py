import pandas as pd
import matplotlib.pyplot as plt
from final_plotting import *
from generatePlot import *

pressure_conditions = [5,10]
# analysis_type = ["Full","Half"]
analysis_type = ["Full"]
#################################################################
######################    INPUT     #############################
#################################################################


## Generate the regression fit for 5 and 10 atm simulation data for each fuel
## After generating Ea_R  for all fuels, Find
coef_data = pd.DataFrame([]) #final coef dataset

for i in range(len(pressure_conditions)):
    for j in range(len(analysis_type)):    
        file_tag = pressure_conditions[i] #define pressure here
        dir_name = 'chemkin_all_'+str(file_tag) #define directory you want to analyze
        #############        Output file name         ###################
        #analysis_type = Full or Half ... which stand for higher temperature
        #################################################################
        #################################################################
        run_code(file_tag,dir_name,analysis_type[j])

        Ea_R_data = pd.read_csv('Ea_by_R_'+str(analysis_type[j])+'_'+str(file_tag)+'.csv')
        Ea_R_data['Fuel(C)'] = Ea_R_data['Fuel'].str.split('_').str[0].str[1:].astype(int) #from file name taking fuel length
        Ea_R_data['Bonds'] = (Ea_R_data['Fuel(C)']-2)*2
        Ea_R_data = Ea_R_data.rename(columns={"Ea/R": "Simulation_"+str(file_tag)+'_'+str(analysis_type[j])+"_Ea_R"})
        print(Ea_R_data)
        
        coef_data['Fuel(C)'] =  Ea_R_data['Fuel(C)'] 
        coef_data['Bonds'] = Ea_R_data['Bonds']
        coef_data["Simulation_"+str(file_tag)+'_'+str(analysis_type[j])+"_Ea_R"] =  Ea_R_data["Simulation_"+str(file_tag)+'_'+str(analysis_type[j])+"_Ea_R"] 

coef_data.to_csv('coeff.csv',index=False)

generatePlot()