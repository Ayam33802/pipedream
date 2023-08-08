import os
import argparse
import templates.generate_actions
import templates.generate_webhook_sources


available_templates = {
    'action': templates.generate_actions,
    'webhook_source': templates.generate_webhook_sources,
}


def main(component_type, app, instructions, verbose=False):
    if verbose:
        os.environ['DEBUG'] = '1'

    try:
        templates = available_templates[component_type]
    except:
        raise ValueError(f'Templates for {component_type}s are not available. Please choose one of {available_templates.keys()}')

    # this is here so that the DEBUG environment variable is set before the import
    from code_gen.generate_component_code import generate_code
    result = generate_code(app, instructions, templates)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--component_type', help='which kind of code you want to generate?', choices=available_templates.keys(), required=True)
    parser.add_argument('--app', help='the app_name_slug', required=True)
    parser.add_argument('--instructions', help='markdown file with instructions: prompt + api docs', required=True)
    parser.add_argument('--verbose', dest='verbose', help='set the logging to debug', required=False, default=False, action='store_true')
    args = parser.parse_args()

    with open(args.instructions, 'r') as f:
        instructions = f.read()

    result = main(args.component_type, args.app, instructions, args.verbose)
    print(result)