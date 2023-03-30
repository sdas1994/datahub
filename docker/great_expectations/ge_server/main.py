# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
import great_expectations as gx
from great_expectations.cli.datasource import sanitize_yaml_and_save_datasource, check_if_datasource_name_exists
from great_expectations.core.batch import BatchRequest
import yaml
import json
context = gx.get_context()
from types import SimpleNamespace
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
from DataQuality import DataQuality

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	return 'Welcome to GE for datahub'

# @app.route('/set_expectation', methods=['POST'])
# def set_expectation():
# 	content = request.get_json(silent=True)
# 	datasource_yaml = content['datasource_yaml']
# 	expectation_config = content['expectation_config']
# 	root_directory = content['root_directory']
# 	dq_checker = DataQuality(root_directory,  datasource_yaml,expectation_config)
# 	dq_checker.create_expectation_suite_if_not_exist()
# 	print (dq_checker.get_expectation_suit())
	
# 	return "expectation_created"


@app.route('/run_expectation', methods=['POST'])
def run_expectation():
	content = request.get_json(silent=True)
	datasource_yaml = content['datasource_yaml']
	expectation_config = content['expectation_config']
	root_directory = content['root_directory']
	dq_checker = DataQuality(root_directory,  datasource_yaml,expectation_config)
	dq_checker.create_expectation_suite_if_not_exist()
	validator = dq_checker.get_validator(with_profiled=False)

	result = dq_checker.validate_data()
	return 'expectation run completed'




# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run(host="0.0.0.0", port=5000, debug=True)


