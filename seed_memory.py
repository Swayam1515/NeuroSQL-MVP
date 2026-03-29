from vanna_setup import memory
from vanna.core.tool import ToolContext
from vanna.core.user import User
import asyncio
import sqlite3

async def seed_memory():
    # Provide a mock context for the seeded tools
    user = User(id="system")
    ctx = ToolContext(user=user, conversation_id="seed", request_id="seed", agent_memory=memory)

    # Only seed if memory is empty
    if len(memory._memories) > 0:
        return
        
    # Seed DDL first
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schema_info = "Database Schema:\n\n" + "\n\n".join([t[0] for t in tables if t[0]])
    conn.close()
    
    await memory.save_text_memory(schema_info, context=ctx)
    
    # 15 pre-seeded Q&A Pairs
    qa_pairs = [
        # Patient queries
        ("How many patients do we have?", "SELECT COUNT(*) AS total_patients FROM patients"),
        ("List all female patients from New York", "SELECT * FROM patients WHERE gender = 'F' AND city = 'New York'"),
        ("Which city has the most patients?", "SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1"),
        # Doctor queries
        ("List all doctors and their specializations", "SELECT name, specialization FROM doctors"),
        ("Which doctor has the most appointments?", "SELECT d.name, COUNT(a.id) AS appt_count FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.name ORDER BY appt_count DESC LIMIT 1"),
        ("Show average appointment duration by doctor", "SELECT d.name, AVG(t.duration_minutes) AS avg_duration FROM doctors d JOIN appointments a ON d.id = a.doctor_id JOIN treatments t ON a.id = t.appointment_id GROUP BY d.name"),
        # Appointment queries
        ("Show me appointments for last month", "SELECT * FROM appointments WHERE appointment_date >= date('now', '-1 month')"),
        ("How many cancelled appointments last quarter?", "SELECT COUNT(*) FROM appointments WHERE status = 'Cancelled' AND appointment_date >= date('now', '-3 months')"),
        ("What percentage of appointments are no-shows?", "SELECT (CAST(SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100 AS no_show_percentage FROM appointments"),
        # Financial queries
        ("What is the total revenue?", "SELECT SUM(total_amount) AS total_revenue FROM invoices"),
        ("Show revenue by doctor", "SELECT d.name, SUM(i.total_amount) AS total_revenue FROM invoices i JOIN appointments a ON a.patient_id = i.patient_id JOIN doctors d ON d.id = a.doctor_id GROUP BY d.name ORDER BY total_revenue DESC"),
        ("Top 5 patients by spending", "SELECT p.first_name, p.last_name, SUM(i.total_amount) as total_spending FROM patients p JOIN invoices i ON p.id = i.patient_id GROUP BY p.id ORDER BY total_spending DESC LIMIT 5"),
        ("Show unpaid invoices", "SELECT * FROM invoices WHERE status != 'Paid'"),
        ("Average treatment cost by specialization", "SELECT d.specialization, AVG(t.cost) AS avg_cost FROM doctors d JOIN appointments a ON d.id = a.doctor_id JOIN treatments t ON a.id = t.appointment_id GROUP BY d.specialization"),
        # Time-based queries
        ("Show monthly appointment count for the past 6 months", "SELECT strftime('%Y-%m', appointment_date) AS month, COUNT(*) AS count FROM appointments WHERE appointment_date >= date('now', '-6 months') GROUP BY month ORDER BY month")
    ]
    
    for q, s in qa_pairs:
        await memory.save_tool_usage(
            question=q,
            tool_name="run_sql",
            args={"sql": s},
            context=ctx,
            success=True
        )
        
    print(f"Successfully seeded {len(qa_pairs)} question-SQL pairs into DemoAgentMemory.")

if __name__ == "__main__":
    asyncio.run(seed_memory())
