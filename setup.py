import subprocess
packages = ['colorama', 'json', 'requests', 'beautifulsoup4', 'mysql-connector-python']

def install_packages():
    for package in packages:
        subprocess.call(['pip', 'install', package])

if __name__ == "__main__":
    print("Installing required packages...")
    install_packages()
    print("Installation completed.")
    print("Run script.py and enjoy!")
