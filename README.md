# Sanatani Bandhan Management App 🕉️

*"Dharmo rakshati rakshitah"* — Dharma protects those who protect it. (Manu Smriti 8.15)

The **Sanatani Bandhan Management App** is a dedicated, offline-first Android application engineered to manage our community's members, Daan (donations), and Seva (social work and festivals). It is built to operate flawlessly without an internet connection, automatically syncing to the cloud once a connection is re-established.

## 🌟 Core Features
* **Multi-Lingual Interface:** Built-in support for English, Bengali (বাংলা), and Hindi (हिन्दी) to serve all volunteers.
* **Offline-First Architecture:** Powered by local SQLite for instant data entry during crowded Utsavs or Seva drives.
* **Smart Cloud Sync:** Background synchronization to Firebase Realtime Database.
* **Secure Access:** Role-based login system for administrators.
* **PDF Generation:** Automated generation of Daan reports directly to device storage.

## 🛠️ Technology Stack
* **Frontend:** Python & Kivy
* **Local Database:** SQLite3
* **Cloud Sync:** Firebase Realtime Database (REST API)
* **DevOps / CI-CD:** GitHub Actions & Buildozer

## 🚀 How to Build the APK
This repository is configured with a 100% cloud-based build pipeline. **No local installation of Android Studio is required.**

1. Commit any changes to the `main` branch.
2. Navigate to the **Actions** tab in this GitHub repository.
3. The `Build SHDA Android APK` workflow will trigger automatically.
4. Once completed (approx. 10-15 minutes), scroll to the **Artifacts** section of the workflow run.
5. Download the `.zip` file containing the compiled `app-debug.apk`.

## 📂 Project Structure
* `/core`: Database initialization and secure authentication logic.
* `/ui`: Kivy screen managers and multi-lingual user interface layouts.
* `/services`: Background workers for Firebase syncing and PDF generation.
* `.github/workflows`: The automated Buildozer CI/CD pipeline.
