import requests
import json as js
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from typing import Optional, Sequence, List


class UnhandledException(Exception):
    """Custom exception for unhandled errors."""
    pass


class RSSParserError(Exception):
    """Custom exception for RSS parsing errors."""
    pass


def rss_parser(xml: str, limit: Optional[int] = None, json: bool = False) -> List[str]:
    """
    Parses an RSS XML string and returns formatted output.
    Supports both standard and JSON formats.
    """
    if not xml.strip():
        raise RSSParserError("Received empty XML response. Please check the URL.")

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        raise RSSParserError(f"Failed to parse XML: {e}")

    # Find the <channel> element
    channel = root.find("channel")
    if channel is None:
        raise RSSParserError("Invalid RSS feed: Missing <channel> tag")

    # Extract channel information
    title = get_text(channel.find("title"))
    link = get_text(channel.find("link"))
    last_build_date = get_text(channel.find("lastBuildDate"))
    pub_date = get_text(channel.find("pubDate"))
    language = get_text(channel.find("language"))
    categories = [get_text(cat) for cat in channel.findall("category")]
    managing_editor = get_text(channel.find("managingEditor"))
    description = get_text(channel.find("description"))

    # Extract news items
    items = []
    for item in channel.findall("item"):
        item_data = {
            "title": get_text(item.find("title")),
            "author": get_text(item.find("author")),
            "pubDate": get_text(item.find("pubDate")),
            "link": get_text(item.find("link")),
            "category": [get_text(cat) for cat in item.findall("category")],
            "description": get_text(item.find("description")),
        }
        item_data = {k: v for k, v in item_data.items() if v not in (None, "", [])}
        items.append(item_data)

    # Apply limit
    if limit:
        items = items[:limit]

    if json:
        json_result = {
            "title": title,
            "link": link,
            "lastBuildDate": last_build_date if last_build_date else None,           
            "pubDate": pub_date if pub_date else None,
            "language": language if language else None,
            "category": categories if categories else None,
            "managingEditor": managing_editor if managing_editor else None,
            "description": description if description else None,
            "items": items if items else None,
        }

        json_result = {k: v for k, v in json_result.items() if v is not None}
        json_output = [js.dumps(json_result, indent=2, ensure_ascii=False)]
        return json_output


    # Format output as per the requirement
    output = [
        f"Feed: {title}",
        f"Link: {link}",
        f"Last Build Date: {last_build_date}" if last_build_date else None,
        f"Publish Date: {pub_date}" if pub_date else None,
        f"Language: {language}" if language else None,
        f"Categories: {', '.join(categories)}" if categories else None,
        f"Editor: {managing_editor}" if managing_editor else None,
        f"Description: {description}" if description else None,
    ]
    output = [line for line in output if line]
    output.append("")  # Ensures spacing before items

    for item in items:
        item_output = []
        
        # Include key-value pairs only if the value exists
        if 'title' in item:
            item_output.append(f"\nTitle: {item['title']}")
        if 'author' in item:
            item_output.append(f"Author: {item['author']}")
        if 'pubDate' in item:
            item_output.append(f"Published: {item['pubDate']}")
        if 'link' in item:
            item_output.append(f"Link: {item['link']}")
        if 'category' in item:
            item_output.append(f"Categories: {', '.join(item['category'])}")
        if 'description' in item:
            item_output.append(f"\n{item['description']}")
        
        # Only add the item to output if it has at least one field
        if item_output:
            output.append("\n".join(item_output))

    return output


def get_text(element: Optional[ET.Element]) -> str:
    """Returns the text content of an XML element, ensuring it's not None."""
    return element.text.strip() if element is not None and element.text else ""

def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
