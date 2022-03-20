import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

###########################################
##############   Input   ##################
###########################################

def generatePlot():
    data = pd.read_csv('coeff.csv')

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

    for  i in range(2,data.shape[1]): #second column to last column 
        yData = data.iloc[:,i]
        
        import statsmodels.api as sm
        X = sm.add_constant(xData) #added constant 
        model = sm.OLS(yData,X)
        results = model.fit()
        parameters = results.params
        beta0 = list(parameters)[0]
        beta1 = list(parameters)[1]

        print(results.summary() )
        
        #x values for the fitted function
        xFit_inv = np.arange(2,30, 0.01)

        R2 = results.rsquared
        pressure = str(data.columns[i]).split('_')[1] ##will give pressure value
        fontsize = 19
        #Plot the fitted functions
        plt.rc('text',usetex=True)
        #Plot experimental data points
        plt.plot(data['Bonds'], yData, 'bo', label=r'$\frac{E_a}{R}$ by simulation')
        plt.plot(xFit_inv, beta0+beta1/xFit_inv, 'g-', label=r'$\frac{1}{C_{SH}}$ fit')
        plt.title(r'Regression fit of simulated $Ea/R$ vs $C_{SH}$ ',fontsize=fontsize)
        plt.xlabel('Number of $C_{SH}$ bonds',fontsize=fontsize)
        plt.ylabel('$E_a/R$',fontsize=fontsize)
        plt.legend(loc='best',fontsize=fontsize)
        text = r'Pressure : '+str(pressure) + ' atm \n $R^2$ : '+str(format(R2, '.4f')) + '\n'r' $\beta_0$ : '+str(format(beta0, '.4f')) + '\n'r'$\beta_1$ : '+str(format(beta1, '.4f'))
        # position text absolutely at specific pixel on image
        plt.text(350, 170, text,ha='center', va='center',transform=None,fontsize=fontsize)
        plt.xticks(np.arange(min(xFit_inv), max(xFit_inv)+1, 2),fontsize=fontsize)
        plt.yticks(fontsize=fontsize, rotation=0)
        plt.tight_layout() 
        plt.savefig('./plots/comparision_updated_'+str(data.columns[i])+'.eps', figsize=(18,13),dpi=600,orientation ='landscape')
        # plt.show()
        plt.close('all')


if __name__ == "__main__":
    generatePlot()