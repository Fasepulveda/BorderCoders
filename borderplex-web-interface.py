# app.py - Flask Web Interface for Borderplex RFI Accelerator

from flask import Flask, render_template, request, send_file, jsonify
from borderplex_rfi_accelerator import BorderplexRFIAccelerator
import os
import json

app = Flask(__name__)
accelerator = BorderplexRFIAccelerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_rfi', methods=['POST'])
def process_rfi():
    # Get the prompt from the form
    prompt = request.form.get('prompt', '')
    
    # Process the request
    parameters = accelerator.parse_request(prompt)
    response = accelerator.generate_rfi_response(parameters)
    
    # Store the response in a session file
    with open('temp_response.json', 'w') as f:
        json.dump(response, f)
    
    # Return JSON response
    return jsonify({
        'parameters': parameters,
        'economic_impact': response['economic_impact']
    })

@app.route('/download_pdf')
def download_pdf():
    # Load the stored response
    with open('temp_response.json', 'r') as f:
        response = json.load(f)
    
    # Generate PDF
    pdf_file = accelerator.export_to_pdf(response)
    
    # Send the file
    return send_file(pdf_file, as_attachment=True)

@app.route('/download_json')
def download_json():
    # Load the stored response
    with open('temp_response.json', 'r') as f:
        response = json.load(f)
    
    # Generate JSON
    json_file = accelerator.export_to_json(response)
    
    # Send the file
    return send_file(json_file, as_attachment=True)

@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    # Get the updated parameters
    data = request.json
    
    # Load the stored response
    with open('temp_response.json', 'r') as f:
        response = json.load(f)
    
    # Update the parameters
    parameters = {
        'industry': data.get('industry', response['project_summary']['industry'].lower()),
        'employees': int(data.get('employees', response['project_summary']['employment'])),
        'location': data.get('location', response['project_summary']['location']),
        'capex': int(data.get('capex', response['project_summary']['capex']))
    }
    
    # Generate new response
    updated_response = accelerator.generate_rfi_response(parameters)
    
    # Store the updated response
    with open('temp_response.json', 'w') as f:
        json.dump(updated_response, f)
    
    # Return the updated economic impact
    return jsonify({
        'economic_impact': updated_response['economic_impact']
    })

if __name__ == '__main__':
    app.run(debug=True)
