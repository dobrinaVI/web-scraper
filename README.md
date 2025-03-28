# Scraper

### CLI
The CLI has the following interface:
 ```shell
usage: rss_reader.py [-h] [--json] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     Help message and exit
  --json         Print result as JSON in stdout
  --limit LIMIT  Limit news topics if this parameter is provided
```

### Command Line Arguments

1) If the `limit` is not specified, then the user should get _all_ available feeds. 
2) If the `limit` is larger than the feed size, then the user should get _all_ available news.
3) The `limit` argument should also affect JSON generation
4) In the case of using the `--json` argument, utility converts the news into the JSON format.


### Console Output:

* For `<channel>` element:
  1. `<title>` is equal to Feed
  2. `<link>` is equal to Link
  3. `<lastBuildDate>` is equal to Last Build Date
  4. `<pubDate>` is equal to Publish Date 
  5. `<language>` is equal to Language
  6. `<category>` `for category in categories` is equal to Categories: category1, category2
  7. `<managinEditor>` is equal to Editor
  8. `<description>` is equal to Description
  9. `<item>` `for item in items` each item is separated by a custom separator, and all items within except for the description are stuck together.
* For `<item>` element:
  1. `<title>` is equal to Title
  2. `<author>` is equal to Author
  3. `<pubDate>` is equal to Published
  4. `<link>` is equal to Link
  5. `<category>` is equal to Categories: category1, category2
  6. `<description>` is on a separate line without any name.

```shell
Feed: BBC News
Link: https://www.bbc.co.uk/news
Last Build Date: Fri, 28 Mar 2025 20:21:17 GMT
Language: en-gb
Description: BBC News - News Front Page


Title: Watch: Moment baby is born on Bangkok street after quake evacuation
Published: Fri, 28 Mar 2025 18:30:40 GMT
Link: https://www.bbc.com/news/videos/c7898myzxvpo

A woman was seen giving birth to a baby shortly after evacuating from a hospital.

Title: Student jailed for 39 years for beach murder had 'rage against women'
Published: Fri, 28 Mar 2025 15:45:34 GMT
Link: https://www.bbc.com/news/articles/cz0309m2vddo

Nasen Saadi was described in court as a "social misfit" who committed his crimes "to feel powerful".

Title: 'Then, the phone rang': BBC's Mark Lowen on being deported from Turkey
Published: Fri, 28 Mar 2025 17:04:53 GMT
Link: https://www.bbc.com/news/articles/c0jgj47zx53o

The BBC correspondent was deported from Turkey this week after covering ongoing mass protests in the country.
```


### JSON Output:

JSON output contains exact names of the tags.

```json
{
  "title": "BBC News",
  "link": "https://www.bbc.co.uk/news",
  "lastBuildDate": "Fri, 28 Mar 2025 20:09:32 GMT",
  "language": "en-gb",
  "description": "BBC News - News Front Page",
  "items": [
    {
      "title": "Watch: Moment baby is born on Bangkok street after quake evacuation",
      "pubDate": "Fri, 28 Mar 2025 18:30:40 GMT",
      "link": "https://www.bbc.com/news/videos/c7898myzxvpo",
      "description": "A woman was seen giving birth to a baby shortly after evacuating from a hospital."
    },
    {
      "title": "Student jailed for 39 years for beach murder had 'rage against women'",
      "pubDate": "Fri, 28 Mar 2025 15:45:34 GMT",
      "link": "https://www.bbc.com/news/articles/cz0309m2vddo",
      "description": "Nasen Saadi was described in court as a \"social misfit\" who committed his crimes \"to feel powerful\"."
    },
    {
      "title": "'Then, the phone rang': BBC's Mark Lowen on being deported from Turkey",
      "pubDate": "Fri, 28 Mar 2025 17:04:53 GMT",
      "link": "https://www.bbc.com/news/articles/c0jgj47zx53o",
      "description": "The BBC correspondent was deported from Turkey this week after covering ongoing mass protests in the country."
    }
  ]
}
```

