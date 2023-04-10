import json
import os

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
    html += "<html>\n"
    html += "<head>\n"
    html += "<title>" + date + "</title>\n"
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
    html += "<html>\n"
    html += "<head>\n"
    html += "<title>One a Day</title>\n"
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
            with open("../" + page_name, "w") as f:
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

if __name__ == "__main__":

    image_directory_path = "../images"
    image_directory_name = "images"

    # Load JSON data
    with open(os.path.join(image_directory_path, "data.json"), "r") as f:
        data = json.load(f)

    # Create index page with links to individual image pages
    html = create_index_page(data, image_directory_name)

    # Write index page to file
    with open("../index.html", "w") as f:
        f.write(html)