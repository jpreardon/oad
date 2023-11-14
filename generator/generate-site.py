#!/usr/bin/env python3

import json
import os
import html
import sys

def create_image_page(date, description, img_path):
    """
    Create a static HTML page for an individual image.

    Args:
        title (str): The title of the image.
        description (str): A description of the image.
        img_path (str): The path to the image file.

    Returns:
        str: The HTML code for the page.
    """
    html = "<!DOCTYPE html>\n"
    html += "<html lang=\"en\">\n"
    html += "<head>\n"
    html += "<meta charset=\"UTF-8\">\n"
    html += "<title>" + date + "</title>\n"
    html += "<meta name=\"description\" content=\"" + description + "\" />\n"
    html += "<link href=\"styles/main.css\" rel=\"stylesheet\">\n"
    html += "</head>\n"
    html += "<body>\n"
    html += "<div class=\"container\">\n"
    html += "<img class=\"main-image\" src=\"" + img_path + "\" alt=\"" + description + "\" title=\"" + date + " - " + description + "\" />\n"
    html += "<a href=\"index.html\" >go back...</a>"
    html += "<div />\n"
    html += "</body>\n"
    html += "<footer>\n"
    html += "<p>Copyright &copy; 2023 JP Reardon</p>\n"
    html += "</footer>\n"
    html += "</html>\n"
    return html

def create_index_page(data, img_dir):
    """
    Create a static HTML index page with links to individual image pages.

    Args:
        data (list): List of dictionaries containing the JSON data.
        img_dir (str): Path to the directory containing the images.

    Returns:
        str: The HTML code for the page.
    """

    html = "<!DOCTYPE html>\n"
    html += "<html lang=\"en\">\n"
    html += "<head>\n"
    html += "<meta charset=\"UTF-8\">\n"
    html += "<title>One a Day</title>\n"
    html += "<meta name=\"description\" content=\"Photoblogging like it's 1996! One picture a day, for a year (at least).\" />\n"
    html += "<link rel=\"alternate\" type=\"application/rss+xml\" href=\"" + site_url + "rss.xml\" title=\"RSS Feed\">\n"
    html += "<link href=\"styles/main.css\" rel=\"stylesheet\">\n"
    html += "</head>\n"
    html += "<body>\n"
    html += "<div class=\"grid\">\n"

    for item in data:
        date = item["date"]
        description = item["description"]
        if "image" in item:
            image = item["image"]
            thumbnail = item["thumbnail"]
            img_path = os.path.join(img_dir, image["filename"])
            thumb_path = os.path.join(img_dir, thumbnail["filename"])
            page_name = image["filename"].split(".")[0] + ".html"
            # Create individual image page
            with open(public_directory_path + page_name, "w") as f:
                f.write(create_image_page(date, description, img_path))
            # Add link to index page
            html += "<a href=\"" + page_name + "\"><img class=\"thumbnail\" src=\"" + thumb_path + "\" alt=\"" + description + "\" title=\"" + date + " - " + description + "\"/></a>\n"

    html += "</div>\n"
    html += "</body>\n"
    html += "<footer>\n"
    html += "<p>Copyright &copy; 2023 JP Reardon</p>\n"
    html += "</footer>\n"
    html += "</html>\n"

    return html

def create_rss_feed(data, img_dir):
    """
    Create a static HTML index page with links to individual image pages.

    Args:
        data (list): List of dictionaries containing the JSON data.
        img_dir (str): Path to the directory containing the images.

    Returns:
        str: The HTML and RSS code for the page.
    """
    rss = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    rss += "<rss version=\"2.0\">\n"
    rss += "<channel>\n"
    rss += "<title>One a Day</title>\n"
    rss += "<link>" + site_url + "</link>\n"
    rss += "<description>One picture a day, need I say more?</description>\n"

    for item in data:
        date = item["date"]
        description = item["description"]
        image = item["image"]
        img_path = os.path.join(img_dir, image["filename"])
        page_name = image["filename"].split(".")[0] + ".html"
        rss_description = html.escape("<img src=\"" + site_url + img_path + "\" alt=\"" + description + "\" /> <p>" + description + "</p> <p><a href=\"" + site_url + page_name + "\">view on site</a>")

        rss += "<item>\n"
        rss += "<title>" + date + "</title>\n"
        rss += "<link>" + site_url + page_name + "</link>\n"
        rss += "<description>" + rss_description + "</description>\n"
        rss += "</item>\n"

    rss += "</channel>\n"
    rss += "</rss>"

    return rss

if __name__ == "__main__":

    try:
        # Get URL and paths from command arguments
        site_url = sys.argv[1]

        # public directory path
        public_directory_path = sys.argv[2]

        image_directory_name = "images"

        # was "../images"
        image_directory_path = public_directory_path + image_directory_name

        # Load JSON data
        with open(os.path.join(image_directory_path, "data.json"), "r") as f:
            data = json.load(f)

        # Create index page with links to individual image pages
        index_page = create_index_page(data, image_directory_name)

        # Create rss feed
        rss = create_rss_feed(data, image_directory_name)

        # Write index page to file
        with open(public_directory_path + "index.html", "w") as f:
            f.write(index_page)

        # Write the rss feed to file
        with open(public_directory_path + "rss.xml", "w") as f:
            f.write(rss)

    except Exception as e:
        print("Error:", e)
        # clean up resources here...
        sys.exit(1)