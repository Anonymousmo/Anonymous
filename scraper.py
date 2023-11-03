import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from requests.exceptions import RequestException, MissingSchema

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to scrape a webpage, save hyperlinks, and remove HTML comments
def scrape_webpage(url):
    # Add 'http://' if the user didn't provide a protocol
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    print("Scraping in progress...")

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a directory for saving scraped hyperlinks
        working_dir = os.getcwd()
        scraped_links_dir = os.path.join(working_dir, 'scraped_links')
        create_directory(scraped_links_dir)

        # Scrape and save hyperlinks
        links = soup.find_all('a')
        for link in links:
            link_url = link.get('href')
            if link_url:
                # Generate a filename from the URL
                filename = urllib.parse.quote(link_url, safe='')
                with open(os.path.join(scraped_links_dir, filename), 'w', encoding='utf-8') as file:
                    file.write(link_url)

        print(f"All hyperlinks saved in the 'scraped_links' directory.")

    except RequestException as e:
        print(f"Failed to fetch the webpage: {str(e)}")
        # Continue to the next step even in case of an error

    except MissingSchema:
        print("Invalid URL format. Please include 'http://' or 'https'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Remove all HTML comments
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

# Input URL
url = input("Enter the URL to scrape: ").strip()

# Call the scrape_webpage function
scrape_webpage(url)