# Chrono24 Scraper

1. By inspecting page by page, the scraper collects the URLs of individual listings and stores them in a list.
2. The scraper then searches for each listing saved in the list and downloads all available information.
3. The information is organized into nested dictionaries since the structure varies from listing to listing, with the key being the listing code.
4. Information about the date when a particular listing was downloaded is added.
5. The dictionary is then downloaded in JSON format.

For specific details, we refer to the scraper itself. However, a couple of important considerations need to be made. This structure was designed to allow data to be downloaded in separate instances since it is a time-consuming process dependent not only on machine performance but also on internet connection performance. In particular, the scraper is "resilient" to network outages (it continues despite interruptions) and resilient if the listings saved in the list are removed. In practice, it only allows the insertion of correctly downloaded data. Additionally, it is equipped with sleep functions to avoid being blocked by the site.

The resulting JSON file is organized as follows:

```json
{
    "KEY": {
        "Basic Info": {...},
        "Caliber": {...},
        "Case": {...},
        "Bracelet/strap": {...},
        "Functions": [...],
        "Other": [...],
        "Title Page": {...},
        "Date of Download": {...}
    }, 
    ...
}
```

The structure of the described JSON consists of a main object with several keys inside. The keys are the codes of the listings, which in turn are objects with several keys inside. Each key inside the object represents an object that can, in turn, contain various keys and values. Specifically, the keys "Basic Info", "Caliber", "Case", "Bracelet/strap", "Functions", and "Other" refer to watch data, while the key "Title Page" represents data from the main page of the listing, and the key "Date of Download" represents the date the data was downloaded. Note that the keys "Functions" and "Other" may be absent, as the structure varies depending on the listing, and in general, the "sub-keys" can vary from listing to listing.
