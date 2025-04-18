# Pitless Bucket

Pitless Bucket is a cloud storage aggregator that allows you to manage all your cloud storage accounts in one convenient place. By integrating services such as Google Drive and Dropbox into a single, seamless interface, Pitless Bucket simplifies file management and access. Whether you're on the web, using our Android app, or interacting via the Pitless Bucket Telegram bot, you have a unified platform for all your storage needs.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
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

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Fuwad13/Pitless-Bucket.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Pitless-Bucket
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   ```
5. Set up the database and environment variables.
6. Run the backend and frontend servers.

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
3. Access the web interface at `http://localhost:3000`.
4. Use the Android app or Telegram bot for mobile and chat-based interactions.

---

## Frameworks, Technologies, and Languages

| Framework/Technology | Icon                                                                 | Language/Tool | Icon                                                                 |
|-----------------------|----------------------------------------------------------------------|---------------|----------------------------------------------------------------------|
| FastAPI              | ![FastAPI](reports/assets/FastAPI.svg)                              | Python        | ![Python](reports/assets/Python.svg)                                |
| PostgreSQL           | ![PostgreSQL](reports/assets/PostgresSQL.svg)                       | SQLModel      | <img src="reports/assets/SQLModel.svg" alt="SQLModel" width="60px"> |
| Next.js              | ![Next.js](reports/assets/Next.js.svg)                              | TypeScript    | ![TypeScript](reports/assets/TypeScript.svg)                        |
| TailwindCSS          | ![TailwindCSS](reports/assets/Tailwind%20CSS.svg)                   | Node.js       | ![Node.js](reports/assets/Node.js.svg)                              |
| Android Studio       | ![Android Studio](reports/assets/Android%20Studio.svg)             | Kotlin        | ![Kotlin](reports/assets/Kotlin.svg)                                |
| Jetpack Compose      | <img src="reports/assets/jetpack compose icon_RGB.png" alt="jetpack" width="50px"> |               |                                                                      |

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
