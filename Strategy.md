Exercise 1: Web Scraping Strategy & Implementation

Scenario
Build a scalable web scraper to extract publicly available job postings from a major job platform (Indeed.com), process the data into structured format, and store it for downstream analytics and visualization.

---

1. Web Scraping Strategy

Target: [Indeed.com](https://www.indeed.com) — one of the largest public job boards in the world with structured job posting listings.

Identification Approach
- Used browser dev tools to inspect HTML structure and identify job listing containers.
- Selected `.job_seen_beacon` as the primary class to locate job cards reliably.
- Identified consistent elements for job title, company, location, summary, date posted, and job URL.

Rate Limiting & Anti-Bot Considerations
- Added `time.sleep()` between page loads to reduce request frequency.
- Used a real browser via Selenium (ChromeDriver) to simulate human-like interaction.
- Avoided unnecessary reloading and only visited paginated URLs.
- For production-scale scraping, rotating proxies and user-agent spoofing can be added.

---

2.Handling Pagination, Dynamic Content, & Anti-Scraping

Pagination
- Indeed uses a URL parameter-based pagination strategy: `start=0`, `start=10`, `start=20`, etc.
- Instead of relying on fragile UI interactions ("Next" buttons), the scraper iteratively builds the paginated URLs for multiple pages.

Dynamic Content Loading
- Job data is loaded via JavaScript on Indeed.
- Selenium was used to allow full page rendering and reliable DOM access.
- `find_elements` waits were added to ensure all listings were loaded before scraping.

Anti-Scraping Measures
- Browser-based scraping using Selenium + ChromeDriver reduces the chance of IP bans.
- Script mimics human browsing with real browser headers and natural delays.
- Optional: proxy rotation, headless mode, and CAPTCHA detection for large-scale use.

---

3. Structured Data Model

Storage Type: SQL (MySQL)

 Field         | Type         | Description                          
------------------------------------------------------------------ 
 `id`           INT, PK       Auto-incremented primary key         
 `job_title`    TEXT          Job title                            
 `company`      TEXT          Employer name                        
 `location`     TEXT          Job location                         
 `post_date`    VARCHAR(50)   e.g., “3 days ago”                   
 `extract_date` DATE          Date the data was scraped           
 `salary`       VARCHAR(100)  Parsed salary or `"N/A"`             
 `summary`      TEXT          Job description snippet              
 `job_url`      TEXT, UNIQUE  Direct URL to the job post           

Why SQL?
- The data is highly structured and fits well in relational format.
- MySQL provides excellent query performance for reporting/analysis.
- Enforces data integrity and supports duplicate checking via constraints.

---

4. Handling Duplicates, Missing Data & Integrity

Duplicate Handling
- Used the `job_url` as a **natural unique key**.
- Implemented logic in Python to check if `job_url` already exists in the DB before insertion.
- Enforced a `UNIQUE` constraint in MySQL for safety.

Missing Values
- Not all listings have salary info.
- If missing, `"N/A"` is stored in the `salary` field to maintain consistent structure.

Data Integrity
- Used parameterized SQL queries to prevent SQL injection.
- Ensured all required fields are scraped and validated before insert.
- All scraped jobs are also stored in a local CSV as a secondary backup.

---

5. Languages, Libraries & Justification

 Tool / Library              Role                                       Justification                                        
-----------------------------------------------------------------------------------------------------------------------------
 Python 3                    Core programming language                  Readable, scalable, and great ecosystem for scraping 
 Selenium              Web scraping (dynamic content)             Handles JavaScript rendering & page interactions     
 ChromeDriver**            Browser automation                         Real browser behavior, human-like scraping           
 MySQL                   Structured data storage                   Ideal for tabular data & query performance           
 mysql-connector-python 
