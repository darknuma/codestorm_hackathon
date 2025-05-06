"""Main module for the AgriFinance project.

This module serves as the entry point for the application and contains
the main function that orchestrates the application flow.
"""

import argparse
import importlib.util
import os
import sys


def import_helper_module(module_name):
	"""Import a helper module dynamically.

	Args:
	    module_name (str): Name of the helper module to import

	Returns:
	    module: The imported module
	"""
	module_path = os.path.join('data_assets', f'helper_{module_name}.py')
	if not os.path.exists(module_path):
		raise FileNotFoundError(f'Helper module {module_name} not found at {module_path}')

	spec = importlib.util.spec_from_file_location(f'helper_{module_name}', module_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[f'helper_{module_name}'] = module
	spec.loader.exec_module(module)
	return module


def main():
	"""Execute the main application logic.

	This function serves as the entry point for the application,
	initializing and running the core components based on command line arguments.
	"""
	parser = argparse.ArgumentParser(description='AgriFinance Data Generation Tools')
	parser.add_argument(
		'helper',
		choices=['cl', 'ds', 'gm'],
		help='Helper module to run (cl=Credit Lending, ds=Data Science, gm=General Model)',
	)
	parser.add_argument(
		'--num-farmers',
		type=int,
		default=4000,
		help='Number of farmers to generate (default: 4000)',
	)

	args = parser.parse_args()

	try:
		# Import and run the selected helper module
		helper_module = import_helper_module(args.helper)

		# Each helper module has its own main function or data generation logic
		if args.helper == 'cl':
			# Credit Lending module
			print('Generating credit lending data...')
			# The module will automatically generate data when imported

		elif args.helper == 'ds':
			# Data Science module
			print('Generating data science dataset...')
			farmers_df = helper_module.generate_farmers(args.num_farmers)
			print(f'\nGenerated dataset with {len(farmers_df)} farmers')
			print('\nSample of generated data:')
			print(farmers_df.head())

		elif args.helper == 'gm':
			# General Model module
			print('Generating general model data...')
			# The module will automatically generate data when imported

	except Exception as e:
		print(f'Error running helper module: {str(e)}')
		sys.exit(1)


if __name__ == '__main__':
	main()
