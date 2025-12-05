# Simple Social - A FastAPI and Streamlit Application

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/Tanmay692004/techwithtim-tutorial.git)

This repository contains the source code for a simple social media application built following a tutorial from Tech With Tim. The application features a FastAPI backend for the API and a Streamlit frontend for the user interface. It allows users to register, log in, upload media (images and videos), and view a shared feed.

## Features

-   **User Authentication**: Secure user registration, JWT-based login, and session management using `fastapi-users`.
-   **Media Uploads**: Users can upload images and videos with captions.
-   **Cloud Media Management**: Integrates with [ImageKit.io](https://imagekit.io/) for media storage, delivery, and real-time transformations.
-   **Dynamic Social Feed**: A central feed that displays all user posts in chronological order.
-   **Post Management**: Users can delete their own posts.
-   **Asynchronous Backend**: Built with FastAPI and SQLAlchemy's async capabilities for high performance.
-   **Interactive Frontend**: A simple and responsive user interface created with Streamlit.

## Technology Stack

-   **Backend**: FastAPI, Uvicorn, SQLAlchemy, aiosqlite
-   **Frontend**: Streamlit
-   **Authentication**: FastAPI-Users
-   **Database**: SQLite
-   **Media Storage**: ImageKit.io
-   **Dependencies**: Handled with `uv` and `pyproject.toml`

## Project Structure

```
├── app/
│   ├── app.py          # Main FastAPI application, defines API routes
│   ├── db.py           # SQLAlchemy database models (User, Post) and session setup
│   ├── images.py       # ImageKit.io SDK configuration
│   ├── schemas.py      # Pydantic models for data validation and serialization
│   └── users.py        # FastAPI-Users configuration for authentication and user management
├── frontend.py         # Streamlit frontend application code
├── main.py             # Entry point to run the FastAPI backend with Uvicorn
├── pyproject.toml      # Project metadata and dependencies
├── test.db             # SQLite database file
├── .env.example        # Example environment variables
└── README.md           # This file
```

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Tanmay692004/techwithtim-tutorial.git
cd techwithtim-tutorial
```

### 2. Install Dependencies

This project uses `uv` for package management. Ensure you have it installed.

```bash
# Install uv if you haven't already
pip install uv

# Create a virtual environment and install dependencies
uv venv
uv sync
```

### 3. Configure Environment Variables

You will need API keys from [ImageKit.io](https://imagekit.io/) for media uploads to work.

Create a `.env` file in the root of the project and add your keys:

```ini
imagekit_private_key="YOUR_IMAGEKIT_PRIVATE_KEY"
imagekit_public_key="YOUR_IMAGEKIT_PUBLIC_KEY"
imagekit_url_endpoint="YOUR_IMAGEKIT_URL_ENDPOINT"
```

## Running the Application

The application consists of two separate processes: the backend server and the frontend interface. You need to run both in separate terminal windows.

### 1. Run the Backend (FastAPI)

From the project root, run:

```bash
python main.py
```

The backend server will start on `http://localhost:8000`.

### 2. Run the Frontend (Streamlit)

In a new terminal window, run:

```bash
streamlit run frontend.py
```

The frontend application will open in your browser, typically at `http://localhost:8501`. You can now register a new user, log in, and start sharing media.