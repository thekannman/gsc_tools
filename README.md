# gsc_tools

Please let me know if you find this useful, identify a special use case, or need to request revisions.

Email: zak@zakkann.com

Twitter: @zrkann 

The gsc_graph_gen.py script creates an improved view of your GSC data.

This data is imported into a Google sheet for easy analysis.

I'll be releasing an easier-to-use web app soon. This version is for
1. Tech-savvy early adopters (get it now, not in a couple of weeks)
2. The ultra security conscious. I understand why some are hesitant to give a web app access to their data. This downloadable version uses your own API key, and the code is entirely open-source. If you have ideas of how to make it more secure, I'm open to them, but this is my current gold standard.


## Current limitations
1. Limited to top 1000 pages. Going beyond this is difficult with the Google Sheet's cell limit.
2. Ignores jump-to URLs (Ex: sample.com/#some_header)
3. Only shows page-level data. Query-level data is coming in the next version.
4. Graphs are always 2022-01-01 to current date. A future version may expand this, but custom ranges would require dealing with the Google Sheets cell limit or switching to a different output format.

## Getting started
1. You'll need oauth credentials for the downloadable version of this app. You can get those by creating a project at https://console.cloud.google.com/. 
2. Once you've created the project, go to https://console.cloud.google.com/apis/dashboard and enable access for the Google Search Console and Google Sheets APIs.
3. Finally, create an OAuth client ID at https://console.cloud.google.com/apis/credentials (for a Desktop app) and download the json file of the credentials.
4. Near the top of the code are two parameters: oauth_file and site. The oauth_file should 

## Output
The final output is created in your Google Sheets account as "GSC graphs - pages". 

You'll find 4 sheets in that file. The first 3 are 1 row per page, showing the trends in clicks (first sheet), impressions (second sheet), or position (third sheet) over time.

The 4th sheet presents the click, impression, and position trends together, with one column per page.
