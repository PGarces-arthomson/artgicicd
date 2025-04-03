import ast
import re
import sys

ARTGI_BRANDING = {
    "author": "A.R. Thomson Group Inc",
    "category": "A.R. Customization",
    "website": "https://www.arthomson.com/",
}
DOCSTRING = """
# This module provides features specifically tailored to the
# internal operations and proprietary needs of A.R. Thomson Group Inc.
# It is not intended for public distribution or general use.

# See LICENSE file for full copyright and licensing details."""


def format_manifest(filename):
    """
    Re-order manifest keys
    """

    def _format_list(value, tab="        "):
        formatted_value = "[\n"
        for dep in value:
            formatted_value = tab.join([formatted_value, f'"{dep}",' f"\n"])
        formatted_value += "        ]"
        return formatted_value

    def _format_value(value):
        return re.sub(r"'([^']*)'", r'"\1"', repr(value))

    try:
        with open(filename, encoding="utf-8") as f:
            content = f.read()

        # Safely parse the Python dictionary using ast
        module_info = ast.literal_eval(content)

        # Define the desired order of keys
        preferred_order = [
            "name",
            "version",
            "summary",
            "description",
            "author",
            "maintainer",
            "website",
            "license",
            "category",
            "depends",
            "images",
            "data",
            "assets",
            "css",
            "js",
            "demo",
            "auto_install",
            "installable",
            "application",
            "sequence",
            "external_dependencies",
            "qweb",
            "pre_init_hook",
            "post_init_hook",
            "uninstall_hook",
            "support",
            "price",
            "currency",
            "live_test_url",
        ]

        ordered_manifest = {}

        # Add keys in the preferred order
        for key in preferred_order:
            if key in module_info:
                ordered_manifest[key] = module_info.pop(key)

        # Add any remaining keys that are not in the preferred order (preserve them)
        for key in sorted(module_info.keys()):
            ordered_manifest[key] = module_info[key]

        # Format the output with consistent indentation and sorting
        formatted_content = "{\n"
        tab = "        "
        for key, value in ordered_manifest.items():
            if key in ["data", "depends", "images"] and isinstance(value, list):
                formatted_value = _format_list(value, tab)
            elif key in ["assets"] and isinstance(value, dict):
                formatted_value = "{\n"
                # Expected dictionary: {key: [vals]}
                for vkey, vval in value.items():
                    formatted_vval = _format_list(vval, tab="            ")
                    formatted_value = "".join(
                        [formatted_value, f'{tab}"{vkey}": ' f"{formatted_vval}," f"\n"]
                    )

                formatted_value = "".join([formatted_value, tab, "}"])
            else:
                orig_val = ARTGI_BRANDING.get(key) or value
                formatted_value = _format_value(orig_val)

            formatted_content += f'   "{key}": {formatted_value},\n'
        formatted_content += "}"

        # Remove trailing comma if present (for cleaner diffs)
        formatted_content = formatted_content.replace(",\n}", "\n}\n")

        # Write the sorted content back to the file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{DOCSTRING}\n" + formatted_content)

        return 0

    except FileNotFoundError:
        print(f"Error: Manifest file not found: {filename}")
        return 1
    except SyntaxError:
        print(f"Error: Syntax error in manifest file: {filename}")
        return 1
    except ValueError:
        print(
            f"Error: Could not parse manifest file as a Python dictionary: {filename}"
        )
        return 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python format_manifest.py <manifest_file>")
        sys.exit(1)

    manifest_file = sys.argv[1]
    EXIT_CODE = format_manifest(manifest_file)
    sys.exit(EXIT_CODE)
