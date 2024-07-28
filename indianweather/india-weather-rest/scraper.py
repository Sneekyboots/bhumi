import requests
from bs4 import BeautifulSoup

def get_station_data(id):
    URL = 'https://city.imd.gov.in/citywx/city_weather_test_try.php?id={}'.format(id)

    try:
        response = requests.get(URL, verify=False)  # Use verify=True in production
        response.raise_for_status()  # Raises HTTPError for bad responses
        html_text = response.text

        soup = BeautifulSoup(html_text, 'html.parser')

        cells = soup.find_all('td')
        # Ensure that the index accesses match the data structure
        max_temp = cells[4].text.strip()
        max_dep = cells[6].text.strip()
        min_temp = cells[8].text.strip()
        min_dep = cells[10].text.strip()
        rh_0830 = cells[14].text.strip()
        rh_1730 = cells[16].text.strip()
        sunrise = cells[20].text.strip()
        sunset = cells[18].text.strip()
        moonrise = cells[24].text.strip()
        moonset = cells[22].text.strip()

        forecast = []
        for i in range(31, 65, 10):  # Ensure this range is correct
            day_data = {
                'day': (i - 31) // 10 + 1,
                'date': cells[i].font.text.strip(),
                'max': float(cells[i + 2].font.text.strip()),
                'min': float(cells[i + 1].font.text.strip()),
                'condition': cells[i + 4].font.text.strip()
            }
            forecast.append(day_data)

        return {
            'temperature': {
                'max': {
                    'value': float(max_temp),
                    'departure': float(max_dep)
                },
                'min': {
                    'value': float(min_temp),
                    'departure': float(min_dep)
                }
            },
            'humidity': {
                'morning': float(rh_0830),
                'evening': float(rh_1730)
            },
            'astronomical': {
                'sunrise': sunrise,
                'sunset': sunset,
                'moonrise': moonrise,
                'moonset': moonset
            },
            'forecast': forecast
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for station {id}: {e}")
        return {"error": "Failed to retrieve weather data", "message": str(e)}
