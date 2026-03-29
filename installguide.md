# 🚀 NeuroSQL Installation Guide (Ultimate Step-by-Step for Beginners)

Welcome! This guide is written so that **anyone**—even without a technical background—can get the NeuroSQL Web Application running on their computer. We will cover exactly what commands to type for both **Windows** and **Ubuntu (Linux)**, and how to fix common errors you might see along the way.

---

## ⚡ The One-Shot Quick Start Command ⚡
If you already have Python (3.10-3.13) installed and just want to copy-paste a single command that does **everything** (creates the bubble, installs requirements, applies the missing drivers tweak, and launches the server), pick your operating system below:

**💻 For Windows (Copy & Paste into Command Prompt):**
```cmd
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && pip install "vanna[openai,sqlite]" && python -m uvicorn main:app --port 8000
```
*(If using PowerShell, replace `venv\Scripts\activate` with `.\venv\Scripts\Activate.ps1`)*

**🐧 For Ubuntu / Mac (Copy & Paste into Terminal):**
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install "vanna[openai,sqlite]" && python3 -m uvicorn main:app --port 8000
```

> *If these commands fail or you get errors, please follow the meticulous step-by-step guide below.*

---

## Step 1: Install the Right Version of Python

Python is the programming language that runs this app. However, **using the right version is critical**. 

🚨 **CRITICAL WARNING:** Do **NOT** use Python 3.14 or newer. During our testing, bleeding-edge versions failed to install packages like `pandas` properly, resulting in scary red errors talking about "C++ compilation." 
✅ **Recommended Versions:** **Python 3.10, 3.11, 3.12, or 3.13**.

* **For Windows:**
  1. Go to the [Official Python Downloads Page](https://www.python.org/downloads/windows/).
  2. Download the installer for Python 3.12 or 3.13.
  3. **VERY IMPORTANT:** On the very first screen of the installer, **check the box that says "Add python.exe to PATH"** at the bottom before clicking Install. If you forget this, nothing will work!
* **For Ubuntu (Linux):**
  Open your Terminal (press `Ctrl + Alt + T`) and run:
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip
  ```

---

## Step 2: Open Your Terminal & Navigate to the Folder

You need to tell your computer to look inside the folder where you downloaded this code.

* **For Windows:** 
  1. Open the folder containing the app files in File Explorer.
  2. Click on the address bar at the top, type `cmd`, and press **Enter**. A black box (Command Prompt) will pop up automatically tied to the correct folder.
* **For Ubuntu:**
  1. Open Terminal.
  2. Use the `cd` (change directory) command to go to your downloaded folder. For example: 
     `cd ~/Downloads/takeHomeTask-master/takeHomeTask-master`

---

## Step 3: Create a "Virtual Environment" (Highly Recommended)

Think of a virtual environment as a safety bubble. It keeps the app's files completely separate from the rest of your computer. This absolutely prevents permission errors which frustrate many beginners.

1. **Create the bubble:**
   * **Windows:** `python -m venv venv`
   * **Ubuntu:** `python3 -m venv venv`
   
2. **Activate the bubble:**
   * **Windows Command Prompt:** `venv\Scripts\activate`
     *(If you are using Windows PowerShell, type: `.\venv\Scripts\Activate.ps1`)*
   * **Ubuntu:** `source venv/bin/activate`

*(You will know it worked if you magically see `(venv)` appear at the very start of your typing line).*

---

## Step 4: Install the Required Packages & Fixes

Now we will download all the coding libraries the app needs from the internet.

1. **Install the base requirements:**
   Type the following exactly as written:
   ```bash
   pip install -r requirements.txt
   ```
   *(Wait a few minutes for the loading bars to finish).*

2. **🛠️ The Secret Tweak (Fixing Missing Drivers):**
   The original developers forgot to list a crucial set of files required for the A.I. tools to talk to the local database. If we don't fix this now, the app will crash later. The fix is running this extra command:
   ```bash
   pip install "vanna[openai,sqlite]"
   ```

---

## Step 5: Launch the Application!

The original code came with a helper script called `generate_results.py`. However, this script tries to launch the web server silently strictly in the background. If something goes wrong, it won't tell you why—it just fails silently. 

**🛠️ The Tweak to Launch the Server Directly:**
Instead of using the helper script, we are going to start the web server manually so we can see its heartbeat.

Type this exact command:
```bash
python -m uvicorn main:app --port 8000
```
*(On Ubuntu, if `python` doesn't work, just type `python3 -m uvicorn main:app --port 8000`)*

**You're Done! 🎉**
When you see `Application startup complete.` on the screen, leave that black window open. Open Google Chrome, Safari, or Microsoft Edge, and type this into the web address bar:
**http://127.0.0.1:8000/**

---

## 🛠️ Troubleshooting & Error Tackling Guide

### ❌ Error: `'python' is not recognized as an internal or external command` (Windows)
* **Why it happens:** Your computer doesn't know where Python is because you forgot to check the "Add Python to PATH" box during installation.
* **How to fix:** Uninstall Python from your computer, run the downloaded installer again, and make sure that box at the very bottom is checked!

### ❌ Error: `metadata-generation-failed` or huge red walls of text mentioning `Building wheel for pandas`
* **Why it happens:** You are using a brand new, experimental version of Python (like 3.14) that isn't fully supported by community packages yet. It's trying to build the code from scratch and failing.
* **How to fix:** Install a stable Python 3.12 or 3.13 instead. Delete the `venv` folder entirely and start fresh from Step 3.

### ❌ Error: `ImportError: openai package is required`
* **Why it happens:** You skipped our Secret Tweak in Step 4.
* **How to fix:** Make sure your virtual environment is activated (you see `(venv)`) and run: `pip install "vanna[openai,sqlite]"`

### ❌ Error: `externally-managed-environment` or `This environment is externally managed`
* **Why it happens:** Ubuntu and modern Python versions try to stop you from installing random packages dangerously over your entire computer (global system).
* **How to fix, Option 1 (Best):** Do **Step 3** properly and activate the virtual environment so it installs safely inside the bubble!
* **How to fix, Option 2 (Quick&Hack):** If you absolutely MUST run it without a virtual environment, append `--break-system-packages` to your pip installs. Like this:  
  `pip install -r requirements.txt --break-system-packages`
