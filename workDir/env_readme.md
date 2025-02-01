# LLMCoder Configuration Guide (.env File)

This document explains each variable within the `.env` file for the LLMCoder application, providing instructions on how to obtain the required values and their expected format.

**General Configuration**

*   `PROJECT_NAME`:
    *   **Description**: The name of the LLMCoder project. This is used for display purposes within the application and in the API documentation.
    *   **How to Obtain**: Choose a descriptive name for your project.
    *   **Format**: A string (e.g., `"LLMCoder"`, `"MyLLMApp"`).  **No quotes required.**
    *   **Example**: `PROJECT_NAME=LLMCoder`
*   `API_V1_STR`:
    *   **Description**: The base URL path for API version 1. This defines the prefix for all API endpoints.
    *   **How to Obtain**: Set the desired prefix for the API.
    *   **Format**: A string starting with a forward slash (e.g., `"/api"` , `"/v1"`). **No quotes required.**
    *   **Example**: `API_V1_STR=/api`
*   `SECRET_KEY`:
    *   **Description**: The secret key used for signing JSON Web Tokens (JWTs) for user authentication. **This should be a strong, randomly generated string and kept secret.**
    *   **How to Obtain**: Generate a secure random string using a password generator or similar tool (e.g., `openssl rand -hex 32` on Linux/macOS).
    *   **Format**: A long, random string. **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`
*   `JWT_ALGORITHM`:
    *   **Description**: The algorithm used to sign JWTs. `HS256` (HMAC with SHA-256) is a common and secure choice.
    *   **How to Obtain**: Use a standard JWT signing algorithm.
    *   **Format**:  A string representing the JWT algorithm (e.g., `"HS256"`, `"RS256"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `JWT_ALGORITHM=HS256`
*   `ACCESS_TOKEN_EXPIRE_MINUTES`:
    *   **Description**: The expiration time (in minutes) for access tokens.
    *   **How to Obtain**: Choose an appropriate expiration time for access tokens.
    *   **Format**: An integer representing minutes (e.g., `"15"`, `"60"`). **No quotes required.**
    *   **Example**: `ACCESS_TOKEN_EXPIRE_MINUTES=15`
*   `DATABASE_URL`:
    *   **Description**: The URL or connection string for the database. SQLite is used by default, which uses a local file.  You may replace this with a connection string to Postgres, MySQL, or other databases.
    *   **How to Obtain**: If using a database other than SQLite, provide the database connection string (e.g., for PostgreSQL: `postgresql://user:password@host:port/database`). For SQLite, it is a file path.
    *   **Format**: A valid database URL string (e.g., `"sqlite:///./llmcoder.db"`). **Quotes are required.**
    *   **Example**: `DATABASE_URL="sqlite:///./llmcoder.db"` or `DATABASE_URL="postgresql://user:password@host:port/database"`
*  `HOST_WORKSPACE`:
    * **Description**: Path to the workspace where LLMCoder is allowed to store and access files. **This should be a secure, limited path.**
    * **How to Obtain**: Set an absolute path on the system.
    * **Format**: A string representing a directory path (e.g., `"/llmcoder_workspace/"`, `"/home/user/llmcoder_data/"`). **Quotes are required.**
    * **Example**: `HOST_WORKSPACE="/llmcoder_workspace/"`

**API Credentials**

*   `OPENAI_API_KEY`:
    *   **Description**: Your OpenAI API key for accessing OpenAI models.
    *   **How to Obtain**: Create an account at [https://platform.openai.com](https://platform.openai.com) and obtain an API key from your API keys page.
    *   **Format**:  A string representing the OpenAI API key (e.g., `"sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `GOOGLE_API_KEY`:
    *   **Description**: Your Google API key for accessing Google services (e.g., Geocoding API).
    *   **How to Obtain**: Create a project at [https://console.cloud.google.com](https://console.cloud.google.com) and enable the relevant APIs.  Generate an API key from the "Credentials" page.
    *   **Format**: A string representing the Google API key (e.g., `"AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*    `GOOGLE_CLIENT_ID`:
    *   **Description**: Your Google Client ID for OAuth 2.0 authentication.
    *   **How to Obtain**: Create an OAuth 2.0 client ID in the Google Cloud Console under "Credentials."
    *   **Format**: A string representing the Google Client ID. **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `GOOGLE_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com`
*  `GOOGLE_CLIENT_SECRET`:
    *   **Description**: Your Google Client Secret for OAuth 2.0 authentication.
    *   **How to Obtain**: Create an OAuth 2.0 client ID in the Google Cloud Console under "Credentials." You will need to download a `client_secret.json` file, and extract the `client_secret` from this file, this is a string.
    *  **Format**: A string representing the Google Client Secret. **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `GOOGLE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `GOOGLE_REDIRECT_URI`:
    *   **Description**: The redirect URI for Google OAuth 2.0 authentication. This should match the redirect URI configured in the Google Cloud Console.
    *   **How to Obtain**: Set to the URL where Google should redirect the user after authentication.
    *   **Format**: A URL string (e.g., `"http://localhost:8000/api/auth/google/callback"`). **Quotes are required.**
    *  **Example**: `GOOGLE_REDIRECT_URI="http://localhost:8000/api/auth/google/callback"`
*  `MICROSOFT_CLIENT_ID`:
    *   **Description**: Your Microsoft Client ID for OAuth 2.0 authentication.
    *   **How to Obtain**: Register an application in the Azure portal and create an OAuth 2.0 client ID.
    *   **Format**: A string representing the Microsoft Client ID. **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
*   `MICROSOFT_CLIENT_SECRET`:
    *  **Description**: Your Microsoft Client Secret for OAuth 2.0 authentication.
    *   **How to Obtain**: Register an application in the Azure portal and create an OAuth 2.0 client secret.
    *  **Format**: A string representing the Microsoft Client Secret. **No quotes required, but can be wrapped for clarity if desired.**
    *  **Example**: `MICROSOFT_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `MICROSOFT_REDIRECT_URI`:
    *  **Description**: The redirect URI for Microsoft OAuth 2.0 authentication. This should match the redirect URI configured in the Azure portal.
    *   **How to Obtain**: Set to the URL where Microsoft should redirect the user after authentication.
    *  **Format**: A URL string (e.g., `"http://localhost:8000/api/auth/microsoft/callback"`). **Quotes are required.**
    *  **Example**: `MICROSOFT_REDIRECT_URI="http://localhost:8000/api/auth/microsoft/callback"`
*   `SLACK_CLIENT_ID`:
    *   **Description**: Your Slack Client ID for OAuth 2.0 authentication.
    *   **How to Obtain**: Create a Slack app in your Slack workspace and obtain the Client ID.
    *   **Format**: A string representing the Slack Client ID (e.g., `"xxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `SLACK_CLIENT_ID=xxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxx`
*   `SLACK_CLIENT_SECRET`:
    *   **Description**: Your Slack Client Secret for OAuth 2.0 authentication.
    *   **How to Obtain**: Create a Slack app in your Slack workspace and obtain the Client Secret.
    *   **Format**: A string representing the Slack Client Secret (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `SLACK_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*  `SLACK_REDIRECT_URI`:
    *   **Description**: The redirect URI for Slack OAuth 2.0 authentication. This should match the redirect URI configured in the Slack app settings.
    *   **How to Obtain**: Set to the URL where Slack should redirect the user after authentication.
    *  **Format**: A URL string (e.g., `"http://localhost:8000/api/auth/slack/callback"`). **Quotes are required.**
    *   **Example**: `SLACK_REDIRECT_URI="http://localhost:8000/api/auth/slack/callback"`
*   `SLACK_BOT_TOKEN`:
    *   **Description**: Your Slack Bot Token for API access.
    *   **How to Obtain**: In your Slack App settings, install the app to your workspace and get the bot token.
    *   **Format**: A string representing the Slack bot token (e.g., `"xoxb-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxx`
*  `SLACK_APP_TOKEN`:
     *   **Description**: Your Slack App Token for Socket Mode.
     *   **How to Obtain**: In your Slack App settings, enable Socket Mode and get the app token. Note - This is not used if you're using the Event API for real-time features.
     *   **Format**: A string representing the Slack App Token (e.g., `"xapp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
     *   **Example**: `SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `JIRA_SERVER_URL`:
    *   **Description**: The base URL of your JIRA server instance.
    *   **How to Obtain**: Copy the base URL from your JIRA instance (e.g., `https://your-company.atlassian.net`).
    *   **Format**: A URL string (e.g., `"https://your-company.atlassian.net"`).  **Quotes are required.**
    *   **Example**: `JIRA_SERVER_URL="https://your-company.atlassian.net"`
*   `JIRA_API_TOKEN`:
    *   **Description**: An API token for JIRA access.
    *   **How to Obtain**: Create an API token in your Atlassian account settings.
    *   **Format**: A long, random string representing the API token. **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `JIRA_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `SKYSCANNER_API_KEY`:
    *   **Description**: Your Skyscanner API key for fetching flight data.
    *   **How to Obtain**: Obtain a Skyscanner API key from the RapidAPI platform.
    *   **Format**: A string representing the Skyscanner API key (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `SKYSCANNER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `PLAID_CLIENT_ID`:
    *   **Description**: Your Plaid API Client ID.
    *   **How to Obtain**: Obtain your Plaid API Client ID from the Plaid developer dashboard.
    *   **Format**: A string representing the Plaid Client ID (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `PLAID_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `PLAID_SECRET`:
    *   **Description**: Your Plaid API Secret.
    *   **How to Obtain**: Obtain your Plaid API Secret from the Plaid developer dashboard.
    *   **Format**: A string representing the Plaid Secret (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `PLAID_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*  `FITBIT_CLIENT_ID`:
    *   **Description**: Your Fitbit API Client ID for accessing Fitbit data.
    *   **How to Obtain**: Create a Fitbit app on the Fitbit Developer portal and obtain the client ID.
    *   **Format**: A string representing the Fitbit Client ID (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `FITBIT_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `FITBIT_CLIENT_SECRET`:
    *   **Description**: Your Fitbit API Client Secret for accessing Fitbit data.
    *   **How to Obtain**: Create a Fitbit app on the Fitbit Developer portal and obtain the client secret.
    *   **Format**: A string representing the Fitbit Client Secret (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `FITBIT_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `TWITTER_BEARER_TOKEN`:
     *   **Description**: Your Twitter (X) API Bearer Token for API access.
     *   **How to Obtain**: Create a Twitter (X) app in your Twitter Developer portal and obtain a bearer token.
     *   **Format**: A string representing the Twitter Bearer token (e.g., `"AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
     *   **Example**: `TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*  `TWITTER_CONSUMER_KEY`:
    *  **Description**: Your Twitter API Consumer Key for OAuth 1.0a authentication.
    *  **How to Obtain**: Create a Twitter app in your Twitter Developer portal and obtain the Consumer Key.
    *   **Format**: A string representing the Twitter Consumer Key (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `TWITTER_CONSUMER_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*  `TWITTER_CONSUMER_SECRET`:
    *   **Description**: Your Twitter API Consumer Secret for OAuth 1.0a authentication.
    *  **How to Obtain**: Create a Twitter app in your Twitter Developer portal and obtain the Consumer Secret.
    *   **Format**: A string representing the Twitter Consumer Secret (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `TWITTER_CONSUMER_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `TWITTER_ACCESS_TOKEN`:
    *   **Description**: Your Twitter API Access Token for OAuth 1.0a authentication.
    *   **How to Obtain**: Create a Twitter app in your Twitter Developer portal and obtain the Access Token.
    *   **Format**: A string representing the Twitter Access Token (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `TWITTER_ACCESS_TOKEN_SECRET`:
    *   **Description**: Your Twitter API Access Token Secret for OAuth 1.0a authentication.
    *   **How to Obtain**: Create a Twitter app in your Twitter Developer portal and obtain the Access Token Secret.
    *   **Format**: A string representing the Twitter Access Token Secret (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
* `CONFLUENCE_URL`:
    *   **Description**: The base URL of your Confluence instance.
    *   **How to Obtain**: Copy the base URL from your Confluence instance (e.g., `"https://your-company.atlassian.net/wiki"`).
    *   **Format**: A URL string (e.g., `"https://your-company.atlassian.net/wiki"`).  **Quotes are required.**
    *   **Example**: `CONFLUENCE_URL="https://your-company.atlassian.net/wiki"`
*   `CONFLUENCE_API_TOKEN`:
    *   **Description**: An API token for Confluence access.
    *   **How to Obtain**: Create an API token in your Atlassian account settings.
    *   **Format**: A long, random string representing the API token. **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `CONFLUENCE_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*   `NEWS_API_KEY`:
    *   **Description**: Your News API key for fetching news articles.
    *   **How to Obtain**: Obtain a News API key from a provider such as NewsAPI.org.
    *   **Format**: A string representing the News API key (e.g., `"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"`). **No quotes required, but can be wrapped for clarity if desired.**
    *   **Example**: `NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
*    `GOOGLE_SERVICE_ACCOUNT`:
    *   **Description**: The JSON data representing your Google Service Account for Google API access.
    *   **How to Obtain**: Create a Service Account in the Google Cloud Console and generate a JSON key file. Copy the entire JSON file string from this service account file here.
    *   **Format**: JSON string representation of your Google Service Account credentials. **This must be a single string including the start and end curly braces and no newlines or escaped characters!**
    *   **Example**: `GOOGLE_SERVICE_ACCOUNT='{"type":"service_account","project_id":"your-project-id","private_key_id":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx","private_key":"-----BEGIN PRIVATE KEY-----\\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\\n-----END PRIVATE KEY-----\\n","client_email":"your-service-account@your-project-id.iam.gserviceaccount.com","client_id":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"}'`

**Important Notes:**

*   **Security**: Treat all API keys and secrets as sensitive information. Do not commit them directly to your codebase or share them publicly.
*   **Environment Variables:** The `.env` file is used to load environment variables, which are used by the application. This is a common approach to managing sensitive information.
*   **Quotes:** Generally, you do not need to wrap values in quotes, but I have noted where it is required (such as with a JSON blob) or recommended for clarity, especially with strings that contain spaces, or are URLS.
*  **Placeholders**: The values provided above are mostly placeholders and should be replaced with your own actual API keys, tokens, and URLs.

## Instructions for Starting, Using, and Testing LLMCoder

These steps provide a guide for starting, using, and testing the LLMCoder application:

**1. Setup:**

    *   **Install Python**: Ensure you have Python 3.10 or higher installed.
    *   **Create and Activate Python Virtual Environment**:
        ```bash
        cd backend
        python3 -m venv venv
        source venv/bin/activate   # On Linux/macOS
        # venv\Scripts\activate  # On Windows
        ```
    *   **Install Python Dependencies**:
        ```bash
        pip install -r requirements.txt
        ```
    *   **Install npm Dependencies**:
        ```bash
        cd ../frontend
        npm install
        ```
    * **Create database directory:**
        ```bash
        mkdir ../data
        ```
    * **return to root directory:**
        ```bash
        cd ..
        ```
    *   **Configure Environment Variables**: Create a `.env` file in the `backend` directory and fill in the appropriate values for all placeholders based on the above documentation.
    *   **Frontend Configuration:** In the `frontend` folder, ensure that `vite.config.ts` contains the correct target `http://localhost:8000` to connect to the API.

**2. Start the Application (Backend Server):**

    *   **Activate the Virtual Environment (if not already active)**:
        ```bash
        cd backend
        source venv/bin/activate  # On Linux/macOS
        # venv\Scripts\activate  # On Windows
        ```
    *   **Run the FastAPI server using uvicorn**
        ```bash
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ```

    *   **Expected Observation:**
        *   The terminal should display the uvicorn startup message, indicating that the server is running on `http://0.0.0.0:8000` (or the port you specified).
        *   The server is now listening for incoming requests on the specified port.

**3. Start the Application (Frontend Client):**
    *    **Navigate to the frontend folder:**
        ```bash
        cd frontend
        ```
    *  **Start the Vite dev server**:
        ```bash
        npm run dev
        ```
    *  **Expected Observation:**
       * The terminal should display the Vite dev server startup message, including the url where the app is running (e.g. `http://localhost:5173/`)

**4. Access the Web GUI:**
    *  Open your web browser and navigate to the frontend URL.

    *   **Expected Observation:**
        *   The LLMCoder web GUI should be displayed. You should see the default "Home" page, a login button in the navbar and a link to the about page.
        *   The web GUI is now connected to the backend server using REST APIs for data fetching and actions.

**5. Basic Testing:**

   *   **User Registration**:
        *   Navigate to the `/login` page and create a new user account with the registration form, this will register a new user into the system.
        *   After registering, you will be redirected to the login page to login.
     *   **User Login**:
         *   Navigate to the `/login` page and use the new user credentials to log into the system. You will be redirected to the main page.
         *  You will also see a dashboard navigation link in the navigation bar.
    *  **Access the Dashboard**:
        *   Click on the `Dashboard` link. You will be redirected to the dashboard page.
     *  **Access a Feature**:
         *   Click on a feature in the navigation links on the dashboard page (Notes, To-Do, Email, etc.). You will see the relevant UI for those components.
    * **Test API calls**:
        * Click the buttons in the UI. If you are running the backend server you will see the relevant output in your terminal (backend side).
    *  **Expected Observation:**
         *   You should be able to create new notes, todos, etc, and have them saved in the database.
         *  You should be able to login.
         *  You should see the various components functioning and interacting with the server, as outlined in the project plan.