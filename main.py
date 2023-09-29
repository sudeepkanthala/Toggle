from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('rides-3690-54c38a55b410.json', scope)
client = gspread.authorize(creds)

# Replace sheet names as needed
toggle_sheet = client.open('Toggle').sheet1


# Open your Google Sheet
sheet = client.open('Toggle').sheet1

@app.route('/')
def index():
    # Read data from the Google Sheet
    data = sheet.get_all_records()
    return render_template('index.html', data=data)

@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        # Process the booking form data and add it to the Google Sheet
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        users = request.form['users']

        # Add the data to the Google Sheet
        new_data = [date, time, location, users]
        sheet.append_row(new_data)

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
