import numpy as np
import pandas as pd
import matplotlib as mtp
from config import spaceFootfallData
from config import footfallMatrix



def generateMatrix():	
	df_test = pd.read_csv(spaceFootfallData)
	c1=df_test[df_test.columns[0]][:]
	c2=df_test[df_test.columns[1]][:]
	c3=df_test[df_test.columns[2]][:]
	cfinal=(c1+c3+c2)/3
	cfinal[489999]=255.0
	cfinal=cfinal.reshape([700,700])   
	mat=np.zeros([20,20])
	for i in xrange(20):
		for j in xrange(20):
			val=0
			for k in xrange(70/2):
				for l in xrange(70/2):
					val=val+cfinal[k+35*i][l+35*j]
			mat[i][j]=val/(35*35)
	mat=255-mat
	np.savetxt(footfallMatrix, mat, delimiter=",")



if __name__ == "__main__":
	generateMatrix()


