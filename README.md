# HSR Motors Lead Management System

## Overview

The HSR Motors Lead Management System is a web application designed to facilitate the management of sales leads at HSR Motors. This application allows users to track, update, and analyze leads efficiently. It incorporates role-based access control to ensure users can perform actions according to their assigned roles.

## Features

- **User Authentication**: Secure login for users to access the system.
- **Lead Listing**: View and manage a list of current leads.
- **Lead Management**: Add new leads with relevant details.
- **Lead Status Updates**: Update the status of existing leads.
- **Dashboard**: Visualize lead metrics for business managers.
- **Role-Based Permissions**: Distinct functionalities based on user roles (Sales Team and Business Manager).

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Setting Up the Environment

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

- Windows:

   ```bash
   .venv\Scripts\activate
   ```

- macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Ensure the following CSV files are present in the root directory:

- users.csv: Contains user credentials and roles.
- leads.csv: Stores lead information.

## Usage

1. Start the application:

```bash
streamlit run app.py
```

2. Access the application in your web browser at http://localhost:8501.

3. Log in with your credentials to access the main interface.

4. Navigate through the application using the sidebar to manage leads and view the dashboard.


### Notes

- Replace `<repository-url>` and `<repository-directory>` with your actual repository URL and directory name.
- Ensure you have Python 3.x installed.
- Ensure you update any details specific to your project, including dependencies in the `requirements.txt`, usage instructions, and any acknowledgments or additional information you wish to include.

