import os
import requests
import webbrowser
import subprocess
import time
from datetime import datetime
from colorama import Fore, init

# Initialize Colorama
init(autoreset=True)

# Function to display the menu with color gradient
def display_menu():
    os.system('clear')  # Clear the terminal
    print(Fore.GREEN + r"""
      _              \             .    .
   ___/   __.  .___  |   ,   ___.  |    |     ___
  /   | .'   \ /   \ |  /  .'   `  |    |   .'   `
 ,'   | |    | |   ' |-<   |    |  |    |   |----'
 `___,'  `._.' /     /  \_  `---| /\__ /\__ `.___,
      `                     \___/
    """)

    print(Fore.BLUE + "=== Enhanced Google Dorks Search Menu ===")
    options = [
        "1. Search for sensitive documents",
        "2. Search for configuration files",
        "3. Search for backup files",
        "4. Search for exposed API keys",
        "5. Search for SQL databases",
        "6. Search for publicly accessible files",
        "7. Search for login pages",
        "8. Search for sensitive information",
        "9. Search for exposed directories",
        "10. Search for webcam feeds",
        "11. Search for sensitive PHP files",
        "12. Search for .env files",
        "13. Search for user directories",
        "14. Search for email addresses",
        "15. Search for vulnerabilities in WordPress",
        "16. Search for unsecured cloud storage",
        "17. Search for FTP login pages",
        "18. Search for files containing specific keywords",
        Fore.GREEN + "19. Search for files with a specific extension (e.g., .pdf)",
        Fore.GREEN + "20. Search for sensitive directories (e.g., /admin, /backup)",
        Fore.GREEN + "21. Search for publicly accessible MongoDB instances"
    ]
    for i, option in enumerate(options):
        # Print each option with a gradient effect
        color = Fore.LIGHTCYAN_EX if i % 2 == 0 else Fore.LIGHTGREEN_EX
        print(color + option)

def build_dork(base_term, keywords, filetypes, search_type):
    # Combine keywords and filetypes into the Google dork syntax
    keyword_part = " OR ".join([f'"{kw.strip()}"' for kw in keywords])
    filetype_part = ' OR '.join([f'filetype:{ft.strip()}' for ft in filetypes])

    # Define various dork types
    dork_types = {
        1: f"{base_term} ({keyword_part})",
        2: f"{base_term} ({keyword_part}) {filetype_part}",
        3: f"{base_term} ({keyword_part}) (filetype:bak OR filetype:config)",
        4: f"{base_term} ({keyword_part}) 'API key'",
        5: f"{base_term} ({keyword_part}) (filetype:sql OR filetype:db)",
        6: f"{base_term} ({keyword_part})",
        7: f"{base_term} 'login' inurl:login",
        8: f"{base_term} ({keyword_part}) 'password' OR 'secret' OR 'confidential'",
        9: f"{base_term} intitle:index.of ({keyword_part})",
        10: f"{base_term} inurl:webcam ({keyword_part})",
        11: f"{base_term} filetype:php ({keyword_part})",
        12: f"{base_term} filetype:env ({keyword_part})",
        13: f"{base_term} 'user' inurl:directory",
        14: f"{base_term} intext:@ ({keyword_part})",
        15: f"{base_term} 'wp-content' 'vulnerability' ({keyword_part})",
        16: f"{base_term} 'bucket' 'cloud' ({keyword_part})",
        17: f"{base_term} 'ftp' 'login' ({keyword_part})",
        18: f"{base_term} intext:({keyword_part})",
        19: f"{base_term} filetype:pdf ({keyword_part})",  # Powerful Dork
        20: f"{base_term} inurl:(/admin OR /backup) ({keyword_part})",  # Powerful Dork
        21: f"{base_term} inurl:mongodb ({keyword_part})"  # Powerful Dork
    }
    return dork_types.get(search_type)

def search_google_dork(dork):
    url = f"https://www.google.com/search?q={dork}"
    print(Fore.YELLOW + f"\nSearching for: {dork}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(Fore.RED + "Error during the search. Please try again later.")
            return None
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")
        return None

def generate_html_report(results, overwrite=True):
    filename = "results.html" if overwrite else f"results_{datetime.now().strftime('%Y-%m-%d')}.html"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Dork Results</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            h1 {{
                color: #333;
            }}
            pre {{
                background-color: #fff;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
                overflow-x: auto;
            }}
            .footer {{
                font-size: 0.8em;
                color: #666;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Google Dork Results</h1>
        <p>Results generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <pre>{results}</pre>
        <div class="footer">Generated by Enhanced Google Dorks Tool</div>
    </body>
    </html>
    """
    with open(filename, "w") as f:
        f.write(html_content)
    print(Fore.GREEN + f"Results saved to {filename}")
    webbrowser.open(filename)  # Automatically open the HTML report

def display_info():
    info_text = (
        "Enhanced Google Dorking Tool\n"
        "-----------------------------\n"
        "This program allows users to perform powerful Google searches using dorking techniques.\n"
        "Features:\n"
        "- Search for sensitive documents, exposed files, and specific configurations.\n"
        "- Supports a variety of file types and keywords.\n"
        "- Generates HTML reports of search results.\n"
        "- User-friendly interface with colored output.\n\n"
        "Usage:\n"
        "1. Choose a search type from the menu.\n"
        "2. Input the base term, keywords, and file types as needed.\n"
        "3. View the generated results in the terminal and saved to an HTML file.\n"
        "4. For more information, consult the documentation.\n"
    )

    # Command to open Konsole and run the echo command with typing effect
    command = f"bash -c \"echo '{info_text}' | pv -qL 10; read -p 'Press enter to continue...'\""
    subprocess.Popen(['konsole', '-e', command])

def main():
    while True:
        display_menu()
        choice = input(Fore.LIGHTWHITE_EX + "\nSelect an option: ")

        if choice.isdigit() and 1 <= int(choice) <= 21:
            base_term = input(Fore.LIGHTWHITE_EX + "Enter the base term for your search: ")
            keywords = input(Fore.LIGHTWHITE_EX + "Enter keywords (separated by commas): ").split(',')
            filetypes = input(Fore.LIGHTWHITE_EX + "Enter file types (separated by commas): ").split(',')

            # Build the dork based on the user's choice
            dork = build_dork(base_term, keywords, filetypes, int(choice))
            if dork:
                results = search_google_dork(dork)

                if results:
                    print(Fore.CYAN + "\n--- Preview of Results ---")
                    print(results[:500])  # Display the first 500 characters of the results
                    generate_html_report(results, overwrite=True)  # Overwrite every time

        elif choice == '19':
            display_info()

        elif choice == '20':
            print(Fore.RED + "Goodbye!")
            break

        else:
            print(Fore.RED + "Invalid choice, please try again.")

if __name__ == "__main__":
    main()
