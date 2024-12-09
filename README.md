# This repo can be used as base template for any Airflow project. It contains the following:

# 1. Dockerfile: To build the Airflow image
# 2. docker-compose.yml: To run the Airflow container
# 3. dags/: Directory to store the DAGs
# 4. plugins/: Directory to store the custom plugins
# 5. requirements.txt: To install the required Python packages
# 6. .gitignore: To ignore the files and directories
# 7. README.md: To provide the information about the project


## Step 1: Clone the repository
```bash
git clone <repo-url>
```

## Step 2: docker-compose up
```bash
docker-compose up
```

## Step 3: Open the browser
Open the browser and go to `http://localhost:2423/` to access the Airflow UI.
username: legacy
password: legacy

## Step 4: DAGs
Add the DAGs in the `dags/` directory.

