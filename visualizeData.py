# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:39:33 2017

@author: Steve
"""


# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importData import getData
import statsmodels.api as sm
import statsmodels.formula.api as smf


frizData = getData('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\friz_clean')
    
navData = getData('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\nav_clean')

# <codecell>

def removeHighRTs(dv,data):
    rtThresh = 2*np.std(data[dv])
    rtMean = np.mean(data[dv])
    dataThresh = data.loc[data[dv] < (rtMean + rtThresh)]
    dataThresh = dataThresh.loc[dataThresh[dv] > 0]
    return dataThresh

def removeWrongAnswers(dv,data):
    dataCorrect = data.loc[data[dv] == 1]
    return dataCorrect


def renameFactorLevels(data,friz_or_nav):
    
    
    data['condition'] = friz_or_nav
        
        
    prompts = sorted(data.prompt1.unique())
    stims = sorted(data.stim1.unique())
    
    new_stims = ['far_left','far_right','near_left','near_right']

    if friz_or_nav == 'friz':    
        new_prompts = ['Away','Left','Right','Home']
    else:
        new_prompts = ['Away','Home','Left','Right']

    for i in range(len(prompts)):
        data = data.replace(prompts[i],new_prompts[i])
        data = data.replace(stims[i],new_stims[i])
        
    return data


def newFactorPrompts(row):
    if row['prompt1'] == 'Home' or row['prompt1'] == 'Away':
        return 'abs'
    else:
        return 'rel'
    
def newFactorStims(row):
    if row['stim1'] == 'near_right' or row['stim1'] == 'near_left':
        return 'near'
    else:
        return 'far'
    



frizData = renameFactorLevels(frizData,'friz')
navData = renameFactorLevels(navData,'nav')

frizData['stimLoc'] = frizData.apply(lambda row: newFactorStims(row),axis=1)
navData['stimLoc'] = navData.apply(lambda row: newFactorStims(row),axis=1)

frizData['promptType'] = frizData.apply(lambda row: newFactorPrompts(row),axis=1)
navData['promptType'] = navData.apply(lambda row: newFactorPrompts(row),axis=1)


frizDataThresh = removeHighRTs('Trials_responsert',frizData)
navDataThresh = removeHighRTs('Trials_responsert',navData)

data = frizDataThresh.append(navDataThresh)
data = removeWrongAnswers('Trials_responsecorr',data)

unthreshed_data = frizData.append(navData)
# <codecell>
sns.boxplot(x='prompt1',y='Trials_responsert',data=data)
plt.show()

# <codecell>
sns.set_style('ticks')
ax = sns.factorplot(x = "promptType", y = "Trials_responsert", data = data, hue = "stimLoc", palette=['red','blue'],
                    kind = "point", size = 8,col='condition')


ax = sns.factorplot(x = "prompt1", y = "Trials_responsert", data = data, hue = "stim1", palette=['red','dodgerblue','blue','salmon'],
                    kind = "point", size = 8,col='condition')


# <codecell>
factor_order = ['The force is away.','The force is home.','The force is backhand.','The force is forehand.',
'Go away. ','Go home.','Go left. ','Go right. ']

ax = sns.factorplot(x = "prompt1", y = "Trials_responsert", data = unthreshed_data, hue = "stim1", palette=['red','green','blue','yellow'], 
                    kind = "point", size = 8, order=factor_order,col='Trials_responsecorr')

# <codecell>




