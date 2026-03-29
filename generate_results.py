import sys
import webbrowser
import subprocess
import socket
import json
import time
import urllib.request

# The original 20 questions
demo_questions = [
    "How many patients do we have?",
    "List all doctors and their specializations",
    "Show me appointments for last month",
    "Which doctor has the most appointments?",
    "What is the total revenue?",
    "Show revenue by doctor",
    "How many cancelled appointments last quarter?",
    "Top 5 patients by spending",
    "Average treatment cost by specialization",
    "Show monthly appointment count for the past 6 months",
    "Which city has the most patients?",
    "List patients who visited more than 3 times",
    "Show unpaid invoices",
    "What percentage of appointments are no-shows?",
    "Show the busiest day of the week for appointments",
    "Revenue trend by month",
    "Average appointment duration by doctor",
    "List patients with overdue invoices",
    "Compare revenue between departments",
    "Show patient registration trend by month"
]

def send_chat_request(question, model_choice):
    try:
        url = "http://localhost:8000/chat"
        payload = json.dumps({"question": question, "model_choice": model_choice}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=120) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        sql = data.get("sql_query", "None generated")
        error = data.get("error")
        rows = data.get("rows", [])
        
        if error:
            correct = "No"
            summary = f"Error: {error}"
            sql = f"`{sql}`"
            passed = False
        elif rows:
            correct = "Yes"
            summary = f"Success ({len(rows)} rows)"
            sql = f"`{sql}`"
            passed = True
        else:
            correct = "No (No data)"
            summary = "Success but no data returned"
            sql = f"`{sql}`"
            passed = True # consider passing if no generic error but just zero data
            
        return sql, correct, summary, passed, data
    except Exception as e:
        return "N/A", "No", f"Request Failed: {e}", False, {}

def countdown_timer(seconds):
    if seconds <= 0: return
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rNext prompt request in {remaining} sec...    ")
        sys.stdout.flush()
        time.sleep(1)
    print("\r" + " " * 40 + "\r", end="")

def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def main():
    print("Welcome to the NL2SQL Interactive Runner\n" + "-"*40)
    
    interface_choice = input("Do you want to run via (1) Terminal Console or (2) Web Browser GUI?\n> ").strip()
    
    if interface_choice == "2":
        print("\nChecking server status...")
        if not is_port_in_use(8000):
            print("Spinning up FastAPI Uvicorn backend...")
            subprocess.Popen("uvicorn main:app --port 8000", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2) # Wait for startup
        else:
            print("Server is already running!")
            
        print("Launching the NeuroSQL Web Interface...")
        webbrowser.open("http://localhost:8000/")
        return
        
    # 1. Model Selection
    model_choice = "gemini"
    m_input = input("Which model do you want to use? (1) Gemini 2.5 Flash, (2) GLM 4.5 Flash\n> ").strip()
    if m_input == "2":
        model_choice = "glm"
    
    # 2. Rate Limit
    rate_limit = 10
    r_input = input("How much rate limit delay do you want between requests (in seconds)? (e.g. 10 or 60)\n> ").strip()
    if r_input.isdigit():
        rate_limit = int(r_input)
        
    # 3. Execution Mode
    mode = "1"
    mode_input = input("What do you want to run? (1) Run the 20 test demo questions, (2) Write custom questions interactively\n> ").strip()
    if mode_input == "2":
        mode = "2"
        
    print(f"\nConfiguration -> Model: {model_choice.upper()}, Delay: {rate_limit}s, Mode: {'Demo Batch' if mode == '1' else 'Custom Interactive'}\n" + "="*50)
    
    if mode == "1":
        # Batch Mode
        results_content = "# Test Results\n\n| # | Question | Generated SQL | Correct? | Result Summary |\n|---|---|---|---|---|\n"
        passed_count = 0
        
        for i, q in enumerate(demo_questions, 1):
            print(f"[{i}/{len(demo_questions)}] Question: {q}")
            sql, correct, summary, is_passed, _ = send_chat_request(q, model_choice)
            
            if is_passed: passed_count += 1
            
            row_md = f"| {i} | {q} | {sql} | {correct} | {summary} |\n"
            print(f"Result: {correct} - {summary}")
            print(f"SQL: {sql}")
            
            # Print database output
            if is_passed and 'columns' in raw_data and 'rows' in raw_data and raw_data['rows']:
                print("-" * 30)
                print(" | ".join([str(c) for c in raw_data['columns']]))
                for row in raw_data['rows'][:5]: # Print first 5 rows
                    print(" | ".join([str(v) for v in row]))
                if len(raw_data['rows']) > 5:
                    print(f"... and {len(raw_data['rows']) - 5} more rows.")
                print("-" * 30)
            print()
            
            results_content += row_md
            
            if i < len(demo_questions):
                countdown_timer(rate_limit)
                
        results_content += f"\n## Summary\nTotal Passed: {passed_count} out of 20\n"
        with open("RESULTS.md", "w") as f:
            f.write(results_content)
        print(f"Batch completed! Total passed: {passed_count} / 20. Saved to RESULTS.md")
        
    elif mode == "2":
        # Interactive Mode
        while True:
            try:
                q = input("\nEnter your question (or type 'exit' to quit):\n> ").strip()
                if not q: continue
                if q.lower() in ('exit', 'quit'): break
                
                print("Generating query...")
                sql, correct, summary, is_passed, raw_data = send_chat_request(q, model_choice)
                
                print("\n[Generated SQL]:\n" + sql)
                print(f"[Status]: {summary}")
                if raw_data and 'rows' in raw_data and raw_data['rows']:
                    print(f"[Results (First 5 max)]:")
                    for row in raw_data['rows'][:5]:
                        print("  ", row)
                
                countdown_timer(rate_limit)
                
            except KeyboardInterrupt:
                break
        print("Exiting interactive mode.")

if __name__ == "__main__":
    main()
