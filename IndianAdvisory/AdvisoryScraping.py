from flask import Flask, request, jsonify
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

app = Flask(__name__)

# Directory where PDFs will be saved
DOWNLOAD_DIRECTORY = "C:\\Users\\Sri Ranjini kavita\\Desktop\\bhumi\\IndianAdvisory\\pdf"

def configure_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIRECTORY,  # Set download directory
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # Automatically download PDFs
    })
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def script(state, district, language):
    initial_url = "https://kvk.icar.gov.in/agromet_advisory.aspx"
    driver = configure_driver()

    try:
        driver.get(initial_url)
        
        # Select state
        state_dropdown = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddl_State'))
        state_dropdown.select_by_visible_text(state)
        
        # Select district
        district_dropdown = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddl_district'))
        district_dropdown.select_by_visible_text(district)
        
        # Select language
        language_dropdown = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddl_language'))
        language_dropdown.select_by_visible_text(language)
        
        # Click 'Go' to load results
        go_button = driver.find_element(By.ID, 'ContentPlaceHolder1_btn')
        go_button.click()
        
        # Wait for the PDF download button to be clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_btnDownload'))
        )
        
        # Click the download button
        download_button = driver.find_element(By.ID, 'ContentPlaceHolder1_btnDownload')
        download_button.click()
        
        # Wait for the download to complete
        time.sleep(5)
        
        return {"status": "PDF download initiated", "directory": DOWNLOAD_DIRECTORY}
    
    except (NoSuchElementException, TimeoutException) as e:
        return {"error": str(e)}
    
    finally:
        driver.quit()

@app.route('/', methods=['GET'])
def homePage():
    return jsonify({"Page": "Home Page navigate to request page", "Time Stamp": time.time()})

@app.route('/download_advisory', methods=['POST'])
def downloadAdvisory():
    stateQuery = request.form.get('state')
    districtQuery = request.form.get('district')
    languageQuery = request.form.get('language')

    if not stateQuery or not districtQuery or not languageQuery:
        return jsonify({"error": "Missing form parameters"})
    
    try:
        response = script(stateQuery, districtQuery, languageQuery)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
