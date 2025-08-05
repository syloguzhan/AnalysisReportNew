import logging
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import google.generativeai as genai
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from report_utils import load_report_if_recent, save_report_to_file
from logger import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
api_key = os.getenv("gemini_key")
if not api_key:
    logger.error("API key not found in environment.")
    raise ValueError("API key not found.")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-pro")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def init_driver():
    logger.info("Initializing Chrome driver.")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def find_social_media_links(html):
    logger.info("Finding social media links from HTML content.")
    try:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", href=True)
        social_links = {
            "linkedin": None,
            "twitter": None,
            "instagram": None,
            "facebook": None
        }
        for link in links:
            href = link["href"]
            if "linkedin.com" in href and not social_links["linkedin"]:
                social_links["linkedin"] = href
            elif "twitter.com" in href and not social_links["twitter"]:
                social_links["twitter"] = href
            elif "instagram.com" in href and not social_links["instagram"]:
                social_links["instagram"] = href
            elif "facebook.com" in href and not social_links["facebook"]:
                social_links["facebook"] = href
        return social_links
    except Exception as e:
        logger.error(f"Error in find_social_media_links: {e}")
        return {
            "linkedin": None,
            "twitter": None,
            "instagram": None,
            "facebook": None
        }

def extract_paragraphs_from_html(html):
    logger.info("Extracting paragraphs from HTML content.")
    try:
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all('p')
        content = "".join(p.get_text(strip=True) for p in paragraphs[:20])
        return content
    except Exception as e:
        logger.error(f"Error in extract_paragraphs_from_html: {e}")
        return ""

def scrape_additional_pages(domain, driver):
    candidates = ['/blog', '/news', '/updates']
    collected_content = ""
    base_url = domain if domain.startswith("http") else f"https://{domain}"
    for path in candidates:
        url = base_url.rstrip("/") + path
        try:
            logger.info(f"Scrapping additional page : {url}")
            driver.get(url)
            time.sleep(2)
            page_content = extract_paragraphs_from_html(driver.page_source)
            collected_content += page_content
        except Exception as e:
            logger.error(f"Error in scrape_additional_pages: {url} : {str(e)}")
            continue
    return collected_content

def scrape_social_media_content(url, driver, max_paragraphs=5):
    try:
        logger.info(f"Scrapping social media content : {url}")
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs[:max_paragraphs])
        return content
    except Exception as e:
        logger.error(f"Failed to scrape social media content at {url} : {str(e)}")
        return ""

def scrape_site(domain):
    driver = None
    try:
        logger.info(f"Starting site scraping for domain : {domain}")
        url = f"http://{domain}" if not domain.startswith("http") else domain
        driver = init_driver()
        driver.get(url)
        time.sleep(2)
        main_html = driver.page_source
        content = extract_paragraphs_from_html(main_html)
        extra_content = scrape_additional_pages(url, driver)
        social_links = find_social_media_links(main_html)
        social_media_content = ""
        for name, link in social_links.items():
            if link:
                social_media_content += f"\n[{name.capitalize()} Posts]\n"
                social_media_content += scrape_social_media_content(link, driver)
        driver.quit()
        full_content = content + "\n" + extra_content + "\n" + social_media_content
        logger.info(f"Finished site scraping for domain : {domain}")
        return full_content, social_links
    except Exception as e:
        logger.error(f"Failed to scrape site : {domain} : {str(e)}")
        return "", {}
    finally:
        if driver:
            driver.quit()


def retry_generate_content(prompt, retries=5, delay=3, section=None, domain=None):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            if response and response.text.strip():
                logger.info(f"Success on attempt {attempt+1} for section: {section} on domain: {domain}")
                return response.text.strip()
        except Exception as e:
            logger.error(f" Attempt {attempt+1} failed for section: {section} on domain: {domain} - Error: {e}")
            time.sleep(delay)
    logger.error(f" All {retries} attempts failed for section: {section} on domain: {domain}")
    return None


def find_competitors_domain(domain):
    logger.info(f"Starting competitors domain scraping for domain : {domain}")
    prompt = f"""{domain} company's 5 major competitors' domain addresses.
              List only the domain addresses line by line. Do not add any other explanation!"""
    result = retry_generate_content(prompt, retries=5, delay=3, section="Competitor Domains", domain=domain)
    if result:
        raw_lines = result.splitlines()
        domains = [line.strip() for line in raw_lines if "." in line]
        logger.info(f"Competitors domains fetched for {domain}: {domains}")
        return domains
    else:
        logger.error(f"Failed to fetch competitors for {domain} after retries.")
        return []

def analyze_section_for_domain(domain_name, text_content, section_title, section_prompt, social_links_text):
    prompt = f"""
    Below are contents from the website {domain_name}.
    SOCIAL MEDIA:
    {social_links_text} 

    WEBSITE CONTENT:
    {text_content}

    Please provide a detailed analysis for: {section_title}
    {section_prompt} 
    """
    logger.info(f"Running AI analysis for section: {section_title} on domain: {domain_name}")
    result = retry_generate_content(prompt, retries=5, delay=3, section=section_title, domain=domain_name)
    return result if result else "Analysis failed"

def generate_summary_for_table(domain, text, field_name):
    prompt = f"""
    Summarize the content about "{domain}" for the section "{field_name}" in a style suitable for a comparison matrix.
    Rules:
    - Maximum 20 words (1 short sentence only).
    - Clear, objective, and concise.
    - Focus on key facts or differentiators relevant to the section.
    - Do NOT start with generic phrases like "The company" or "Based on the content."
    - No extra commentary or explanations.

    Content:
    {text}

    Return ONLY the summary sentence.
    """

    logger.info(f"Generating summary for table field: {field_name} of {domain}")
    result = retry_generate_content(prompt, retries=5, delay=3, section=field_name, domain=domain)
    return result if result else "No data available"

@app.route("/generate-reports", methods=['POST'])
def generate_report():
    data = request.get_json()
    domain = data.get("domain")
    force_refresh = data.get("force_refresh", False)
    logger.info(f"Received report generation request for domain: {domain} with force_refresh={force_refresh}")

    if not domain or "." not in domain:
        return jsonify({'msg': 'Please enter a valid domain name like example.com'}), 400
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        return jsonify({'msg': 'Domain does not exist or is unreachable'}), 400

    if not force_refresh:
        existing_report = load_report_if_recent(domain)
        if existing_report:
            return jsonify(existing_report), 200

    content, social_links = scrape_site(domain)
    if not content.strip():
        return jsonify({'msg': 'Content is empty'}), 400

    social_links_text = "\n".join([f"{key.capitalize()}: {value}" for key, value in social_links.items() if value])
    formal_instructions = "Please respond with a formal, coherent, essay-style paragraph instead of markdown or list format"

    sections = {
        "Company Overview & Strategy": (
            "Analyze the company's key topics and industry focus, main customer segments, "
            "business model, revenue strategy, and any notable partnerships or collaborations. "
            + formal_instructions
        ),
        "Technology & Practices": (
            "Examine the company's use of technological innovations, digital tools, "
            "as well as its ethical and sustainable practices. "
            + formal_instructions
        ),
        "Reputation & Team": (
            "Evaluate the company's brand strength and public image, its geographical presence, "
            "and comment on the management team’s visibility or expertise. "
            + formal_instructions
        ),
        "SWOT Summary": (
            "Provide a SWOT-style summary to highlight key strengths, weaknesses, opportunities, and threats. "
            + formal_instructions
        ),
        "Weekly Activity Summary": (
            "Provide a concise summary of what this company has done or announced in the past week. "
            + formal_instructions
        ),
    }

    main_report = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(analyze_section_for_domain, domain, content, title, prompt_text, social_links_text): title for title, prompt_text in sections.items()}
        for future in as_completed(futures):
            title = futures[future]
            main_report[title] = future.result()

    competitors = find_competitors_domain(domain)

    def process_competitor(comp):
        comp_content, comp_social = scrape_site(comp)
        if not comp_content.strip():
            return None
        comp_social_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in comp_social.items() if v])
        comp_sections = {}
        for title, prompt_text in sections.items():
            comp_sections[title] = analyze_section_for_domain(comp, comp_content, title, prompt_text, comp_social_text)
        return {"competitor_domain": comp, "sections": comp_sections}

    competitors_report = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_competitor, comp): comp for comp in competitors[:5]}
        for future in as_completed(futures):
            result = future.result()
            if result:
                competitors_report.append(result)

    all_domains = [{"company": domain, **main_report}] + [{"company": comp["competitor_domain"], **comp["sections"]} for comp in competitors_report]
    comparison_table = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for d in all_domains:
            summarized_fields = {}
            for key, value in d.items():
                if key != "company":
                    futures[executor.submit(generate_summary_for_table, d["company"], value, key)] = (d["company"], key)
            for future in as_completed(futures):
                company, key = futures[future]
                summarized_fields[key] = future.result()
            summarized_fields["company"] = d["company"]
            comparison_table.append(summarized_fields)

    turkey_time = datetime.utcnow() + timedelta(hours=3)
    result_data = {
        "main_domain": domain,
        "main_report": main_report,
        "competitors": competitors_report,
        "comparison_table": comparison_table,
        "saved_at": turkey_time.isoformat(),
    }

    save_report_to_file(domain, result_data)
    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=False)
