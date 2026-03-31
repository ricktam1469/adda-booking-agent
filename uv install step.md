🏆 METHOD 1 — POWERSHELL (RECOMMENDED)

👉 Open PowerShell (Run as normal user)

Run:
irm https://astral.sh/uv/install.ps1 | iex
✅ After install, restart terminal and verify:
uv --version

👉 Expected:

uv 0.x.x
🏆 METHOD 2 — CMD (Command Prompt)

CMD cannot directly run PowerShell scripts, so do this:

Run:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
✅ Then verify:
uv --version
⚠️ IF uv NOT FOUND (VERY COMMON)

You may see:

'uv' is not recognized

👉 Fix:

1. Restart terminal (IMPORTANT)

OR

2. Add to PATH manually:

Check if installed here:

C:\Users\<your-user>\.cargo\bin

If yes → add this to PATH:

setx PATH "%PATH%;C:\Users\<your-user>\.cargo\bin"

Then restart terminal again

🏆 METHOD 3 — ALTERNATIVE (IF SCRIPT BLOCKED)

If PowerShell blocks script:

Run first:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Then run install again.

🧠 WHAT HAPPENS AFTER INSTALL

uv will:

✔ Auto install Python
✔ Manage virtual env
✔ Install dependencies
✔ Run your script
🚀 QUICK TEST

After install:

uv init test-project
cd test-project
uv run python -c "print('uv working')"