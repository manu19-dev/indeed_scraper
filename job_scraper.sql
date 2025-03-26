CREATE DATABASE job_scraper;

USE job_scraper;

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    location TEXT,
    post_date VARCHAR(50),
    extract_date DATE,
    salary VARCHAR(100),
    summary TEXT,
    job_url TEXT UNIQUE
);
