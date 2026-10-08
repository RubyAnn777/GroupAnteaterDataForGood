# GroupAnteaterDataForGood
This is the final project of the Data for Good class of October 2026


2 exercises:
a) measure displacement of gold mining activity due to enforcement in Peru and Brazil (both enforcements are in the question)
*Figure out where the people went*

b) Dif in Dif for each case study - creating a control group for each enforcement


a)
Focus on displacement of gold mining activity due to enforcement in Peru and Brazil. Check in the buffer zone, around the enforcement areas, close mines and check for new mines



b)
Control group selection

First get a map of all protected areas with buffer zones

get the AMW polygons (panel structure by quarter and zone for Peru and Brazil)
for all protected areas, check if there are any active mines in the buffer zone !! then check whether there is active enforcement! check 

The control group should be selected based on the following criteria:

Gold is there -> river is there originating in the Andes (this is satisfied by checking whether a polygon is found inside the zone as the algorithm detects active mines along rivers only)
further away -> to avoid spillover
same country -> to avoid different regulations and gold prices etc.
Geographic similarity (same climate, terrain, etc.) -> get this data for our treated and potential control zones
Needs to not have enforcement at all

find geographic twin -> find sophisticated algorithm that does that

Then we run Dif in Dif

Limtiations
planes 
what does enforcement mean



Other idea: 

figure out when gangs were active and when they were not -> looka t relative prices of gold and coca (instrumental variable)



Descriptive exercise:


Control variables: 


Graphs: 



