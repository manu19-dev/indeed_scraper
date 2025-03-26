# 💼 Job Scraper for Indeed.com

This project is a scalable Python-based web scraper that collects job listings from [Indeed](https://www.indeed.com), extracts structured data, and stores it in both a CSV file and a MySQL database. It handles pagination, dynamic content, missing data, and duplicate entries, making it ideal for analysis of job market trends.

---

## 📌 Features

- 🔍 Scrapes job title, company, location, post date, extract date, salary, summary, and job URL
- 📄 Saves data to CSV
- 🛢️ Inserts data into MySQL with duplicate prevention
- 🔁 Supports pagination using URL parameters (`start=0, 10, 20...`)
- 💡 Handles missing salary with fallback to `"N/A"`
- 🚀 Scalable and extendable for future enhancements

---

## 🧠 Web Scraping Strategy

- **Target**: [Indeed.com](https://www.indeed.com)
- **Dynamic Content**: Handled using `Selenium` with `ChromeDriver`
- **Pagination**: Implemented via `&start=0`, `&start=10`, etc.
- **Anti-Scraping**:
  - Real browser simulation using Selenium
  - Delay added between page requests
- **Deduplication**: Ensures uniqueness using `job_url` and DB constraint

---

## 🧱 Data Model

**Table Name**: `jobs`

| Column         | Type         | Description                       |
|----------------|--------------|-----------------------------------|
| `id`           | INT, PK      | Auto-incremented primary key      |
| `job_title`    | TEXT         | Job title                         |
| `company`      | TEXT         | Company name                      |
| `location`     | TEXT         | Job location                      |
| `post_date`    | VARCHAR(50)  | e.g., "2 days ago"                |
| `extract_date` | DATE         | Date the job was scraped          |
| `salary`       | VARCHAR(100) | Salary value or `"N/A"`           |
| `summary`      | TEXT         | Job summary/description           |
| `job_url`      | TEXT, UNIQUE | Direct job URL                    |

---

## ⚙️ Tech Stack

| Tool / Library             | Purpose                             |
|----------------------------|-------------------------------------|
| `Python 3`                 | Core language                       |
| `Selenium`                 | Dynamic web scraping                |
| `ChromeDriver`             | Browser automation with Chrome      |
| `MySQL`                    | Relational database for storage     |
| `mysql-connector-python`   | Python ↔ MySQL connection           |
| `CSV` module               | Export to CSV                       |

---


