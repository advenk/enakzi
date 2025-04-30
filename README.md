# expl0rer

A web application for crawling, storing, and displaying images 

## Components

- **API**: FastAPI backend for serving image data
- **Crawler**: web crawler with NIMA scoring for aesthetics 
- **Web**: React frontend for displaying images
- **Database**: PostgreSQL database for storing image metadata

## Local Setup (Without Docker)

### Prerequisites

- Python 3.6+
- PostgreSQL
- Node.js and npm

### Setup Instructions
Clone the repository and run the setup script:
   ```
   python setup_local.py
   ```

   This script will:
   - Check if PostgreSQL is installed and running
   - Create the database if it doesn't exist
   - Set up virtual environments for the API and crawler
   - Install dependencies for all components

### Running the Components

#### 1. Start the API

```bash
cd api
../run_api.py
```

The API will be available at http://localhost:8000

#### 2. Run the Crawler

```bash
cd crawler
../run_crawler.py
```

#### 3. Start the Web Application

```bash
cd web
npm start
```

The app will be available at http://localhost:3000

## Configuration

All configuration is centralized in the `config/config.py` file. You can modify this file to change:

- Database connection parameters
- API host and port
- Web application settings
- Crawler settings

## Troubleshooting

### Database Connection Issues

- Make sure PostgreSQL is running: `brew services start postgresql` (macOS) or `sudo service postgresql start` (Linux)
- Check that the database user has the correct permissions
- Verify the database connection parameters in `config/config.py`

### API Issues

- Check that the API is running and accessible at http://localhost:8000
- Look for error messages in the API console output

### Web Application Issues

- Make sure the API is running before starting the web application
- Check that the API URL is correctly set in the `.env` file