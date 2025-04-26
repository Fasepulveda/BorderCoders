# Borderplex RFI Accelerator - Simple Implementation

import json
import re
import os
import datetime
from fpdf import FPDF
import pandas as pd

class BorderplexRFIAccelerator:
    def __init__(self):
        # Load mock data sources
        self.load_data()
        
    def load_data(self):
        """Load mock data from JSON files (in a real implementation, this would connect to APIs and databases)"""
        # Labor data
        self.labor_data = {
            "El Paso": {
                "manufacturing_workforce": 42500,
                "average_wage": 18.75,
                "unemployment_rate": 4.2,
                "stem_graduates_yearly": 3200
            },
            "Las Cruces": {
                "manufacturing_workforce": 12800,
                "average_wage": 17.50,
                "unemployment_rate": 4.5,
                "stem_graduates_yearly": 1800
            },
            "Juarez": {
                "manufacturing_workforce": 280000,
                "average_wage": 6.25,
                "unemployment_rate": 3.2,
                "stem_graduates_yearly": 4500
            }
        }
        
        # Real estate data
        self.real_estate_data = {
            "El Paso": {
                "industrial_sqft_available": 2500000,
                "avg_lease_rate": 5.75,
                "avg_land_cost": 3.25,
                "major_industrial_parks": ["West Texas Industrial Park", "El Paso Logistics Park", "Mission Industrial Park"]
            },
            "Las Cruces": {
                "industrial_sqft_available": 850000,
                "avg_lease_rate": 5.25,
                "avg_land_cost": 2.75,
                "major_industrial_parks": ["West Mesa Industrial Park", "Las Cruces Innovation & Industrial Park"]
            },
            "Juarez": {
                "industrial_sqft_available": 3800000,
                "avg_lease_rate": 4.50,
                "avg_land_cost": 2.25,
                "major_industrial_parks": ["Juarez Industrial Park", "Bermudez Industrial Park", "San Jeronimo Park"]
            }
        }
        
        # Incentives data
        self.incentives_data = {
            "El Paso": {
                "property_tax_abatement": "Up to 100% abatement for 10 years",
                "job_training_grants": "Up to $2,500 per employee",
                "infrastructure_grants": "Case-by-case basis",
                "foreign_trade_zone": True
            },
            "Las Cruces": {
                "property_tax_abatement": "Up to 90% abatement for 20 years",
                "job_training_grants": "Up to $3,000 per employee",
                "infrastructure_grants": "$500,000 maximum",
                "foreign_trade_zone": True
            },
            "Juarez": {
                "property_tax_abatement": "Up to 100% for 5 years",
                "job_training_grants": "Up to $1,500 per employee",
                "infrastructure_grants": "Case-by-case basis",
                "foreign_trade_zone": True
            }
        }
        
        # Cross-border data
        self.cross_border_data = {
            "border_crossings": {
                "commercial_crossings_daily": 2800,
                "crossing_wait_times_avg": "45 minutes",
                "maquiladora_facilities": 330,
            },
            "trade_data": {
                "annual_trade_value": "$82 billion",
                "main_industries": ["Automotive", "Electronics", "Medical Devices", "Aerospace"],
                "duty_free_programs": ["USMCA", "IMMEX"]
            }
        }
        
        # Industry multipliers for economic impact calculations
        self.industry_multipliers = {
            "automotive": {
                "jobs_multiplier": 2.8,
                "income_multiplier": 1.9,
                "tax_revenue_per_job": 3200
            },
            "electronics": {
                "jobs_multiplier": 2.5,
                "income_multiplier": 1.7,
                "tax_revenue_per_job": 2800
            },
            "medical": {
                "jobs_multiplier": 2.1,
                "income_multiplier": 1.8,
                "tax_revenue_per_job": 3500
            },
            "aerospace": {
                "jobs_multiplier": 3.2,
                "income_multiplier": 2.1,
                "tax_revenue_per_job": 4200
            },
            "manufacturing": {
                "jobs_multiplier": 2.3,
                "income_multiplier": 1.6,
                "tax_revenue_per_job": 2500
            },
            "logistics": {
                "jobs_multiplier": 1.9,
                "income_multiplier": 1.4,
                "tax_revenue_per_job": 2200
            },
            "technology": {
                "jobs_multiplier": 2.7,
                "income_multiplier": 2.0,
                "tax_revenue_per_job": 3800
            }
        }
    
    def parse_request(self, prompt):
        """Parse natural language prompt to extract key parameters"""
        # Simple regex-based parameter extraction (in a real implementation, this would use NLP)
        
        parameters = {
            "industry": "manufacturing",  # Default values
            "employees": 100,
            "location": "El Paso",
            "capex": 10000000
        }
        
        # Extract industry
        industry_match = re.search(r'(automotive|electronics|medical|aerospace|manufacturing|logistics|technology)', prompt.lower())
        if industry_match:
            parameters["industry"] = industry_match.group(1)
            
        # Extract employee count
        employee_match = re.search(r'(\d+)[ -]employee', prompt)
        if employee_match:
            parameters["employees"] = int(employee_match.group(1))
            
        # Extract location preference
        location_match = re.search(r'(El Paso|Las Cruces|Juarez)', prompt)
        if location_match:
            parameters["location"] = location_match.group(1)
            
        # Extract capex if provided
        capex_match = re.search(r'\$(\d+)[ -]million', prompt)
        if capex_match:
            parameters["capex"] = int(capex_match.group(1)) * 1000000
        
        return parameters
    
    def calculate_economic_impact(self, parameters):
        """Calculate economic impact based on input parameters"""
        industry = parameters["industry"]
        employees = parameters["employees"]
        capex = parameters["capex"]
        
        # Get multipliers for the industry (default to manufacturing if not found)
        multipliers = self.industry_multipliers.get(industry, self.industry_multipliers["manufacturing"])
        
        # Calculate impacts
        impact = {
            "direct_jobs": employees,
            "indirect_jobs": int(employees * multipliers["jobs_multiplier"]),
            "total_jobs": int(employees * (1 + multipliers["jobs_multiplier"])),
            "annual_payroll": employees * self.labor_data[parameters["location"]]["average_wage"] * 2080,  # 2080 = work hours per year
            "total_economic_output": employees * self.labor_data[parameters["location"]]["average_wage"] * 2080 * multipliers["income_multiplier"] + capex,
            "tax_revenue": employees * multipliers["tax_revenue_per_job"],
            "capex": capex
        }
        
        return impact
    
    def generate_rfi_response(self, parameters):
        """Generate complete RFI response package"""
        impact = self.calculate_economic_impact(parameters)
        
        response = {
            "project_summary": {
                "industry": parameters["industry"].capitalize(),
                "employment": parameters["employees"],
                "location": parameters["location"],
                "capex": parameters["capex"]
            },
            "workforce_analysis": {
                "available_workforce": self.labor_data[parameters["location"]]["manufacturing_workforce"],
                "average_wage": self.labor_data[parameters["location"]]["average_wage"],
                "unemployment_rate": self.labor_data[parameters["location"]]["unemployment_rate"],
                "stem_graduates": self.labor_data[parameters["location"]]["stem_graduates_yearly"]
            },
            "real_estate_options": self.real_estate_data[parameters["location"]],
            "incentives": self.incentives_data[parameters["location"]],
            "cross_border_advantages": self.cross_border_data,
            "economic_impact": impact,
            "generation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return response
    
    def export_to_pdf(self, response, output_file="borderplex_rfi_response.pdf"):
        """Export RFI response to PDF format"""
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Borderplex RFI Response: {response['project_summary']['industry']} Project", ln=True, align="C")
        pdf.ln(5)
        
        # Project Summary
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Project Summary", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"Industry: {response['project_summary']['industry']}")
        pdf.multi_cell(0, 6, f"Employment: {response['project_summary']['employment']} jobs")
        pdf.multi_cell(0, 6, f"Location: {response['project_summary']['location']}")
        pdf.multi_cell(0, 6, f"Capital Investment: ${response['project_summary']['capex']:,}")
        pdf.ln(5)
        
        # Workforce Analysis
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Workforce Analysis", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"Available Workforce in Target Sector: {response['workforce_analysis']['available_workforce']:,}")
        pdf.multi_cell(0, 6, f"Average Wage: ${response['workforce_analysis']['average_wage']:.2f}/hour")
        pdf.multi_cell(0, 6, f"Current Unemployment Rate: {response['workforce_analysis']['unemployment_rate']}%")
        pdf.multi_cell(0, 6, f"Annual STEM Graduates: {response['workforce_analysis']['stem_graduates']}")
        pdf.ln(5)
        
        # Real Estate Options
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Real Estate Options", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"Industrial Space Available: {response['real_estate_options']['industrial_sqft_available']:,} sq ft")
        pdf.multi_cell(0, 6, f"Average Lease Rate: ${response['real_estate_options']['avg_lease_rate']:.2f}/sq ft")
        pdf.multi_cell(0, 6, f"Average Land Cost: ${response['real_estate_options']['avg_land_cost']:.2f}/sq ft")
        pdf.multi_cell(0, 6, f"Major Industrial Parks: {', '.join(response['real_estate_options']['major_industrial_parks'])}")
        pdf.ln(5)
        
        # Incentives
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Available Incentives", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"Property Tax Abatement: {response['incentives']['property_tax_abatement']}")
        pdf.multi_cell(0, 6, f"Job Training Grants: {response['incentives']['job_training_grants']}")
        pdf.multi_cell(0, 6, f"Infrastructure Grants: {response['incentives']['infrastructure_grants']}")
        pdf.multi_cell(0, 6, f"Foreign Trade Zone: {'Available' if response['incentives']['foreign_trade_zone'] else 'Not Available'}")
        pdf.ln(5)
        
        # Cross-Border Advantages
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Cross-Border Advantages", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"Daily Commercial Border Crossings: {response['cross_border_advantages']['border_crossings']['commercial_crossings_daily']}")
        pdf.multi_cell(0, 6, f"Average Wait Times: {response['cross_border_advantages']['border_crossings']['crossing_wait_times_avg']}")
        pdf.multi_cell(0, 6, f"Maquiladora Facilities: {response['cross_border_advantages']['border_crossings']['maquiladora_facilities']}")
        pdf.multi_cell(0, 6, f"Annual Trade Value: {response['cross_border_advantages']['trade_data']['annual_trade_value']}")
        pdf.ln(5)
        
        # Economic Impact
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Economic Impact Analysis", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"Direct Jobs: {response['economic_impact']['direct_jobs']:,}")
        pdf.multi_cell(0, 6, f"Indirect Jobs: {response['economic_impact']['indirect_jobs']:,}")
        pdf.multi_cell(0, 6, f"Total Jobs: {response['economic_impact']['total_jobs']:,}")
        pdf.multi_cell(0, 6, f"Annual Payroll: ${response['economic_impact']['annual_payroll']:,.2f}")
        pdf.multi_cell(0, 6, f"Total Economic Output: ${response['economic_impact']['total_economic_output']:,.2f}")
        pdf.multi_cell(0, 6, f"Estimated Annual Tax Revenue: ${response['economic_impact']['tax_revenue']:,.2f}")
        pdf.ln(5)
        
        # Footer
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, f"Generated on {response['generation_date']} by Borderplex RFI Accelerator", ln=True, align="C")
        
        pdf.output(output_file)
        return output_file

    def export_to_json(self, response, output_file="borderplex_rfi_response.json"):
        """Export RFI response to JSON format"""
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=2)
        return output_file

# Simple command-line interface for the system
def main():
    accelerator = BorderplexRFIAccelerator()
    
    print("Welcome to the Borderplex RFI Accelerator")
    print("----------------------------------------")
    print("Enter your RFI request in natural language:")
    print("Example: Generate an RFI for a 200-employee automotive supplier in El Paso")
    
    while True:
        prompt = input("\nRFI Request (or 'exit' to quit): ")
        
        if prompt.lower() == 'exit':
            break
            
        start_time = datetime.datetime.now()
        
        # Process the request
        parameters = accelerator.parse_request(prompt)
        
        # Display extracted parameters
        print("\nExtracted parameters:")
        print(f"Industry: {parameters['industry']}")
        print(f"Employees: {parameters['employees']}")
        print(f"Location: {parameters['location']}")
        print(f"Capital Investment: ${parameters['capex']:,}")
        
        # Generate response
        response = accelerator.generate_rfi_response(parameters)
        
        # Calculate processing time
        processing_time = (datetime.datetime.now() - start_time).total_seconds()
        
        print(f"\nRFI response generated in {processing_time:.2f} seconds!")
        
        # Export options
        print("\nExport options:")
        print("1. Export to PDF")
        print("2. Export to JSON")
        print("3. Skip export")
        
        export_choice = input("Choose export format (1-3): ")
        
        if export_choice == '1':
            pdf_file = accelerator.export_to_pdf(response)
            print(f"PDF exported to {pdf_file}")
        elif export_choice == '2':
            json_file = accelerator.export_to_json(response)
            print(f"JSON exported to {json_file}")

        # Display economic impact summary
        print("\nEconomic Impact Summary:")
        print(f"Direct Jobs: {response['economic_impact']['direct_jobs']:,}")
        print(f"Indirect Jobs: {response['economic_impact']['indirect_jobs']:,}")
        print(f"Total Jobs: {response['economic_impact']['total_jobs']:,}")
        print(f"Annual Payroll: ${response['economic_impact']['annual_payroll']:,.2f}")
        print(f"Total Economic Output: ${response['economic_impact']['total_economic_output']:,.2f}")
        print(f"Estimated Annual Tax Revenue: ${response['economic_impact']['tax_revenue']:,.2f}")

if __name__ == "__main__":
    main()
