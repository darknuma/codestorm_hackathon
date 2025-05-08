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


def run_generator():
	"""Run the main data generator script."""
	generator_path = os.path.join('data_assets', 'data_gen.py')
	if not os.path.exists(generator_path):
		raise FileNotFoundError(f'Generator script not found at {generator_path}')

	spec = importlib.util.spec_from_file_location('generator', generator_path)
	generator = importlib.util.module_from_spec(spec)
	sys.modules['generator'] = generator
	spec.loader.exec_module(generator)

	# The generator module will automatically generate data when imported
	print('Running main data generator...')


def main():
	"""Execute the main application logic.

	This function serves as the entry point for the application,
	initializing and running the core components based on command line arguments.
	"""
	parser = argparse.ArgumentParser(description='AgriFinance Data Generation Tools')
	parser.add_argument(
		'helper',
		nargs='?',  # Make the argument optional
		choices=['cl', 'ds', 'gm'],
		help='Helper module to run (cl=Credit Lending, ds=Data Science, gm=General Model). If not provided, runs the main generator.',
	)
	parser.add_argument(
		'--num-farmers',
		type=int,
		default=4000,
		help='Number of farmers to generate (default: 4000)',
	)

	args = parser.parse_args()

	try:
		if args.helper is None:
			# No helper specified, run the main generator
			run_generator()
		else:
			# Import and run the selected helper module
			try:
				helper_module = import_helper_module(args.helper)

				# Each helper module has its own main function or data generation logic
				if args.helper == 'cl':
					# Credit Lending module
					print('Generating credit lending data...')
					try:
						# The module will automatically generate data when imported
						# If there's specific functionality to run, add it here
						if hasattr(helper_module, 'generate_data'):
							helper_module.generate_data()
					except Exception as e:
						print(f'Error in Credit Lending module: {e}')
						import traceback

						traceback.print_exc()

				elif args.helper == 'ds':
					# Data Science module
					print('Generating data science dataset...')
					try:
						farmers_df = helper_module.generate_farmers(args.num_farmers)
						print(f'\nGenerated dataset with {len(farmers_df)} farmers')
						print('\nSample of generated data:')
						print(farmers_df.head())
					except Exception as e:
						print(f'Error in Data Science module: {e}')
						import traceback

						traceback.print_exc()

				elif args.helper == 'gm':
					# General Model module
					print('Generating general model data...')
					try:
						if hasattr(helper_module, 'run') or hasattr(helper_module, 'generate_data'):
							func = getattr(helper_module, 'run', None) or getattr(
								helper_module, 'generate_data'
							)
							func()
					except Exception as e:
						print(f'Error in General Model module: {e}')
						import traceback

						traceback.print_exc()

			except Exception as e:
				print(f'Error importing helper module: {e}')
				import traceback

				traceback.print_exc()

	except Exception as e:
		print(f'Error running main module: {e}')
		import traceback

		traceback.print_exc()
		sys.exit(1)


if __name__ == '__main__':
	main()
