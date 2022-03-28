import pandas as pd
import numpy as np

df0 = pd.read_csv('./Ignition_delay_comparison/ID_comparison_external_cluster_0.csv')
df1 = pd.read_csv('./Ignition_delay_comparison/ID_comparison_external_cluster_1.csv')
df2 = pd.read_csv('./Ignition_delay_comparison/ID_comparison_external_cluster_2.csv')

cols = ['Relative Error']
df0 = df0[cols]
df1 = df1[cols]
df2 = df2[cols]

df = pd.concat([df0,df1,df2])

# print(df0.describe(percentiles=[.1,.2,.3,.4,.5,.6,.7,.8,.9,1]))
# print(df1.describe(percentiles=[.1,.2,.3,.4,.5,.6,.7,.8,.9,1]))
# print(df2.describe(percentiles=[.1,.2,.3,.4,.5,.6,.7,.8,.9,1]))

print(df.describe(percentiles=[.2,.4,.6,.8,1]))
