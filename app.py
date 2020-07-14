import requests
import bs4
import pandas
from flask import Flask,render_template

app=Flask(__name__)

webUrl = "https://kathmandupost.com/covid19"

web_content = requests.get(webUrl).text

soup = bs4.BeautifulSoup(web_content, 'html.parser')

tableData = soup.find('table', class_="district-wrapper")

headings= []
for heading in tableData.find_all("th"):
    headings.append(heading.text)

statistics = []

for row in tableData.tbody.find_all("tr"):
    temp = []
    for column in row.find_all("td"):
        temp.append(column.text)

    statistics.append(temp)

district_data = pandas.DataFrame(data=statistics, columns=headings)

district_data['Confirmed'] = district_data['Confirmed'].map(int)
district_data['Deaths'] = district_data['Deaths'].map(int)
district_data['Recovered'] = district_data['Recovered'].map(int)
district_data['Readmitted'] = district_data['Readmitted'].map(int)

total = [sum(district_data['Confirmed']), sum(district_data['Deaths']), sum(district_data['Recovered']), sum(district_data['Readmitted'])]

@app.route('/')
def index():
    return render_template('index.html', total=total, districts=statistics)

if __name__ == "__main__":
    app.run(debug=True)
    

