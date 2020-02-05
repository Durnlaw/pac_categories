# Pac Category

This project that finds similarities between political action committees based on the total votes of all Congresspeople each PAC donates to. 

The intent of this project is not to draw conclusions concerning the correlation between what kind of PAC donates to what kind of candidate, nor is the intent to find a correlation between a PAC’s influence over Congresspeople. Those kind of studies are numerous already. 

# Considerations: 
This project views a PAC contribution, of any size, to one candidate as an endorsement of all bills the candidate votes “Yes” on. This consideration is without regard to what the PAC’s views are publicly and instead treats all “Yes” votes as tacit agreement by the PAC. This decision is made for two reasons: public statements of PACs may not align with private decisions and Congresspeople may have different perspectives on the donation’s purpose. This setup should remove prejudice and assumptions toward how much a PAC donates, how a PAC is viewed publicly, and the importance a Congressperson places on specific donations.

# Data used:
All data is acquired through three sources: opensecrets.org (OS), voteview.com (VV), and a public github (https://github.com/unitedstates/congress-legislators). This public github is mostly used as a joiner between OS and VV. The project considers all bills that require a Presidential signature voted on by House and Senate members from 2010 to present day. 2010 is selected as a starting year because this is the year that Citizens United v FEC was decided. For the moment, the project uses the top ten donors for each Congressperson per political cycle they ran, because that dataset is available to me.

# Overall Process: (Write up in progress)
1. us_git_legis_pull.py -> Used to pull all Congresspeople before 2010.
2. 

# Next Steps and Possible Improvements:
Next steps include visualizing the clusters and potenitally a blog post or user interface to help users navigate the analysis. Future iterations of this project will include a full list of PAC donations, followed by more model iterations. Under consideration is adding temporal consideration to the donation logic. At the moment, this model assumes a PAC makes a donation in 2016 while analyzing all votes by a Congressperson even back to 2010. We might find more accuracy if we restrict the model to only group on votes made from the earliest donation forward. 

# Known bugs: 
The current iteration of us_git_legis_pull.py creates a file called leg_2010. This output needs to be updated to handle off year elections like special elections. Currently it does not, and causes os_pac_pull.py to be semi manual and cumbersome.

	
