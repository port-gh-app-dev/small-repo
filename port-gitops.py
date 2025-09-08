#!/usr/bin/env python3
import yaml
import sys
import copy

def main():
    """
    Reads the first YAML document from port.yml and generates 5000 documents
    back into the file, each with a unique identifier.
    """
    try:
        with open('port.yml', 'r') as f:
            # Load only the first document from port.yml to use as a template
            original_doc = next(yaml.safe_load_all(f))
    except FileNotFoundError:
        print("Error: port.yml not found.", file=sys.stderr)
        sys.exit(1)
    except StopIteration:
        print("Error: port.yml is empty or not a valid YAML file.", file=sys.stderr)
        sys.exit(1)

    original_identifier = original_doc.get('identifier')

    if not original_identifier:
        print("Error: 'identifier' key not found in the first document of port.yml", file=sys.stderr)
        sys.exit(1)

    with open('port.yml', 'w') as f:
        for i in range(1, 5001):
            if i > 1:
                f.write('---\n')

            # Use deepcopy to ensure nested structures are not shared between documents
            new_doc = copy.deepcopy(original_doc)
            new_doc['identifier'] = f"{original_identifier}-{i}"

            yaml.dump(new_doc, f, sort_keys=False)

if __name__ == "__main__":
    main()
