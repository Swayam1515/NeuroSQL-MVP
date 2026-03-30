# Test Results

| # | Question | Generated SQL | Correct? | Result Summary |
|---|---|---|---|---|
| 1 | How many patients do we have? | `SELECT COUNT(*) FROM patients;` | Yes | Success (1 rows) |
| 2 | List all doctors and their specializations | `SELECT name, specialization FROM doctors;` | Yes | Success (15 rows) |
| 3 | Show me appointments for last month | `SELECT * FROM appointments WHERE appointment_date >= date('now', 'start of month', '-1 month') AND appointment_date < date('now', 'start of month');` | Yes | Success (142 rows) |
| 4 | Which doctor has the most appointments? | `SELECT d.name, COUNT(a.id) AS appointment_count FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.id ORDER BY appointment_count DESC LIMIT 1;` | Yes | Success (1 rows) |
| 5 | What is the total revenue? | `SELECT SUM(amount) FROM invoices WHERE status = 'paid';` | Yes | Success (1 rows) |
| 6 | Show revenue by doctor | `SELECT d.name, SUM(i.amount) FROM doctors d JOIN appointments a ON d.id = a.doctor_id JOIN invoices i ON a.id = i.appointment_id GROUP BY d.name;` | Yes | Success (15 rows) |
| 7 | How many cancelled appointments last quarter? | `SELECT COUNT(*) FROM appointments WHERE status = 'cancelled' AND appointment_date >= date('now', '-3 months');` | Yes | Success (1 rows) |
| 8 | Top 5 patients by spending | `SELECT p.name, SUM(i.amount) AS total_spent FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN invoices i ON a.id = i.appointment_id GROUP BY p.id ORDER BY total_spent DESC LIMIT 5;` | Yes | Success (5 rows) |
| 9 | Average treatment cost by specialization | `SELECT d.specialization, AVG(t.cost) FROM doctors d JOIN appointments a ON d.id = a.doctor_id JOIN treatments t ON a.id = t.appointment_id GROUP BY d.specialization;` | Yes | Success (8 rows) |
| 10 | Show monthly appointment count for the past 6 months | `SELECT strftime('%Y-%m', appointment_date) AS month, COUNT(*) FROM appointments WHERE appointment_date >= date('now', '-6 months') GROUP BY month;` | Yes | Success (6 rows) |
| 11 | Which city has the most patients? | `SELECT city, COUNT(id) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1;` | Yes | Success (1 rows) |
| 12 | List patients who visited more than 3 times | `SELECT p.name, COUNT(a.id) AS visit_count FROM patients p JOIN appointments a ON p.id = a.patient_id GROUP BY p.id HAVING visit_count > 3;` | Yes | Success (22 rows) |
| 13 | Show unpaid invoices | `SELECT * FROM invoices WHERE status = 'unpaid';` | Yes | Success (12 rows) |
| 14 | What percentage of appointments are no-shows? | `SELECT (COUNT(CASE WHEN status = 'no-show' THEN 1 END) * 100.0 / COUNT(*)) AS noshow_percentage FROM appointments;` | Yes | Success (1 rows) |
| 15 | Show the busiest day of the week for appointments | `SELECT strftime('%w', appointment_date) AS day_of_week, COUNT(*) AS count FROM appointments GROUP BY day_of_week ORDER BY count DESC LIMIT 1;` | Yes | Success (1 rows) |
| 16 | Revenue trend by month | `SELECT strftime('%Y-%m', i.invoice_date) AS month, SUM(i.amount) FROM invoices i GROUP BY month ORDER BY month;` | Yes | Success (12 rows) |
| 17 | Average appointment duration by doctor | `SELECT d.name AS doctor_name, AVG(t.duration_minutes) AS average_duration_minutes FROM doctors AS d JOIN appointments AS a ON d.id = a.doctor_id JOIN treatments AS t ON a.id = t.appointment_id GROUP BY d.name ORDER BY d.name;` | Yes | Success (15 rows) |
| 18 | List patients with overdue invoices | `SELECT DISTINCT p.name FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN invoices i ON a.id = i.appointment_id WHERE i.status = 'overdue';` | Yes | Success (8 rows) |
| 19 | Compare revenue between departments | `SELECT d.department, SUM(i.amount) AS revenue FROM doctors d JOIN appointments a ON d.id = a.doctor_id JOIN invoices i ON a.id = i.appointment_id GROUP BY d.department;` | Yes | Success (5 rows) |
| 20 | Show patient registration trend by month | `SELECT strftime('%Y-%m', registration_date) AS month, COUNT(*) FROM patients GROUP BY month ORDER BY month;` | Yes | Success (12 rows) |

## Summary
**Total Passed: 20 out of 20**
