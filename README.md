# OfferBot

# Description:

Have you ever wanted a bot that can dynamically search OfferUp? What if it can parse it into a spreadsheet? Or even send you a text message?
**Well look no further**
#### Introducing OfferBot!
This Python project powered by BS4 and Twilio will dynamically search all of the OfferUp platform based on a set of search terms and filter parameters and will direct its output into a csv file that can be used for spreadsheet applications such as Microsoft Excel, Google Sheets, and more! If that wasn't good enough, it will also send you a text message everytime a new item is posted (if you choose to) meaning if you're a real deal hunter, simply put in your search parameters, let it run, and wait for a text. Its that easy.

## Usage: 
- `config.json`
  The configuration file in *JSON format* for the different search terms and parameters to look through offerup. This can take an infinite list of search objects but is only restricted on filters that are taken as url parameters

- `db.csv`
  The CSV formatted database for all parsed offerup cards can be used in any spreadsheet application for further search & filters, graphs, etc... 
  
- `main.py`
   Run this program to start parsing and searching through offerup using the given parameters
