from flask import Flask, render_template, request
import os

app = Flask(__name__)
FLAG = "SC2{P0W3R_L3V3L_0V3R_9000_BURP_BYPASS}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    power_level = request.form.get('power_level', '')
    
    print(f"Received - Name: {name}, Power: {power_level}")
    
    # Simple server-side validation
    try:
        power_level_int = int(power_level)
        if power_level_int > 9000:
            # SUCCESS - They bypassed the client-side restriction via Burp
            return render_template('success.html', 
                                 name=name, 
                                 power_level=power_level_int,
                                 flag=FLAG)
        else:
            # FAILED - Power level too low (normal form submission)
            return render_template('failed.html', 
                                 name=name, 
                                 power_level=power_level_int,
                                 required_level=9000)
    except (ValueError, TypeError):
        return render_template('failed.html', 
                             name=name, 
                             power_level=0,
                             required_level=9000,
                             error="Invalid power level!")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=20001)
