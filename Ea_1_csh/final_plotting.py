import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats as spt
import os
import time 

butane = 'Butane'
decane_sarthy = 'decane_sarthy'
dodecane = 'Dodecane'
dodecane_sarthy = 'dodecane_sarthy'
Heptane_sarthy = 'Heptane_sarthy'
Hexane = 'Hexane'
Nonane_sarthy = 'Nonane_sarthy'
octane_sarthy = 'octane_sarthy'
pentane = 'Pentane'
propane = 'Propane'
undocane_sarthy = 'undocane_sarthy'
heptane = 'Heptane'
# folder_list = [butane,decane_sarthy,propane,Hexane,dodecane,dodecane_sarthy,Heptane_sarthy,Nonane_sarthy,octane_sarthy,pentane,heptane]
folder_list = [butane,Hexane,pentane,propane,heptane]




def temp_ID(foldername1):
    '''
    It will find the ignition delay and temp from the 
    Flamemaster format 
    '''
    #result 
    data =  pd.read_csv('./'+str(foldername1)+'/IgniDelTimesCHmax.dout',sep="\t")
    temp = []
    ID = []
    for i in range(1,data.shape[0],1):
        line = str(data.iloc[i,:]).split(' ') #reading line
        
        ID_time = line[4].split('\n')[0] #sepearting ID

        #TEMP SEPERATED
        Temp = str(line[5].split('(')[1])
        Temp = Temp.split(',')[0]
        
        ID.append(float(ID_time))
        temp.append(1000/float(Temp))
    return ID,temp

def regression(temp,ID):
    '''
    Regression form the given the limits
    '''
    # #regression
    #tau =  exp (Ea/R * 1/T)
    #log(tau) = Ea/R * 1/T
    slope, intercept, r_value, p_value, std_err = spt.linregress(temp,np.log(ID))
    print('std_err: ', std_err)
    print('p_value: ', p_value)
    print('r_value: ', r_value)
    print('intercept: ', intercept)
    print('slope: ', slope)
    return intercept, slope


def run_code(file_tag,dir_name,analysis_type='Full'):
    files = sorted(os.listdir('./'+str(dir_name)+'/'))
    
    #output of file
    Ea_by_R =  pd.DataFrame([])
    fuel_list = []
    intercepts_list =[]
    EaR_list =[]
    
    #dataframe for the activation and file
    '''#if folders are there'''
    # for i in range(len(folder_list)):
    #     ID , temp = temp_ID(folder_list[i])
    #     ID = ID[14:25]
    #     temp = temp[14:25]
    #     plt.semilogy(temp,ID,marker='o',label = '$Fuel = %s ,P=5atm , X_{Fuel}=1, X_{Oxi}=Stochio, X_{Ar}=Rest$'%folder_list[i])
    #     intercept,slope = regression(temp,ID)

    #     fuel_list.append(folder_list[i])
    #     intercepts_list.append(intercept)
    #     EaR_list.append(slope)

    #     x = np.linspace(np.min(temp),np.max(temp),100)
    #     y = np.exp(intercept + (x  * slope))
    #     # plt.semilogy(x,y,linestyle='dashed',label = 'Regression line %s $Ea/R=%f$' %(folder_list[i],slope))

    Fname = ['C_{3}H_{8}','n-C_{4}H_{10}','n-C_{5}H_{12}','n-C_{6}H_{14}','n-C_{7}H_{16}',
    'n-C_{8}H_{18}','n-C_{9}H_{20}','n-C_{10}H_{22}','n-C_{11}H_{24}','n-C_{12}H_{26}','n-C_{13}H_{28}',
    'n-C_{14}H_{30}','n-C_{15}H_{32}','n-C_{16}H_{34}']
    for i in range(len(files)):
        data  = pd.read_csv('./'+str(dir_name)+'/'+str(files[i]))
        if(analysis_type == 'Full'):
            ##for all the data points
            ################################
            # Removing data with zero rows #
            ################################
            data = data[data.iloc[:,1] != 0]
            temp = data.iloc[:,0]
            ID  = data.iloc[:,1]  

        elif(analysis_type == 'Half'):
            # For data points having higher temperature
            ID  = (data.iloc[13:25,1]) 
            temp = data.iloc[13:25,0] 

        ###########################################
        ######   Doing Simple regression ##########
        intercept,slope = regression(temp,ID)

        fuel_list.append(files[i])
        intercepts_list.append(intercept)
        EaR_list.append(slope)

        x = np.linspace(np.min(temp),np.max(temp),100)
        y = np.exp(intercept + (x  * slope))
        # plt.semilogy(x,y,linestyle='dashed',label = 'Regression line %s $Ea/R=%f$'%(str(i+8),slope))
        fuel_name = str(Fname[i])
        print('fuel_name: ', fuel_name)
        plt.rc('text',usetex=True)
        plt.semilogy(temp,ID,marker='.',label = '$%s$'%fuel_name)

        # plt.semilogy(x1,y1,linestyle='dashed',label = 'Regression line 1 $Ea/R=%f$'%slope1)

    Ea_by_R['Fuel'] = pd.Series(fuel_list)
    Ea_by_R['Ea/R'] = pd.Series(EaR_list)
    Ea_by_R['intercept'] = pd.Series(intercepts_list)
    Ea_by_R.to_csv('Ea_by_R_'+str(analysis_type)+'_'+str(file_tag)+'.csv',index=False)




    #plottinhg 
    # plt.xlim(np.min(temp),np.max(temp))
    # plt.ylim(np.min(ID),np.max(ID))
    fontsize_ = 19
    legeng_font = 14
    
    plt.rc('text',usetex=True)
    # plt.figure(figsize=(20,10)) 
    plt.title("Ignition delay plot of alkanes $C_3H_{8}$ to $n-C_{16}H_{34}$ \n [P=$"+str(file_tag)+"$atm , $\chi_{Fuel}=1\%, \chi_{Ar}=$Remaining, \n $ \hspace{1cm} \chi_{O_{2}}=$According to stoichiometric ]",fontsize = fontsize_)
    plt.xlabel('1000/T [K]',fontsize = fontsize_)
    plt.ylabel('Ignition delay (s)',fontsize = fontsize_)  
    plt.xlim(0.4,2.0)
    plt.xticks(fontsize=fontsize_, rotation=0)
    plt.yticks(fontsize=fontsize_, rotation=0)
    # plt.legend(loc = 'best',fontsize = '5', title = 'Hey there', title_fontsize = 'fontsize_')
    plt.legend(labelspacing=0.2,loc = 'lower right',fontsize = legeng_font,ncol=2,title_fontsize=legeng_font)
    # plt.savefig('./plots/combined.eps', dpi=1000)
    plt.tight_layout()
    plt.savefig('./plots/combined_'+str(analysis_type)+'_'+str(file_tag)+'.eps', figsize=(18,13),dpi=600,orientation ='landscape')
    plt.close('all')
    # plt.show()
    # plt.title(r"Ignition delay plot of alkanes $C_3H_{8}-C_{16}H_{34}$ \\ $[P="
    #     +str(file_tag)+
    #     r"$atm , $X_{Fuel}=1\%, X_{Ar}=$Remaining, \\ "
    time.sleep(2)
if __name__ == "__main__":
    #################################################################
    ######################    INPUT     #############################
    #################################################################
    file_tag = 10 #define pressure here
    dir_name = 'chemkin_all_'+str(file_tag) #define directory you want to analyze
    #############        Output file name         ###################
    analysis_type = 'Full' #Full or Half ... which stand for higher temperature
    #################################################################
    #################################################################
    run_code(file_tag,dir_name,analysis_type)
