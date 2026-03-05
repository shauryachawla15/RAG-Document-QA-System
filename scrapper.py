import requests
from bs4 import BeautifulSoup


def fetch_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Website fetched successfully!")
        return response.text
    else:
        print("Failed to fetch website")
        return None


def parse_website(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    
    data = {
        "title": soup.title.text if soup.title else "No Title",
        "headings": [],
        "links": []
    }

    # Extract headings
    for heading in soup.find_all(["h1", "h2"]):
        data["headings"].append(heading.text.strip())

    # Extract links
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            data["links"].append(href)

    return data


def save_data(data):
    with open("innovationm_data.txt", "w", encoding="utf-8") as file:
        file.write("PAGE TITLE:\n")
        file.write(data["title"] + "\n\n")

        file.write("HEADINGS:\n")
        for heading in data["headings"]:
            file.write(heading + "\n")

        file.write("\nLINKS:\n")
        for link in data["links"]:
            file.write(link + "\n")

    print("Data saved locally!")


def main():
    url = "https://www.innovationm.com/"
    
    html_content = fetch_website(url)
    
    if html_content:
        data = parse_website(html_content)
        save_data(data)


if __name__ == "__main__":
    main()