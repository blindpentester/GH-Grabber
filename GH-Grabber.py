import argparse
import requests
import subprocess
import sys
import os
import shutil
import platform
import zipfile
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Function to print help guide and examples
def print_help():
    help_text = f"""
    {Fore.CYAN}GitHub Repo Downloader and Installer Script{Style.RESET_ALL}

    {Fore.CYAN}Usage:{Style.RESET_ALL}
        script.py -s <software_name>
        script.py -a <author_name>

    {Fore.CYAN}Arguments:{Style.RESET_ALL}
        -s, --software    Specify the software name to search for repositories.
        -a, --author      Specify the author name to find repositories by author.

    {Fore.CYAN}Examples:{Style.RESET_ALL}
        script.py -s example-software
        script.py -a example-author
    """
    print(help_text)

# Function to fetch repositories by author or by search term
def fetch_repos_by_search(search_term, search_by_author=False):
    if search_by_author:
        url = f"https://api.github.com/users/{search_term}/repos"
    else:
        url = f"https://api.github.com/search/repositories?q={search_term}"

    response = requests.get(url)
    
    if response.status_code == 200:
        if search_by_author:
            repos = response.json()
        else:
            repos = response.json().get('items', [])
        if len(repos) == 0:
            print(f"{Fore.YELLOW}[ (⊙_☉) ] No repositories found for '{search_term}'.{Style.RESET_ALL}")
            sys.exit(1)
        return repos
    else:
        print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] Failed to fetch repositories for '{search_term}'. HTTP Status Code: {response.status_code}{Style.RESET_ALL}")
        sys.exit(1)

# Function to select a repository
def select_repo(repos):
    try:
        print(f"{Fore.CYAN}\nSelect a repository by number:{Style.RESET_ALL}")
        for idx, repo in enumerate(repos):
            print(f"{Fore.GREEN}[ {idx+1} ] {repo['full_name']} (⭐ {repo['stargazers_count']}){Style.RESET_ALL}")
        
        choice = int(input(f"{Fore.CYAN}\nEnter the number of the repository you want to select: {Style.RESET_ALL}")) - 1
        if choice < 0 or choice >= len(repos):
            print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] Invalid selection. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
        
        return repos[choice]
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[ (⊙_☉) ] Selection process interrupted by user. Exiting...{Style.RESET_ALL}")
        sys.exit(1)
    except ValueError:
        print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] Invalid input. Please enter a valid number.{Style.RESET_ALL}")
        sys.exit(1)

# Function to fetch release information
def fetch_release(repo):
    url = f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        release = response.json()
        if len(release['assets']) == 0:
            print(f"{Fore.YELLOW}[ (⊙_☉) ] No releases found for this repository. Cloning instead...{Style.RESET_ALL}")
            clone_repository(repo)
            sys.exit(0)
        return release
    else:
        print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] Failed to fetch releases for {repo['name']}. HTTP Status Code: {response.status_code}{Style.RESET_ALL}")
        clone_repository(repo)
        sys.exit(0)

# Function to clone repository or pull latest changes if directory exists
def clone_repository(repo):
    repo_url = repo['clone_url']
    target_dir = repo['name']
    
    if os.path.exists(target_dir):
        print(f"{Fore.YELLOW}[ ಠ‿ಠ ] Directory '{target_dir}' already exists. Pulling latest changes...{Style.RESET_ALL}")
        subprocess.run(["git", "-C", target_dir, "pull"])
    else:
        print(f"{Fore.CYAN}[ ಠ‿ಠ ] Cloning {repo['name']}...{Style.RESET_ALL}")
        subprocess.run(["git", "clone", repo_url])


# Function to identify the correct asset based on OS and architecture
def select_asset(release, repo):
    system = platform.system().lower()
    architecture = platform.machine().lower()

    print(f"Detected system: {system}, architecture: {architecture}")

    # Log available assets for debugging
    for asset in release['assets']:
        print(f"Available asset: {asset['name']}")

    # Adjusted logic for matching assets
    for asset in release['assets']:
        asset_name = asset['name'].lower()
        if "linux" in asset_name and "amd64" in asset_name:
            return asset

    print(f"{Fore.YELLOW}[ ୧༼ಠ益ಠ༽୨ ] No suitable release found for {system} on {architecture}. Cloning repository instead...{Style.RESET_ALL}")
    clone_repository(repo)
    sys.exit(0)


# Function to download and install the software
def download_and_install(release, repo):
    # Pass both release and repo to select_asset
    asset = select_asset(release, repo)
    if asset:
        download_url = asset['browser_download_url']
        file_name = asset['name']

        print(f"Downloading {file_name}...")

        download_response = requests.get(download_url, stream=True)
        if download_response.status_code == 200:
            with open(file_name, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    if chunk: 
                        f.write(chunk)
            print(f"Downloaded {file_name} successfully.")

            if file_name.endswith(".zip"):
                print(f"Unzipping {file_name}...")
                extract_dir = f"{file_name}_extracted"
                with zipfile.ZipFile(file_name, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"Extracted files to '{extract_dir}' directory.")
                move_to_path(extract_dir)
            else:
                move_to_path(file_name)
        else:
            print(f"Failed to download {file_name}. HTTP Status Code: {download_response.status_code}")
            sys.exit(1)


# Function to move executable to PATH
def move_to_path(file_or_dir):
    destination_dir = "/usr/local/bin"  # Change this if needed for Windows or other OS
    if os.path.isfile(file_or_dir):
        print(f"{Fore.CYAN}[ ಠ‿ಠ ] Moving {file_or_dir} to {destination_dir}...{Style.RESET_ALL}")
        shutil.move(file_or_dir, os.path.join(destination_dir, os.path.basename(file_or_dir)))
    elif os.path.isdir(file_or_dir):
        for root, dirs, files in os.walk(file_or_dir):
            for file in files:
                if os.access(os.path.join(root, file), os.X_OK):
                    print(f"{Fore.CYAN}[ ಠ‿ಠ ] Moving {file} to {destination_dir}...{Style.RESET_ALL}")
                    shutil.move(os.path.join(root, file), os.path.join(destination_dir, file))
    else:
        print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] {file_or_dir} is not a file or directory.{Style.RESET_ALL}")
        sys.exit(1)

# Function to test the installed software with an optional executable name
def test_software(repo_name, executable_name=None):
    executable = executable_name if executable_name else repo_name
    print(f"{Fore.CYAN}[ ಠ‿ಠ ] Testing {executable}...{Style.RESET_ALL}")

    # Check if the executable is a Python script or a binary
    if os.path.exists(f"{executable}.py"):
        print(f"{Fore.CYAN}[ ಠ‿ಠ ] Detected Python script: {executable}.py{Style.RESET_ALL}")
        result = subprocess.run(["python3", f"{executable}.py", "--version"], capture_output=True, text=True)
    elif shutil.which(executable):
        print(f"{Fore.CYAN}[ ಠ‿ಠ ] Detected executable: {executable}{Style.RESET_ALL}")
        result = subprocess.run([executable, "--version"], capture_output=True, text=True)
    else:
        print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] Could not find an executable or build instructions for {executable}.{Style.RESET_ALL}")
        sys.exit(1)
    
    if result.returncode == 0:
        print(f"{Fore.GREEN}[ ಠ‿ಠ ] {executable} installed and tested successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[  ୧༼ಠ益ಠ༽୨  ] Error testing {executable}.{Style.RESET_ALL}")
        print(result.stderr)
        sys.exit(1)

# Main function to parse arguments and execute the workflow
def main():
    parser = argparse.ArgumentParser(description="GitHub Repo Downloader and Installer")
    parser.add_argument('-s', '--software', type=str, help="Specify the software name")
    parser.add_argument('-a', '--author', type=str, help="Specify the author name")
    parser.add_argument('--logs', type=str, help="Path to save logs", default=None)
    parser.add_argument('--exec', type=str, help="Specify the executable name if different from repo name", default=None)
    
    args = parser.parse_args()

    if not args.software and not args.author:
        print_help()
        sys.exit(1)
    
    if args.software:
        repos = fetch_repos_by_search(args.software)
        selected_repo = select_repo(repos)
    elif args.author:
        repos = fetch_repos_by_search(args.author, search_by_author=True)
        selected_repo = select_repo(repos)
    release = fetch_release(selected_repo)
    download_and_install(release, selected_repo)  # Pass the repository object here
    test_software(selected_repo['name'], args.exec)

if __name__ == "__main__":
    main()
