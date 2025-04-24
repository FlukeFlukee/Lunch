from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    total = 0

    if request.method == 'POST':
        players = request.form.getlist('name')
        hours = request.form.getlist('hours')
        court_rate = float(request.form.get('court_rate', 0))
        shuttle_price = float(request.form.get('shuttle_price', 0))
        shuttle_used = int(request.form.get('shuttle_used', 0))

        hours_float = [float(h) for h in hours]
        total_hours = sum(hours_float)
        court_total = court_rate * total_hours
        shuttle_total = shuttle_price * shuttle_used

        for name, hour in zip(players, hours_float):
            share_ratio = hour / total_hours if total_hours else 0
            court_fee = share_ratio * court_total
            shuttle_fee = shuttle_total / len(players) if players else 0
            total_fee = court_fee + shuttle_fee
            result.append({
                'name': name,
                'hours': hour,
                'court_fee': round(court_fee, 2),
                'shuttle_fee': round(shuttle_fee, 2),
                'total_fee': round(total_fee, 2),
            })

        total = round(court_total + shuttle_total, 2)

    return render_template('index.html', result=result, total=total)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
