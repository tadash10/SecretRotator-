import argparse
import datetime
import os
import subprocess

# DISCLAIMER: This script is provided "as is" and without warranty of any kind. 
# Use at your own risk. The author shall not be liable for any damages arising from the use of this script.

def check_tool(tool):
    """
    Checks if a given tool is installed and available in the PATH.
    """
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call([tool, '--version'], stdout=devnull, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print(f"{tool} not found. Please make sure {tool} is installed and available in the PATH.", file=sys.stderr)
        sys.exit(1)

def rotate_secrets(secret_path):
    """
    Rotates the secrets stored at the specified path using a secret management tool.
    """
    # Check that the secret management tool is installed
    check_tool('vault')

    # Generate a new secret
    new_secret = subprocess.check_output(['openssl', 'rand', '-base64', '32']).decode().strip()

    # Store the new secret using the secret management tool
    subprocess.check_call(['vault', 'kv', 'put', secret_path, f'secret={new_secret}'])

def main():
    parser = argparse.ArgumentParser(description="Automate the process of rotating secrets such as API keys, passwords, and access tokens")
    parser.add_argument("secret_path", metavar="PATH", type=str,
                        help="Path to the secret to rotate")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be done, but do not actually perform the rotation")
    args = parser.parse_args()

    if args.dry_run:
        print(f"Would rotate secret at {args.secret_path}")
    else:
        rotate_secrets(args.secret_path)
        print(f"Rotated secret at {args.secret_path}")

if __name__ == '__main__':
    main()
