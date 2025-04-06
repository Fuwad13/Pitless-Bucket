# Pitlessbucket - Cloud Storage Aggregator

[![Next.js](https://img.shields.io/badge/Next.js-15.1.6-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.0.0-blue?style=flat-square&logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![Firebase](https://img.shields.io/badge/Firebase-11.3.0-orange?style=flat-square&logo=firebase)](https://firebase.google.com/)

**Pitlessbucket** simplifies your digital life by bringing your cloud storage accounts together. Connect multiple Google Drive and Dropbox accounts to your single Pitlessbucket account and manage your files seamlessly from one centralized platform.

## Table of Contents

- [Live Link](#live-link)
- [🎯 The Problem](#-the-problem)
- [✨ The Solution](#-the-solution)
- [🛠️ Tech Stack](#️-tech-stack)
- [Screenshots](#screenshots)
- [🚀 Getting Started](#-getting-started)
- [📜 Available Scripts](#-available-scripts)
- [📄 License](#-license)

## Live Link

**[Link to Live Demo/Website - will be added later]**

## 🎯 The Problem

Juggling multiple cloud storage accounts (like different Google Drives for personal/work or combining Drive with Dropbox) can be cumbersome. Remembering where files are stored, logging in and out of different services, and transferring files between them takes time and effort.

## ✨ The Solution

Pitlessbucket provides a unified interface to:

- **Connect Multiple Accounts:** Securely link various Google Drive and Dropbox accounts.
- **Aggregate Files:** View files and folders from all connected accounts in one place.
- **Upload Files:** Choose which connected account to upload new files to directly from Pitlessbucket.
- **Download Files:** Easily download files stored in any of your connected cloud drives.
- **Centralized Management:** Simplify browsing, accessing, and organizing your cloud-stored data.

## 🛠️ Tech Stack

This project is built using modern web technologies:

- **Framework:** [Next.js](https://nextjs.org/) (v15) - React framework for server-side rendering, static site generation, and more.
- **Language:** [TypeScript](https://www.typescriptlang.org/) - Strongly typed JavaScript for better maintainability and developer experience.
- **UI Components:**
  - [shadcn/ui](https://ui.shadcn.com/) - Beautifully designed components built using Radix UI and Tailwind CSS.
  - [Radix UI](https://www.radix-ui.com/) - Primitives for building high-quality, accessible design systems and web apps.
  - [Lucide React](https://lucide.dev/) - Simply beautiful open-source icons.
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) - A utility-first CSS framework for rapid UI development.
- **Forms:** [React Hook Form](https://react-hook-form.com/) & [Zod](https://zod.dev/) - Efficient form handling and validation.
- **Backend & Authentication:** [Firebase](https://firebase.google.com/) (Authentication, potentially Firestore/Cloud Functions - inferred from `firebase` and `firebase-admin`).
- **API Calls:** [Axios](https://axios-http.com/) - Promise-based HTTP client.
- **State Management:** React Context API (implied via Next.js/React structure).
- **Notifications:** [Sonner](https://sonner.emilkowal.ski/), [React Toastify](https://fkhadra.github.io/react-toastify/), [SweetAlert2](https://sweetalert2.github.io/) - For user feedback and alerts.
- **Linting/Formatting:** [ESLint](https://eslint.org/) - Code linting.
- **Other UI Libraries:** `recharts`, `embla-carousel-react`, `react-resizable-panels`, `vaul`, `react-day-picker`, etc.

## Screenshots

<p align="center">
  <img src="https://i.ibb.co.com/7JMvPzqY/pitless-index.png" alt="Pitlessbucket Landing Page" width="700">
  <br>
  <em>Landing Page</em>
</p>

<p align="center">
  <img src="https://i.ibb.co.com/Y4FxPGb5/pitless-login.png" alt="Pitlessbucket Login Page" width="500">
  <br>
  <em>Login Page</em>
</p>

<p align="center">
  <img src="https://i.ibb.co.com/DHwfFqZ2/pitless-signup.png" alt="Pitlessbucket Signup Page" width="500">
  <br>
  <em>Signup Page</em>
</p>

<p align="center">
  <img src="https://i.ibb.co.com/Y7JHCjFC/pitless-dashboard.png" alt="Pitlessbucket Dashboard File View" width="700">
  <br>
  <em>Main Dashboard / File View</em>
</p>

<p align="center">
  <img src="https://i.ibb.co.com/39Q9RNQp/pitless-upload-modal.png" alt="Pitlessbucket File Upload Modal" width="500">
  <br>
  <em>File Upload Modal</em>
</p>

<p align="center">
  <img src="https://i.ibb.co.com/KpQPfZxs/pitless-settings.png" alt="Pitlessbucket Settings Page" width="700">
  <br>
  <em>User Settings Page</em>
</p>

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Fuwad13/Pitless-Bucket.git
    cd Pitless-Bucket
    cd frontend
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Set up Environment Variables:**

    - Create a `.env.local` file in the `frontend` directory.
    - You will need to add Firebase configuration keys and potentially API keys/secrets for Google Drive and Dropbox OAuth. Refer to the official documentation for each service to obtain these.
    - Example `.env.local` structure ( **DO NOT COMMIT THIS FILE** ):
      ```env
      # Firebase Config (Frontend)
      NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
      NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
      NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
      NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
      NEXT_PUBLIC_FIREBASE_APP_ID=1:your-sender-id:web:your-app-id
      NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=G-xxxxxxxxxx # Optional
      ```

4.  **Run the development server:**

    ```bash
    npm run dev
    # or
    yarn dev
    ```

5.  **Open your browser:**
    Navigate to [http://localhost:3000](http://localhost:3000).

## 📜 Available Scripts

In the `frontend` project directory, you can run:

- `npm run dev` or `yarn dev`: Runs the app in development mode.
- `npm run build` or `yarn build`: Builds the app for production.
- `npm run start` or `yarn start`: Starts the production server (requires `build` first).
- `npm run lint` or `yarn lint`: Lints the codebase using Next.js's ESLint configuration.

Please ensure your code adheres to the project's linting rules (`npm run lint`).

## 📄 License

"All Rights Reserved".

---
