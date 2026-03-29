# 🚀 Ultimate Beginner's Guide to GitHub (Terminal Edition)

If you've never used the terminal to push code to GitHub, don't worry! This guide breaks down the four simple "Golden Steps" you'll use every single day as a developer.

---

## 0. Initial Setup & Identity (Do this Once!)

Before pushing code, telling Git **who you are** is critical. If your commits are showing up as `stryker` instead of your real name, it's because Git is using your computer's default account name!

Run these two commands to permanently set the name and email that will appear on GitHub:
```bash
git config --global user.name "Your Real Name"
git config --global user.email "your.email@example.com"
```

### Logging into GitHub
If your terminal ever asks for a password when pushing code, **do not type your actual GitHub website password**. GitHub requires a "Personal Access Token" (PAT).
1. Go to GitHub.com > Settings > Developer Settings > Personal access tokens > Tokens (classic).
2. Generate a new token with "repo" permissions.
3. Paste that token into your terminal when it asks for the password!

---

## 1. The Core Workflow (The "Big Four")

Whenever you make changes to your code and want them to show up on GitHub, you run these commands in order:

### 📥 Step 1: `git add .`
**What it does:** This "stages" your changes. Imagine you're moving house—this is like putting your items into a cardboard box. The `.` means "add everything in this folder."

### 📝 Step 2: `git commit -m "Your message here"`
**What it does:** This "saves" your changes locally with a label. In our moving house analogy, this is like taping the box shut and writing "Kitchen Supplies" on the side. 
*Tip: Always write a short, helpful message in the quotes!*

### 🔄 Step 3: `git pull origin master`
**What it does:** This checks if there are any new changes on GitHub that you don't have on your computer yet. It "syncs" the cloud to your machine so you don't overwrite anyone else's work.

### 📤 Step 4: `git push origin master`
**What it does:** This uploads your "boxes" (commits) from your computer to GitHub. Once this finishes, your code is live on the web!

---

## 2. Working with Branches 🌿

Branches let you work on new features without breaking your main app! It's like making a parallel timeline of your code.

### Create a new Branch
To create a new branch named `cool-feature` and immediately switch to it:
```bash
git checkout -b cool-feature
```

### Switch back to Master
To go back to your original, safe timeline:
```bash
git checkout master
```

### Push a new Branch to GitHub
If you're on a new branch, `git push origin master` won't work! Tell GitHub the name of your new branch like this:
```bash
git push -u origin cool-feature
```

---

## 3. Common "Help Me!" Commands

| Command | What it's for |
| :--- | :--- |
| `git status` | Shows you exactly which files you changed but haven't saved yet. (Uses simple Green/Red colors!) |
| `git log --oneline` | Shows a history of all your past "saves" (commits) so you can see what you did. |
| `git diff` | Shows the exact lines of code you added or deleted before you save them. |

---

## 4. What to do if things go wrong?

### "The Conflict Error"
If Git says `CONFLICT (content): Merge conflict`, it means you and someone else (or you from another computer) changed the same line of code. 
1. Open the file mentioned in the error.
2. Look for `<<<<<<< HEAD` and `=======`. 
3. Delete the parts you don't want and the weird symbols.
4. Run `git add .` and `git commit` to fix it.

### "I committed the wrong thing!"
If you accidentally saved something you didn't mean to:
Run `git reset --soft HEAD~1`. This "un-tapes" your last box so you can add or remove items before saving again.

---

## 5. Cheat Sheet Summary
1. `git add .` (Pack the box)
2. `git commit -m "Done"` (Label it)
3. `git push origin master` (Send it!)

*Note: In some newer projects, the branch might be named `main` instead of `master`. If `origin master` fails, try `origin main`!*
