# Pac Category

This project finds similarities between political action committees based on the total votes of all Congresspeople each PAC donates to. 

This project does not draw conclusions concerning the correlation between which PAC donates to which candidate, nor does it draw a correlation between a PAC’s influence over Congresspeople. Those kind of studies are numerous already. 

# Considerations: 
This project views a PAC contribution, of any size, to one candidate as an endorsement of all bills the candidate votes “Yes” on. This consideration is without regard to what the PAC’s views are publicly and instead treats all “Yes” votes as tacit agreement by the PAC. This decision is made for two reasons: public statements of PACs may not align with private decisions and Congresspeople may have different perspectives on the donation’s purpose. This setup should remove prejudice and assumptions toward how much a PAC donates, how a PAC is viewed publicly, and the importance a Congressperson places on specific donations.

# Data used:
All data is acquired through three sources: opensecrets.org (OS), voteview.com (VV), and a public [github](https://github.com/unitedstates/congress-legislators). This public github (third source) is mostly used as a joiner between OS and VV. The project considers all bills that require a Presidential signature and bills that were voted on by House and Senate members from 2010 to present day. 2010 is selected as a starting year because this is the year that Citizens United v FEC was decided. For the moment, the project uses the top ten donors for each Congressperson per political cycle they ran, because that dataset is available to me.

# Overall Process:
1. us_git_legis_pull.py -> Used to pull all Congresspeople before 2010 and sets up a key to allow connection to voteview and opensecrets data. It creates a csv.
2. vv_roll_nmbr_key.py -> Used to combine all >2010 House/Senate bills into one csv from bulk data. Specifically targets bills requiring presidential signature. Includes a key to identify the bill by Chamber, Congress, and rollnumber. Used for pivoting later.
3. os_pac_pull.py -> Used to pull the top ten PAC donors to each congressperson for each congressional cycle served. Returns csv's every 5 API calls
4. vv_votes_2_PACs.py -> Used to find the sum donated by each PAC and the number of times a PAC voted on a specific bill via a Congressperson. All bills are featured in this csv.

   This program incorporates all work from above. us_git_legis_pull to pull the congresspeople keys. vv_roll_nmbr_key to find the unique bill identifiers and pivot them. os_pac_pull to find the donations made to each candidate.
   
5. pca_cluster.py -> Now that all of our data is together, we run PCA and clustering algorithms on the result of vv_votes_2_PACs.py

# Next Steps and Possible Improvements:
Next steps include visualizing the clusters and potenitally a blog post or user interface to help users navigate the analysis. Future iterations of this project will include a full list of PAC donations, followed by more model iterations. Under consideration is adding temporal consideration to the donation logic. At the moment, this model assumes a PAC makes a donation in 2016 while analyzing all votes by a Congressperson even back to 2010. We might find more accuracy if we restrict the model to only group on votes made from the earliest donation forward. 

# Known bugs: 
The current iteration of us_git_legis_pull.py creates a file called leg_2010. This output needs to be updated to handle off year elections like special elections. Currently it does not, and causes os_pac_pull.py to be semi manual and cumbersome.

	
