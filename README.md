# North American Trade Visualization

An interactive web application visualizing 2024 North American trade data for U.S. states, created as a final project for ECON 1500 (Current Global Topics in Macroeconmics) at Brown University (Spring 2025).

## Project Overview

This project provides an interactive visualization of trade balances between U.S. states and their North American trade partners (Canada and Mexico). It allows users to:

- View current trade balances for each state through an interactive map
- Hover over states to see detailed import/export data
- Adjust a tariff slider to visualize the projected impact of different tariff rates on state trade balances

## Motivation

This project has twofold motivation, beside being a "current global topic in macroeconomics"
that well suited this course structure, it was also very topical at the time of it's creation,
as Donald Trump threatened, implemented, and then partially unimplemented universal tariffs on
Mexico and Canada. In this project, I sought to square the general political appeal of tariffs with my own observations and economic theory.

From my twenty years on this planet and personal interest in urbanism and society, it 
is clear that America's decline of manufacturing capacity has had pronounced effects on the lives of millions. We have seen huge externalities in the Rust Belt and certain New England cities, where the
social order has been almost completely decimated by the exodus of factory jobs. Cities such as
Lawrence, Massachusetts and Lowell, Massachusetts have been hard-hit by the closure of mills,
and have brought these once great cities into shells of their former selves. The effects are much
greater than the loss of industrial jobs, though, as these cities have become hotbeds of crime and
disorder, with little desire for individuals to move there and revitalize the economy. The effects
are even worse in certain Midwestern cities like Detroit, MI or Albany, NY.

These effects cannot be ignored only by saying: "tariffs are not economically efficient." There has to be more to examine. Pretending the problem does not exist will never yield a good solution.

I myself am from the Greater Boston area, and both from what I’ve read in the news and seen
personally, the last 10 years have brought tremendous growth and prosperity to the region. The
amount of high-quality, well-paying jobs across all sectors is gargantuan, particularly in spaces
like bio-tech, academia, medicine, technological and financial sectors. Even here in Rhode
Island, I feel that anyone with a good well paying job is commuting to Boston. Thus it seems that
increased globalization has not brought equal prosperity to different regions. The growth of the
technological sector has been concentrated in places like New York, Boston, and San Francisco,
bringing sky-high housing costs, yet other regions seem to have been left behind. The current
situation in Boston comes in stark contrast to the economic destruction that has befallen so many
Midwestern cities: urban decay, population decline, and social dysfunction have all but ruined
these cities.

With this project, I will bring the data to bear and see if there really is broad inequality in which states are benefitting from free trade. I seek to provide a small snapshot of trade with North America, and see whether or not certain states are being adversely affected. This is only a small project for one class, so I do not seek to understand all the social, political, and economic intricacies of United States foreign trade policy. I will only seek to bring the data to life and provide some light commentary on different states' trade relationships with Mexico and Canada. It should be noted that there is not enough data to draw any clear causal connections, and also that the state I provide as a counterexample to Michigan, Massaschusetts, has a sizeable trade deficit under *all* tariff regimes.



## Data Sources

The data for this project was obtained from:
- U.S. Trade Online (trade.gov)
//Need to find the specific dashboard and link
- [List any other data sources you used]

trade.gov has very granular data (including the types of exports (commodities, steel, etc)), which 
could be used to make a much more granular model

All data is from 2024 and represents imports and exports between U.S. states and Canada/Mexico.

## Implementation Details



### Technologies Used
- Python
- Streamlit (for web application framework)
- Plotly (for interactive visualization)
- Pandas (for data manipulation)

### Tariff Impact Model
<! --- SIMPLE MODEL ---!>

The trade impact projection model uses elasticity coefficients to estimate how tariffs would affect import and export volumes:

- Import elasticity: -0.7 (standard in economic literature)
- Export elasticity: 1.0 (assuming reciprocal tariffs would affect our exports)

This simplified model assumes that a 1% increase in tariffs would result in:
- A 0.7% decrease in imports from tariffed countries
- A 1.0% increase in exports to those countries


<! --- MORE COMPLEX MODELS ---!>
I did not use this, but it's possible to use more complex and reactive models

### Limitations

There are obvious limitations in the simplicity of the model and the inherent difficulty
in determining which balance of trade is "good" or "bad." It may be that Americans are better 
off by having trade deficits with Mexico and Canada, and it is almost certainly true that the tariffs
which reduce those deficits would have some negative effects on the American economy.

## Running Locally

1. Clone this repository
2. Install dependencies:



