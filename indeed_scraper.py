import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
import time

def get_url(position, location):
    """Generate base URL without pagination."""
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    return template.format(position, location)

def save_data_to_file(records):
    """Save job records to CSV."""
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Salary', 'Summary', 'JobUrl'])
        writer.writerows(records)

def save_data_to_db(records):
    """Save job records to MySQL database, avoiding duplicates based on job_url."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # ← Replace with your MySQL username
        password="root1234",   # ← Replace with your MySQL password
        database="job_scraper"
    )
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO jobs (job_title, company, location, post_date, extract_date, salary, summary, job_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    check_query = "SELECT COUNT(*) FROM jobs WHERE job_url = %s"
    inserted_count = 0

    for record in records:
        cursor.execute(check_query, (record[-1],))  # Check by job_url
        if cursor.fetchone()[0] == 0:
            cursor.execute(insert_query, record)
            inserted_count += 1

    connection.commit()
    print(f"{inserted_count} new records inserted into database.")
    cursor.close()
    connection.close()

def get_record(card):
    """Extract job data from a card."""
    try:
        job_title = card.find_element(By.CSS_SELECTOR, 'h2.jobTitle').text
    except:
        job_title = ''
    try:
        company = card.find_element(By.CSS_SELECTOR, 'span.companyName').text
    except:
        company = ''
    try:
        location = card.find_element(By.CSS_SELECTOR, 'div.companyLocation').text
    except:
        location = ''
    try:
        post_date = card.find_element(By.CSS_SELECTOR, 'span.date').text
    except:
        post_date = ''
    try:
        salary = card.find_element(By.CSS_SELECTOR, 'div.metadata.salary-snippet-container').text
    except:
        salary = 'N/A'
    try:
        summary = card.find_element(By.CSS_SELECTOR, 'div.job-snippet').text
    except:
        summary = ''
    try:
        job_url = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    except:
        job_url = ''

    extract_date = datetime.today().strftime('%Y-%m-%d')
    return (job_title, company, location, post_date, extract_date, salary, summary, job_url)

def get_page_records(cards, job_list, url_set):
    """Extract job data from all cards."""
    for card in cards:
        record = get_record(card)
        if record[0] and record[-1] not in url_set:
            job_list.append(record)
            url_set.add(record[-1])

def main(position, location):
    scraped_jobs = []
    scraped_urls = set()
    base_url = get_url(position, location)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    # Loop through multiple pages using &start= pagination
    for page in range(0, 50, 10):  # Adjust range for more pages (e.g., 0–90 for 10 pages)
        paginated_url = f"{base_url}&start={page}"
        driver.get(paginated_url)
        time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')
        get_page_records(cards, scraped_jobs, scraped_urls)

    driver.quit()
    save_data_to_file(scraped_jobs)
    save_data_to_db(scraped_jobs)
    print(f"{len(scraped_jobs)} job records saved to results.csv and inserted into DB.")

# Run the script
main('python developer', 'charlotte nc')
