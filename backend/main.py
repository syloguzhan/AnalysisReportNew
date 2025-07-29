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


load_dotenv()
api_key = os.getenv("gemini_key")
if not api_key:
    raise ValueError("API key not found.")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-pro")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def find_social_media_links(html):
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

def extract_paragraphs_from_html(html):
    soup  = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all('p')
    content = "".join(p.get_text(strip=True) for p in paragraphs[:20])
    return content

def scrape_additional_pages(domain, driver):
    candidates = ['/blog', '/news', '/updates']
    collected_content = ""
    base_url = domain if domain.startswith("http") else f"https://{domain}"
    for path in candidates:
        url = base_url.rstrip("/") + path
        try:
            driver.get(url)
            time.sleep(2)
            page_content = extract_paragraphs_from_html(driver.page_source)
            collected_content += page_content
        except Exception as e:
            print(f"[Scrape Error for additional pages] {url}: {str(e)}")
            continue
    return collected_content

def scrape_social_media_content(url, driver, max_paragraphs=5):
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs[:max_paragraphs])
        return content
    except Exception as e:
        print(f"[Social Media Error] {url}: {str(e)}")
        return ""

def scrape_site(domain):
    driver = None
    try:
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
                social_media_content += f"\n[{name.capitalize()} Gönderileri]\n"
                social_media_content += scrape_social_media_content(link, driver)
        driver.quit()

        full_content = content + "\n" + extra_content + "\n" + social_media_content
        return full_content, social_links
    except Exception as e:
        print(f"[Scrape Error2] {str(e)}")
        return "", {}
    finally:
        if driver:
            driver.quit()

def find_competitors_domain(domain):
    prompt = f"""{domain} company's 1 major competitors's domain addresses.
              List only the domain addresses line by line.Do not add any other explanation!"""
    try:
        response = model.generate_content(prompt)
        raw_lines = response.text.splitlines()
        domains = [line.strip() for line in raw_lines if "." in line]
        return domains
    except Exception as e:
        print(f"[Competitor Fetch Error] {e}")
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
    try:
        response = model.generate_content(prompt)
        cleaned_response  =  response.text.strip()
        return cleaned_response
    except Exception as e:
        print(f"Error analyzing {section_title} for {domain_name}: {e}")
        return "Analysis failed"



@app.route("/generate-reports", methods=['POST'])
def generate_report():
    data = request.get_json()
    domain = data.get("domain")

    if not domain or "." not in domain:
        return jsonify({'msg': 'Please enter a valid domain name like example.com'}), 400
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        return jsonify({'msg': 'Domain does not exist or is unreachable'}), 400

    content, social_links = scrape_site(domain)
    if not content.strip():
        return jsonify({'msg': 'Content is empty'}), 400

    social_links_text = "\n".join([f"{key.capitalize()}: {value}" for key, value in social_links.items() if value])

    formal_instructions = "Please respond with a formal,  coherent , essay-style paragraph instead of markdown or list format"
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
    for title, prompt_text in sections.items():
        main_report[title] = analyze_section_for_domain(domain, content, title, prompt_text, social_links_text)

    competitors = find_competitors_domain(domain)
    competitors_report = []
    for comp in competitors[:1]:
        comp_content, comp_social = scrape_site(comp)
        if not comp_content.strip():
            continue
        comp_social_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in comp_social.items() if v])

        comp_sections = {}
        for title, prompt_text in sections.items():
            comp_sections[title] = analyze_section_for_domain(comp, comp_content, title, prompt_text, comp_social_text)

        competitors_report.append({
            "competitor_domain": comp,
            "sections": comp_sections
        })


    return jsonify({
        "main_domain": domain,
        "main_report": main_report,
        "competitors": competitors_report,
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
