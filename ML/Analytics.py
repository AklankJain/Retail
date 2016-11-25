
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import spaceData
from config import footfallMatrix



def analytics():
	footfall = pd.read_csv(footfallMatrix,header=None,names = [i for i in xrange(20) ])
	
	area = pd.read_csv(spaceData,header=None,names =  [i for i in xrange(20) ])
	 
	arr2=np.array(footfall)
	arr2=arr2.reshape(400,1)
	
	arr1=np.array(area)
	arr1=arr1.reshape(400,1)
	
	arrfin=np.concatenate((arr1,arr2),axis=1)
	
	arrfin1=arrfin[arrfin[:,0].argsort()]

	#for i in xrange(400):
	#	value=arrfin1[i,0]
	#	j=i
	#	while j!=400 and arrfin[j,0]==value:
	#		j=j+1
	#	j=j-1
	#	arrfin1[i:j,]=arrfin1[arrfin1[i:j,1].argsort()]
	#	i=j+1
	
	area=arrfin1[:,0]
	footfall=arrfin1[:,1]
	z=np.polyfit(area,footfall,2)
	print "Correlation Cofficient : \n",np.corrcoef(area,footfall)
	print "\nCofficient of the Polynomial\n",z
	
	p3=np.poly1d(z)
	
	
	plt.axis((0,5.5,-10,80))
	plt.plot(area, footfall, 'bo-', area, p3(area), 'ro--')
	plt.show()

if __name__=="__main__":
	analytics()

