## Scraping GSoC
When I saw this task in the list, I slept. Because I figured writing a couple of Bs4 commands wouldn't take me long. I was mistaken.
Google like basically every modern site out there (Yahoo! Finance is an example) uses Javascript to populate HTML, so requesting the url and then running bs4 was out of question.
It was time to bring in the big guns, i.e Selenium.
### Enter Selenium
Selenium is used to automate browsers. Now browsers _can_ run Javascript to populate HTML, so by using selenium I was able to filter HTML elements. I found the XPATH/CSS selector using Inspect Element (pro-level hacking skillz) and then simply used the find_elements() method of Selenium. This was fairly easy, but took a lot of time. At ~6 seconds per organisation, I had to wait for 20 minutes to get the attributes of each organisation.
I was able to get the name, short description, tech stack, topics, and contact details. I also scraped the full description because it was just one more line of code. 
Now I had the dictionary of dictionaries, one dictionary for each organization. 
Converting the dictionary to JSON was easy. 
### Brownie Points
This seemed impossible in the beginning. After spending a lot of time in the inspect console, I found that clicking on category buttons **does not** send javascript request. It just sent requests for every organisations logo. This meant that the homepage already _knew_ which organisations fell into each category. This pointed to the fact that when the website was first loaded, it received a database of all organisations, and buttons simpy filtered the database. Sure enough, after some digging, I found that Google uses an API (ofc). A certain call returned a JSON containing everything one could hope to know about an organisation. This was a facepalm moment. 
All the time I spent scraping the website could have been diverted more noble pursuits like scrolling Instagram for cat pictures.
Anyway, extracting tags now was a trivial affair. 
I extracted tags therefore earning my brownie points.


### Usage
To simply scrape data run python3 scraping.py


This returns a json file called 'orgs.json'
To scrape and tag data run python3 scraping.py tags
'''