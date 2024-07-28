from flask import Flask, request, jsonify
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)

def script(state, commodity):
    initial_url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
    driver = webdriver.Chrome()

    try:
        driver.get(initial_url)
        
        # Select commodity
        commodity_dropdown = Select(driver.find_element(By.ID, 'ddlCommodity'))
        commodity_dropdown.select_by_visible_text(commodity)
        
        # Select state
        state_dropdown = Select(driver.find_element(By.ID, 'ddlState'))
        state_dropdown.select_by_visible_text(state)
        
        # Set date to the previous day
        today = datetime.now()
        previous_day = today - timedelta(days=1)
        date_string = previous_day.strftime('%d-%b-%Y')
        print(f"Setting date to: {date_string}")  # Debugging step
        driver.execute_script(f"document.getElementById('txtDate').value = '{date_string}';")
        
        # Click 'Go' to load results
        go_button = driver.find_element(By.ID, 'btnGo')
        go_button.click()
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cphBody_GridPriceData'))
        )
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data_list = []
        for row in soup.find_all("tr"):
            data_list.append(row.text.replace("\n", "_").replace("  ", "").split("__"))
        
        # Process and format the data
        jsonList = []
        for i in data_list[4:len(data_list) - 1]:
            d = {
                "S.No": i[1],
                "City": i[2],
                "Commodity": i[4],
                "Min Prize": i[7],
                "Max Prize": i[8],
                "Model Prize": i[9],
                "Date": i[10]
            }
            jsonList.append(d)
        
        return jsonList
    
    except (NoSuchElementException, TimeoutException) as e:
        return {"error": str(e)}
    
    finally:
        driver.quit()

@app.route('/', methods=['GET'])
def homePage():
    return jsonify({"Page": "Home Page navigate to request page", "Time Stamp": time.time()})

@app.route('/request', methods=['GET'])
def requestPage():
    commodityQuery = request.args.get('commodity')
    stateQuery = request.args.get('state')

    if not commodityQuery or not stateQuery:
        return jsonify({"error": "Missing query parameters"})
    
    try:
        json_data = json.dumps(script(stateQuery, commodityQuery), indent=4)
        return json_data
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
