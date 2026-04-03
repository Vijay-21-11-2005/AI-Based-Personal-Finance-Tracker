# AI-Based Personal Finance Tracker

A modern personal finance tracker with AI-powered features, built using Flask, MySQL, and a Burgundy/Night theme.

## Features
- **Expense Tracking**: Add, edit, and delete expenses.
- **AI Categorization**: Automatically categorizes expenses based on descriptions (e.g., "pizza" -> Food).
- **Spending Prediction**: Uses Linear Regression to forecast next month's spending.
- **Budget Management**: Set monthly limits and receive overspending alerts.
- **Google Authentication**: Functional Sign-In with Google integration.
- **Responsive Dashboard**: Beautiful visualizations using Chart.js.

## Tech Stack
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Chart.js)
- **Backend**: Python (Flask)
- **Database**: MySQL (XAMPP compatible)
- **AI/ML**: Scikit-learn, Pandas

## Setup Instructions

### 1. Prerequisites
- Python 3.12+
- XAMPP (for MySQL)

### 2. Database Setup
1. Start MySQL in XAMPP.
2. Run the setup script:
   ```bash
   python db_setup.py
   ```

### 3. Environment Variables
Create a `.env` file in the root directory (refer to `.env.example`):
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
SECRET_KEY=your_random_secret_key
```

### 4. Google Auth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Configure OAuth consent screen.
4. Create OAuth 2.0 Client IDs.
5. Add Authorized Redirect URI: `http://127.0.0.1:5000/login/google/authorize`.
6. Copy the Client ID and Secret to your `.env` file.

### 5. Running the App
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python app.py
   ```
3. Visit `http://127.0.0.1:5000`.

## License
MIT
