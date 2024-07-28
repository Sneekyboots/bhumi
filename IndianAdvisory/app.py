from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

def download_pdf(state, district):
    # Path to the chromedriver executable
    chromedriver_path = 'path/to/chromedriver'  # Update this path as needed

    # Set up Selenium WebDriver with options
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()

    # Instantiate the WebDriver with the service and options
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the target page
        driver.get("https://kvk.icar.gov.in/agromet_advisory.aspx")

        # Wait for the page to load and the form to be available
        wait = WebDriverWait(driver, 10)

        # Fill out the form (adjust the selectors as needed)
        state_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlState")))
        state_dropdown.send_keys(state)

        district_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlDistrict")))
        district_dropdown.send_keys(district)

        # Submit the form to download the PDF
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btn")))
        submit_button.click()

        # Wait for the download to complete (adjust the wait time as needed)
        time.sleep(10)

        # Return a success message
        return {"status": "success", "message": "PDF download initiated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        # Close the browser
        driver.quit()

@app.route('/download_advisory', methods=['POST'])
def download_advisory_route():
    data = request.json
    state = data.get('state')
    district = data.get('district')

    if not state or not district:
        return jsonify({"status": "error", "message": "State and district are required."}), 400

    result = download_pdf(state, district)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
