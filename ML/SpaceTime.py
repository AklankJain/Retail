
# coding: utf-8

# In[ ]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[11]:

s = pd.read_csv("./Time/1.csv",header = None,names = ['x','y','z','a'])
s


# In[ ]:

area = np.array(s.z)
time = np.array(s.a)
#area = [17,23]
#plt.plot(dist,time,'*')
plt.plot(area,time,'o')
plt.show()
area
time

