## Execution Process

### Initialize the scrapper
```
scraper = JoeRoganPodcastScraper(URL)
```
### Define the attributes, Html Tag and CSS Class
```
scraper.define_attributes(
    ('title', 'h2', 'card__title'),
    ('date', 'p', 'card__date'),
    ('duration', 'span', 'card__duration'),
    ('excerpt', 'div', 'card__excerpt')
)
```

### Scrape the Data
```
scraper.scrape()
```

### Fetch the Scraped Data

```
scraper.update_episode_data()

for i, episode in enumerate(scraper.episode_manager.get_episodes_data()):
    print(f"{i} \n{episode}", end="\n")
```
