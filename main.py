import argparse
import logging
import requests
from github import Github

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_github_token():
    """
    Retrieves the GitHub token from the environment variable GITHUB_TOKEN.
    
    Returns:
        str: The GitHub token.
    """
    import os
    return os.environ.get('GITHUB_TOKEN')

def scan_license(repository):
    """
    Scans the license of a GitHub repository.
    
    Args:
        repository (str): The name of the repository (e.g., owner/repo).
    
    Returns:
        str: The license of the repository.
    """
    try:
        token = get_github_token()
        g = Github(token)
        repo = g.get_repo(repository)
        license = repo.get_license()
        return license.license.name
    except Exception as e:
        logging.error(f"Error scanning license: {e}")
        return None

def check_compliance(license):
    """
    Checks if the license is AGPL compliant.
    
    Args:
        license (str): The license of the repository.
    
    Returns:
        bool: True if the license is AGPL compliant, False otherwise.
    """
    return license == "AGPL-3.0"

def risk_assessment(repository):
    """
    Performs a risk assessment on a GitHub repository.
    
    Args:
        repository (str): The name of the repository (e.g., owner/repo).
    
    Returns:
        str: A risk assessment report.
    """
    try:
        license = scan_license(repository)
        if license:
            compliance = check_compliance(license)
            if compliance:
                return f"Repository {repository} is AGPL compliant."
            else:
                return f"Repository {repository} is not AGPL compliant."
        else:
            return f"Failed to retrieve license for repository {repository}."
    except Exception as e:
        logging.error(f"Error performing risk assessment: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='AGPL License Compliance Tool')
    parser.add_argument('--repository', help='GitHub repository (e.g., owner/repo)')
    parser.add_argument('--token', help='GitHub token')
    args = parser.parse_args()
    
    if args.repository:
        report = risk_assessment(args.repository)
        if report:
            print(report)
        else:
            print("Failed to generate report.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()