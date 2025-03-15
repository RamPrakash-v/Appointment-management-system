from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Store appointments (date + time for checking availability)
appointments = []

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <title>Healthcare Appointment System</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: url('/static/images/ss.jpg') no-repeat center center/cover;
                color: #fff;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
            }

            h1 {
                font-size: 3em;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            }

            .container {
                background: rgba(0, 0, 0, 0.6);
                padding: 2em;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
                width: 90%;
                max-width: 600px;
                animation: fadeIn 1.5s ease-in-out;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }

            input, textarea {
                width: 90%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 8px;
            }

            button {
                padding: 12px 24px;
                margin: 10px;
                background: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.3s;
            }

            button:hover {
                background: #218838;
            }

            .view-btn {
                background: #007bff;
            }

            .view-btn:hover {
                background: #0056b3;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Healthcare Appointment System</h1>

            <!-- Appointment Form -->
            <form action="/book" method="POST">
                <input type="text" name="name" placeholder="Your Full Name" required>
                <input type="email" name="email" placeholder="Your Email Address" required>
                <input type="date" name="date" required>
                <input type="time" name="time" required>
                <textarea name="reason" placeholder="Reason for Appointment" rows="3" required></textarea>
                <button type="submit">Book Appointment</button>
            </form>

            <!-- View Appointments -->
            <form action="/appointments">
                <button type="submit" class="view-btn">View Scheduled Appointments</button>
            </form>
        </div>
    </body>

    </html>
    '''

@app.route('/book', methods=['POST'])
def book():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')
    time = request.form.get('time')
    reason = request.form.get('reason')

    # Check if the slot is already booked
    if any(appt['date'] == date and appt['time'] == time for appt in appointments):
        return '''
        <script>
            alert("❌ Slot already booked! Please choose another time.");
            window.location.href = "/";
        </script>
        '''

    # Store appointment if slot is available
    appointments.append({
        'name': name,
        'email': email,
        'date': date,
        'time': time,
        'reason': reason
    })

    return '''
    <script>
        alert("✅ Appointment Successful!");
        window.location.href = "/";
    </script>
    '''

@app.route('/appointments')
def view_appointments():
    appointment_list = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>View Appointments</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: #20232a;
                color: #fff;
                text-align: center;
                padding: 20px;
            }

            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }

            table {
                width: 90%;
                margin: 0 auto;
                border-collapse: collapse;
            }

            th, td {
                padding: 12px;
                border-bottom: 1px solid #444;
            }

            th {
                background: #282c34;
            }

            .back-btn, .clear-btn {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 24px;
                text-decoration: none;
                color: white;
                border-radius: 8px;
                transition: background 0.3s;
            }

            .back-btn:hover { background: #0056b3; }
            .clear-btn { background: #dc3545; }
            .clear-btn:hover { background: #c82333; }
        </style>
    </head>

    <body>
        <h1>Scheduled Appointments</h1>
        <table>
            <tr><th>Name</th><th>Email</th><th>Date</th><th>Time</th><th>Reason</th></tr>
    '''

    if not appointments:
        appointment_list += '<tr><td colspan="5">No appointments available.</td></tr>'
    else:
        for appt in appointments:
            appointment_list += f"""
            <tr><td>{appt['name']}</td><td>{appt['email']}</td><td>{appt['date']}</td><td>{appt['time']}</td><td>{appt['reason']}</td></tr>
            """

    appointment_list += '''
        </table>
        <a href="/" class="back-btn">Back to Home</a>
        <a href="/clear" class="clear-btn">Clear All Appointments</a>
    </body></html>
    '''
    return appointment_list

@app.route('/clear')
def clear_appointments():
    appointments.clear()
    return redirect(url_for('view_appointments'))

if __name__ == '__main__':
    app.run(debug=True)
