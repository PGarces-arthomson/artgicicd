import ast
import re
import sys


def check_version(filename):
    """
    Checks the version formatting on all manifest.
    """
    try:
        with open(filename, encoding="utf-8") as f:
            content = f.read()
            module_info = ast.literal_eval(content)
            version = module_info.get("version")

            warning_message = ""
            print(version)
            if not version:
                warning_message = f"Error: 'version' key not found in {filename}"

            # Check if the version matches a semantic versioning pattern
            # ([version.0].major.minor.patch)
            # Example: 18.0.1.0.1
            version_pattern = re.compile(r"^18+\.\d+\.\d+\.\d+\.\d+$")

            if not version_pattern.match(version):
                warning_message = (
                    f"Error: Invalid version format '{version}' "
                    f"in {filename}. Expected format: [version.0].major.minor.patch"
                )

            if warning_message:
                print(warning_message)
                return 1

            print(f"Version '{version}' in {filename} is valid.")
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
        print("Usage: python check_manifest_version.py <manifest_file>")
        sys.exit(1)

    manifest_file = sys.argv[1]
    EXIT_CODE = check_version(manifest_file)
    sys.exit(EXIT_CODE)
