import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import copy 

###########################################
##############   Input   ##################
###########################################

def generatePlot():
    data = pd.read_csv('coeff.csv')

    #removing propane data
    data = data[data['Fuel(C)'] != 3]
    ############################################################
    '''
    To do regression against C_SH and Ea/R
    Inverse of data['Bonds'] has been taken and 
    after that regression has been obtained which 
    gives fit of,
    Ea/R = \beta_0 + \beta_1 / C_SH
    '''

    #Experimental x and y data points    
    xData = 1/data['Bonds']  #inverted just for finding the fit 
    # xData = data['Bonds']  #inverted just for finding the fit 
    error_com_data = copy.deepcopy(data)
    error_com_data['1byC_SH'] = xData

    for  i in range(2,data.shape[1]): #second column to last column 
        yData = data.iloc[:,i]
        
        import statsmodels.api as sm
        X = sm.add_constant(xData) #added constant 
        print(X)
        print(yData)
        model = sm.OLS(yData,X)
        results = model.fit()
        parameters = results.params
        beta0 = list(parameters)[0]
        beta1 = list(parameters)[1]

        print(results.summary() )
        
        #x values for the fitted function
        xFit = np.arange(0,0.5, 0.01)
        error_com_data[data.columns[i]+'_pred'] = results.predict(X)
        error_com_data[data.columns[i]+'_relErr'] = (np.abs(error_com_data[data.columns[i]+'_pred'] - error_com_data[data.columns[i]])/error_com_data[data.columns[i]])*100
        mean_rel_error = error_com_data[data.columns[i]+'_relErr'].mean()
        max_rel_error = error_com_data[data.columns[i]+'_relErr'].max()
        min_rel_error = error_com_data[data.columns[i]+'_relErr'].min()
        
        R2 = results.rsquared
        pressure = str(data.columns[i]).split('_')[1] ##will give pressure value
        fontsize = 17
        #Plot the fitted functions
        plt.rc('text',usetex=True)
        #Plot experimental data points
        plt.plot(1/data['Bonds'], yData, 'bo', label=r'$\frac{E_a}{R}$ by simulation')
        plt.plot(xFit, beta0+beta1*xFit, 'g-', label=r'${C_{SH}}$ fit')
        plt.title(r'Regression fit of simulated $Ea/R$ vs $1/C_{SH}$ ',fontsize=fontsize)
        plt.xlabel('1/Number of $C_{SH}$ bonds',fontsize=fontsize)
        plt.ylabel('$E_a/R$',fontsize=fontsize)
        plt.legend(loc='best',fontsize=fontsize)
        text = r'Pressure : '+str(pressure) + ' atm \n $R^2$ : '+str(format(R2, '.4f')) + '\n'r' $\beta_0$ : '+str(format(beta0, '.4f')) + '\n'r'$\beta_1$ : '+str(format(beta1, '.4f')) \
            + '\n'r'Mean RE : '+str(format(mean_rel_error, '.2f') +'$\%$') + '\n'r'Max RE : '+str(format(max_rel_error, '.2f')+'$\%$') + '\n'r'Min RE : '+str(format(min_rel_error, '.2f')+'$\%$')
        
        # position text absolutely at specific pixel on image
        plt.text(380, 150, text,ha='center', va='center',transform=None,fontsize=fontsize)
        # plt.xticks(np.arange(min(xFit_inv), max(xFit_inv)+1, 2),fontsize=fontsize)
        # plt.yticks(fontsize=fontsize, rotation=0)
        plt.tight_layout() 
        plt.savefig('./plots/comparision_1_csh_'+str(data.columns[i])+'.eps', figsize=(18,13),dpi=600,orientation ='landscape')
        plt.show()
        plt.close('all')

    
    
    error_com_data.to_csv('./res_error_compare/predicted_coef.csv')

if __name__ == "__main__":
    generatePlot()