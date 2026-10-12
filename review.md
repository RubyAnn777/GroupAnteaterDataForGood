## Ruby doc für Seb draft analysis

New mining (additions) 	Mining area this year minus last year, in hectares (ha). 1 ha = 100 × 100 m.

here we need to check what happens with mines that are reused in a way (abandoned and then picked up again). We would "hope" that these are shown in expansion in ha mined but to me its not 100% clear that this is the case. 

in general we need to say that we cannot measure whether all mines have been abandoned or not.

measure deforestation in legal areas! Did they just go the the corridor??

look at monthly data (better for econometrics)

Sources claim that the people just went across the road (that mining in the legal zone spiked) - can we verify? also then we need to claim that for the region itself and very vulnerable populations this is a successful operation. However if mercury is used in the legal corridor then this is a problem for biodiversity and human health even outside (understanding how far it travels is essential).

Also I think we should include the social aspect of the operation. The livelihood of the miners. (there is a cost calculator we could use).


Momentan core = buffer zone comparison ABER displacement very likely also into legal corridor zone (see Conservation letter paper) - klar differenzieren

covid did not affect all zones the same! (enforcement budget cuts)


content wise - descriptive as main and with causal analysis we can show parallel trends violated for the two buffer zones (+ Amarakaeri is actually not a control lmao), meaning we needed to find another one
I would suggest we add the layer of checking for other enforcement operations in the zones! So we can control/compare for intensity.

Clearly mark whether mining is in "legal corridor" rather than saying "rest of madre de dios". We need a clearer distinction here to make claims about effectiveness of the placement of enforcement operations.

Frame Brazil as the case post-covid with more consistent effects hopefully seen in future. Make sure we highlight the differences in enforcement.
Also -> interoceanic highway as a limitation (displacement ease might not be the same everywhere). 

We need to thik about the timing as well in general -> restauration is itself an enforcement program. before there was also enforcement. (more of a mental note)

displacement shows that we need stronger regulation also in legal areas. aber what exactly would that look like? (we need to check the legal framework for mining in the legal corridor a bit more). 


in the literature there are also "anti-corruption" measures mentioned in the operation. Check what this means.

double check how the borders of all zones are drawn - more granular = better (flags for la pampa, buffer zone, legal corridor, indigenous territories, protected areas etc. would be incredible). Use AMW if available.

Method: for Amarakaeri / legal corridor - should we just check if there is a stat significant difference? Like increase wise i mean?

In general it is very very important to check that the geospatial data lays on the same grid. And even more so that the boundaries are defined in the same way!


For my suggested method (8)
no intervention is maybe a too strong rule (esp. because if its a buffer zone there will be some kind of enforcement). It needs to be somewhat comparable in magnitude I would say. I think for Peru we should have data available. 
In general the control group looks slay. If we can get monthly/quartetly data that would be insane

We should also study the changes of the zones over time (when was the legal corridor established, what about the buffer zones etc.)

Concrete Feedback
graph in 4: the middle one is not very intutive to read ("rest" is not showing us anything tbh)
graph in 5: shows clearly in 2020 as the amarakaeri buffer zone is also receiving treatment, the increase "reverses" slightly.
can we find an event that explains the spike in mining activity in 2017 in the buffer zone? It follows a crazy dip - the pattern is a bit weird.

Edit: i found one “In 2017, a line was crossed: extortion increased, they started calling themselves ‘Security,’ and they brought in their own machines to extract gold. During the pandemic, they took over all extraction sites, and starting in 2022, they began to show themselves openly in public,” https://forbiddenstories.org/with-control-of-la-pampas-lawless-mines-the-guardianes-de-la-trocha-gang-imposes-its-own-rule/

8 The two satellite products disagree on 2019. AMW still sees a lot of new mining in Tambopata in 2019; MapBiomas sees little. Shares, not hectares, are compared here.
We need to take care of that in the sense that we at least must use the same product for all areas. (I would suggest AMW because it is more granular and has a better resolution). Make more robustness checks comparing data sources.

9 For the synthetic twin we need to validate if this actually is a good idea overall. Maybe here we can also use non-peruvian areas that have no enforcement in that period of time as an expansion of the current pool used. Maybe in this context synthetic control is not a method match at all.  

for 10 where did the mining go
clearly outline the legal corridor 
show the percentage of mining happening in illegal territory over time as a descriptive exeercise.


Qualitative assessment (readings - yellowness; tents; drone footage; interviews) Yellowness is a good indicator when using satellite data to see if the mines are abandoned or not.



---------------------------------------------------------------------------------------------------------------------------------------
AI generated nicer version:
---------------------------------------------------------------------------------------------------------------------------------------

1. Econometrics & Methodology
Control Groups & Parallel Trends: The current core vs. buffer zone comparison violates the parallel-trend assumption. Furthermore, the Amarakaeri buffer zone is not a valid control group because it also receives treatment in 2020  (expansion of the Mercury operation)

Difference-in-Differences (DiD): For Amarakaeri and the legal corridor, we should apply a proper Difference-in-Differences specification to test whether there is a statistically significant difference in the growth/increase trajectory.

Displacement Effects: We must clearly differentiate and account for displacement (leakage), as mining activity likely spills over into the legal corridor zone (see Conservation letter paper). The Interoceanic Highway serves as a logistical limitation/facilitator, meaning the ease of displacement is not uniform everywhere. Clearly outline the corridor! Understand whether these boundaries changed over time

Enforcement Intensity: We should incorporate other enforcement operations in the zones as control variables so we can control/compare for enforcement intensity.

Covid-19 Impact: The pandemic did not affect all zones equally due to differing budget cuts for enforcement agencies across regions. Brazil could be framed as a post-Covid case study, with more consistent effects hopefully observable in the future. Highlight differences in enforcement between Peru and Brazil. Also does not have the interoceanic highway effect (which might cause displacement to be huge)

2. Geospatial & Satellite Data
Data Consistency (AMW vs. MapBiomas): The two satellite products disagree on 2019 data (Amazon Mining Watch sees a lot of new mining in Tambopata; MapBiomas sees little, comparing shares rather than hectares). Action: We must consistently use the same product across all areas (AMW is recommended due to higher granularity and resolution) and conduct robustness checks comparing data sources.

Grid and Boundary Alignment: It is critical that geospatial data overlays the exact same grid and that boundaries are defined identically. We need consistent flags for La Pampa, buffer zones, the legal corridor, indigenous territories, protected areas, etc. (use AMW if available).

Temporal Resolution: Monthly or quarterly data should be used where possible, as it is much better suited for econometric models than annual data.

3. Substantive Mechanisms & Contextual Factors
Legal vs. Illegal Distinction: We need a clear distinction for whether mining is occurring in the "legal corridor" rather than vaguely referring to the "rest of Madre de Dios." We should track the percentage of mining happening in illegal territory over time. AMW has a matrix with a likelihood of illegality that can be used to classify mining activity. Also here make sure it maps onto the existing data we have

Social and Health Aspects: Include the social dimension, specifically the livelihoods of the miners (using a cost calculator). Additionally, account for mercury use: if mercury is used in the legal corridor, it threatens biodiversity and human health even outside the corridor (understanding its spread is essential). Not in the models but in recommendtions we should include local enforcement, legal zone enforcement, tracking systems, evaluating mercury travel in water, placement of enforcement operations as key measure, social cost (livelihoods of miners).

Anti-Corruption & Timing: Check literature regarding "anti-corruption" measures mentioned in the operation. Also, keep in mind the overall timeline: restoration is itself an enforcement program, and enforcement existed prior to the main intervention. I think we should have data on how much enforcement was happening before 2017. Why was previous enforcement not effective? Even before 2017 there was a lot going on

4. Specific Feedback on Graphics and Points (Draft References)
Graph 4: The middle section is not intuitive to read; the "rest" category does not provide useful insight.

Graph 5: Clearly shows that in 2020, when the Amarakaeri buffer zone also receives treatment, the upward trend in mining "reverses" slightly.

Context for the 2017 Spike: We can explain the unusual dip followed by a massive spike in 2017 within the buffer zone using qualitative evidence:

"In 2017, a line was crossed: extortion increased, they started calling themselves 'Security,' and they brought in their own machines to extract gold. During the pandemic, they took over all extraction sites, and starting in 2022, they began to show themselves openly in public." (Source: Forbidden Stories article) Also there is some informaton about mercurcy use bans (and consequent price spikes leadin to potentially the expansion of the black market by the same gangs) - we could check if we can find more information on this. more of a sidenote

Point 8: Address the 2019 satellite product discrepancies (AMW vs. MapBiomas) by using a single, unified data source and running robustness checks.

Point 9 (Synthetic Twin / SCM): Validate whether the synthetic twin approach is a solid choice overall. Consider incorporating non-Peruvian areas that experienced no enforcement during that time period. Note that a strict "no intervention" rule might be too strong (buffer zones always have some enforcement), so the donor pool needs to be comparable in magnitude.   

Point 10 (Where did the mining go?): Clearly outline the legal corridor and visualize the percentage of mining taking place in illegal territory over time.

Qualitative Assessment: Back up the findings with qualitative observations such as water discoloration (yellowness), tents, drone footage, and interviews.

---------------------------------------------------------------------------------------------------------------------------------------
## Response (Claude, 12 Oct 2026): the two satellite products that disagreed
---------------------------------------------------------------------------------------------------------------------------------------

**Bottom line:** the disagreement is still there, we checked it, and it is mostly a measurement difference, not two opposite realities.

**What disagreed at first (overnight run, 10-11 Oct):**
- MapBiomas (course tables) showed new mining in "rest of Madre de Dios" **rising** after 2019.
- Amazon Mining Watch (AMW) showed new mining in the legal corridor **falling** (2019-21 vs 2022-24).
- We then refused to claim displacement into the corridor.

**What we changed (plan v2):**
1. **One backbone, one grid:** all zone numbers now come from the MapBiomas Peru Collection 4 *rasters*, cut to our own zones (La Pampa, corridor across the road, rest of corridor, communities, reserves...). The raster reproduces the published totals (Tambopata buffer zone 2025: 20,716 vs 20,730 ha).
2. **AMW became a robustness check on the same zones** (`code/v2_extra.py`, E1), never subtracted from MapBiomas.
3. **We split "new mining" into first-time mining and returns to old pits,** because the two products count different things.

**Is the disagreement still there? Yes, in one place:**

| ha/yr | MapBiomas 2019-21 -> 2022-25 | AMW 2019-21 -> 2022-25 |
|---|---|---|
| Rest of mining corridor | 4,038 -> 7,638 (up) | 14,848 -> 9,967 (down) |
| Corridor across the road | 463 -> 538 | 1,009 -> 650 |
| La Pampa sector | 722 -> 987 | 936 -> 1,043 (agree) |

- Both agree on the *direction of the move across the road*: AMW's north-of-road share in the La Pampa longitudes went from 68% (2019) to 87% (2021).
- Across all zone-years, the two series correlate at 0.83.

**Have we checked why? Yes** (`code/v2_products_check.py`, numbers `pc_*`):
- AMW flags a 480 m square **once**, in the year mining first appears, and never counts it again. MapBiomas counts every new 30 m pixel.
- **Two-thirds of MapBiomas's first-time mining in the corridor in 2022-25 (68%) lies inside AMW squares flagged in an earlier year** (79% in the corridor across the road). AMW cannot count that infill as new.
- So AMW "falls" in a maturing mining area while mining keeps filling in. The corridor's AMW-flagged share of land rose from 12% (2018) to 31% (2025): the squares are filling up.

**What we claim now:** the move across the road (both products agree); the corridor's growth after 2021 (MapBiomas, with the AMW caveat stated). We do not use AMW hectares for trends inside already-mined areas.
