#!/usr/bin/env python3

import json
import os
import html
import sys
from datetime import datetime, timezone

def create_image_page(date, description, img_path, prev_page_path, next_page_path):
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
    html += "</div>\n"
    html += "</body>\n"
    html += "<footer>\n"
    html += "<p><a href=\"" + prev_page_path + "\"><</a>  |  <a href=\"index.html\">index</a>  |  <a href=\"" + next_page_path + "\">></a></p>"
    html += "<p>" + copyright + "</p>\n"
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

    previous_data_item = data[len(data) - 1]
    next_data_item = data[1]

    html = "<!DOCTYPE html>\n"
    html += "<html lang=\"en\">\n"
    html += "<head>\n"
    html += "<meta charset=\"UTF-8\">\n"
    html += "<title>One a Day</title>\n"
    html += "<meta name=\"description\" content=\"" + site_description + "\" />\n"
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
            previous_page_path = previous_data_item["image"]["filename"].split(".")[0] + ".html"
            next_page_path = next_data_item["image"]["filename"].split(".")[0] + ".html"
            if (page_name not in file_list or update_files == "True"):
                # Create individual image page
                with open(public_directory_path + page_name, "w") as f:
                    f.write(create_image_page(date, description, img_path, previous_page_path, next_page_path))
                increment_count()
            # Add link to index page
            html += "<a href=\"" + page_name + "\"><img loading=\"lazy\" class=\"thumbnail\" src=\"" + thumb_path + "\" alt=\"" + description + "\" title=\"" + date + " - " + description + "\"/></a>\n"
            previous_data_item = item
            if (data.index(item) + 1 >= len(data) - 1):
                next_data_item = data[0]
            else:
                next_data_item = data[data.index(item) + 2]
    html += "</div>\n"
    html += "</body>\n"
    html += "<footer>\n"
    html += "<p>" + copyright + "</p>\n"
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
    rss += "<description>" + site_description + "</description>\n"
    rss += "<language>en-us</language>\n"
    rss += "<copyright>" + copyright + "</copyright>\n"
    rss += "<lastBuildDate>" + datetime.now(timezone.utc).strftime(date_format) + "</lastBuildDate>\n"
    rss += "<docs>https://www.rssboard.org/rss-specification</docs>\n"

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
        rss += "<pubDate>" + rfc822date(date) + "</pubDate>\n"
        rss += "</item>\n"

    rss += "</channel>\n"
    rss += "</rss>"

    return rss

def rfc822date(date_string):

    rfc_date_string = datetime.strptime(date_string, '%B %d, %Y').replace(tzinfo=timezone.utc)
    
    return rfc_date_string.strftime(date_format)

def increment_count():
    global change_file_count
    change_file_count += 1

if __name__ == "__main__":

    try:
        # Some global variables
        copyright = "Copyright © 2023-24 JP Reardon"
        site_description = "Photoblogging like it's 1996! One picture a day, for a year (at least)."
        date_format = "%a, %d %b %Y %H:%M:%S %z"
        image_directory_name = "images"
        site_url = sys.argv[1] # URL
        public_directory_path = sys.argv[2] # Public directory path
        update_files = sys.argv[3] # If True, rewrites all image pages
        image_directory_path = public_directory_path + image_directory_name
        change_file_count = 0
        
        # Load JSON data
        with open(os.path.join(image_directory_path, "data.json"), "r") as f:
            data = json.load(f)

        # Get list of existing HTML pages
        file_list = os.listdir(public_directory_path)

        # Create index page with links to individual image pages
        index_page = create_index_page(data, image_directory_name)

        # Only write write files and create RSS if there are changes
        if (change_file_count > 0):
        
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