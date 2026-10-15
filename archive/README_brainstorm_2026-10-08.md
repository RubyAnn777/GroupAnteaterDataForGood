# Team brainstorm and early notes (from README.md, 8 Oct 2026; kept for the record)

## Conceptual draft (team brainstorm, 8 Oct)

*Working ideas from 8 Oct, kept for the record; superseded where `docs/PLAN_v3.md` differs.*

### Two exercises

**a) Displacement: figure out where the miners went.**
Measure how gold mining moves after enforcement. Look in the buffer zone and around the enforcement areas: which mines close, and where do new ones appear? The draft considers both enforcement cases on the card: Peru (Operation Mercurio, 2019) and Brazil (Yanomami territory, 2023).

**b) Difference-in-differences for each case, with a constructed/searched for control group.**

Here we can include the failed synthetic control approach and also use the unclean control in Brazil to show our efforts in establishing causality. 
### Control group selection

1. Get a map of all protected areas with their buffer zones.
2. Get the Amazon Mining Watch (AMW) polygons and build a panel by period and zone.
3. For every protected area, check whether its buffer zone has active mines, then whether there was active enforcement.
4. Pick controls that meet these criteria:

| Criterion | Why | How to check |
|---|---|---|
| Gold is present (rivers from the Andes) | Mining is possible at all | AMW polygons inside the zone |
| Far from the treated area | Avoid spillovers | Distance to La Pampa |
| Same country | Same regulation, same prices | Peru only |
| Geographically similar (climate, terrain) | Comparable conditions | Covariate data for treated and candidate zones |
| No enforcement at all | Otherwise it is not a control | Enforcement records (to be found) |

5. Find each treated zone's "geographic twin" with a matching algorithm, then run the DiD.

### Limitations noted so far

- Planes for transport?*(to clarify)*
- What exactly counts as "enforcement"?
- interoceanic highway (especially relevant for control group selection)
- mine abandonment and re-use (we cannot measure whether all mines have been abandoned or not)

### Other idea

Find out when gangs were active and when not, using relative prices of gold and coca as an instrumental variable.

### Still to fill in

- Descriptive exercise
- Control variables
- Graphs

### Draft structure for the presentation

Introduction - two fun facts about giant anteaters.

whats the difference between legal and illegal mining? 
regulations, impact, taxing etc etc. 
show the map and explain the zones (legal, illegal, buffer, protected, indigenous) and the enforcement operations.

Different manners of protection - what do they do? Protected vs indigenous territories -> (intro to SERNANP and their data) Cooperation with FENAMAD
How is illegality defined in data?
    Very High: Activity is occurring without a permit and within a protected area that doesn’t allow for any kind of resource exploitation
    High: Activity if occurring outside of any explicit concession for doing so
    Medium: Activity is happening within a concession, but active status could not be verified and/or concession doesn’t meet legal requirements
    Low: Activity is happening within active concession, but compliance with all requirements could not be verified

FZS impact and role + the zones they cover

Why illegality is an issue (social, environmental cost). Why it matters in other words.

Zone in on Peru and Brazil - explaining the initiatives 
(Operation Mercurio earls 2019 + The restauration plan since 2021)

Descriptives
-> how many of the areas are affected by mining today (indigenous + protected) (per country)
-> overall development of mining in studied area over time
-> comparison of mining activity before and after enforcement (also looking at buffer zone and close by areas)
**make sure we add the "number check" thing she wants us to do**

Trying to do causal analysis
-> failed synthetic control
-> looking for control 

Limitations and further research

Key limitation is that the enforcement is actually happening always somewhere in some unsystematic way. We need to find for the control a zone that has comparable levels of enforcement. Luckily in Peru its well done

Why was previous enforcement not effective? Even before 2017 there was a lot going on

Recommendations
local enforcement 
legal zone enforcement 
tracking systems
evaluating mercury travel in water
placement of enforcement operations as key measure
social cost (livelihoods of miners)
