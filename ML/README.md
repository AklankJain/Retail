#Machine Learnig Documentation

## Description
Finds the Relation between space-time and space-footfall and plot them.

## Space-Footfall
Footfall signifies the average number of people present in a location during a period of time.

The Heatmap generated in image-processing part gives the information about footfall.The footfall data is merged with the
field-map to obtain the image.

![0boxgrid](https://cloud.githubusercontent.com/assets/16621282/20865699/86123438-ba3f-11e6-8597-7718f0487b7f.png)

## Grid Apply
We devided the image into 20*20 smaller image grids.

![20boxgrid](https://cloud.githubusercontent.com/assets/16621282/20865739/8f22638a-ba40-11e6-8eea-b34d4aea7dea.jpg)

## Final Visualization
analytics.py analyzes the grids and assigns footfall wight for every small grids.After getting the grids weights we simply plot 
grid footfall weigts to space area data.

Similarly spacetime.py plots the space data with average spending time.
