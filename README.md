# WhereToBot
A discord bot with the same design as "throwing a dart at a map". Displays information about a random country or one within a specified region if wanted!

In order to use bot make an environ.py file and define the following variable: TOKEN = 'Your bot's token here' 

To change the command prefix under the variable 'client' change the command prefix (Defaults to '>')

Displays the following information about the chosen country from the JSON file:
- Name
- Capital
- Native Language
- Country's currency
- Country's region

Uses are as follows:
- \>whereto help : displays a help embed
- \>whereto random : chooses a random country from the Countries.json 
- \>whereto region [Region] : chooses a random country from the specified region (see whereto help for list of available region choices) 
