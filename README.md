# Pitless Bucket

Pitless Bucket is a cloud storage aggregator that allows you to manage all your cloud storage accounts in one convenient place. By integrating services such as Google Drive and Dropbox into a single, seamless interface, Pitless Bucket simplifies file management and access. Whether you're on the web, using our Android app, or interacting via the Pitless Bucket Telegram bot, you have a unified platform for all your storage needs.

---

## Contributors
- Fuwad Hasan 2211247042 fuwad.hasan@northsouth.edu
- Abdullah Al Raiyan 2212712042 abdullah.raiyan@northsouth.edu

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
   - [Telegram Bot Setup](#telegram-bot-setup)
3. [Usage](#usage)
4. [Frameworks, Technologies, and Languages](#frameworks-technologies-and-languages)
5. [Contributing](#contributing)
6. [License](#license)

---

## Features

- Unified platform for managing multiple cloud storage accounts.
- Integration with Google Drive, Dropbox, and more.
- Web, Android, and Telegram bot interfaces.
- Secure and seamless file management.
- User-friendly design and intuitive navigation.

---

## Installation

### Prerequisites

- Python 3.13+
- Node.js 22+
- Kotlin 2.1.1+

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Fuwad13/Pitless-Bucket.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Pitless-Bucket
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Copy the `.env.example` file to `.env` and fill in the required environment variables:
   ```bash
   cp .env.example .env
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```

### Telegram Bot Setup

1. Navigate to the `telegram-bot` directory:
   ```bash
   cd telegram-bot
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install bot dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy the `.env.example` file to `.env` and fill in the required environment variables:
   ```bash
   cp .env.example .env
   ```

---

## Usage [Development]

1. Start the backend server:
   ```bash
   # in the root directory run this command
   fastapi dev backend
   ```
2. Start the frontend server:
   ```bash
    # in the frontend directory run this command
   npm run dev
   ```
3. Start the Telegram bot:
   ```bash
   python telegram-bot/bot.py
   ```
4. Access the web interface at `http://localhost:3000`.
5. Use the Android app or Telegram bot for mobile and chat-based interactions.

---

## Frameworks, Technologies, and Languages

| Framework/Technology | Purpose                                                                 | Language/Tool | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|---------------|-------------------------------------------------------------------------|
| FastAPI              | Backend framework for building APIs                                    | Python        | Programming language for backend development                           |
| PostgreSQL           | Database for storing user and file metadata                            | SQLModel      | ORM for interacting with the PostgreSQL database                       |
| Redis                | In-memory data structure store used for caching    |               |                                                                         |
| Next.js              | Frontend framework for building the web interface                      | TypeScript    | Programming language for frontend development                          |
| TailwindCSS          | Utility-first CSS framework for styling the frontend                   | Node.js       | Runtime for executing JavaScript/TypeScript code                       |
| Android Studio       | IDE for developing the Android application                             | Kotlin        | Programming language for Android app development                       |
| Jetpack Compose      | Toolkit for building native Android UI                                 |               |                                                                         |

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
