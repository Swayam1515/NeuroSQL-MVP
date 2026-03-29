# Test Results

| # | Question | Generated SQL | Correct? | Result Summary |
|---|---|---|---|---|
| 1 | How many patients do we have? | `None generated` | No | Error: No SQL query could be generated. |
| 2 | List all doctors and their specializations | `None generated` | No | Error: No SQL query could be generated. |
| 3 | Show me appointments for last month | `None generated` | No | Error: No SQL query could be generated. |
| 4 | Which doctor has the most appointments? | `None generated` | No | Error: No SQL query could be generated. |
| 5 | What is the total revenue? | N/A | No | Request Failed: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /chat (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x716eb0abe060>: Failed to establish a new connection: [Errno 111] Connection refused')) |
| 6 | Show revenue by doctor | `None generated` | No | Error: No SQL query could be generated. |
| 7 | How many cancelled appointments last quarter? | `None generated` | No | Error: No SQL query could be generated. |
| 8 | Top 5 patients by spending | `None generated` | No | Error: No SQL query could be generated. |
| 9 | Average treatment cost by specialization | `None generated` | No | Error: No SQL query could be generated. |
| 10 | Show monthly appointment count for the past 6 months | `None generated` | No | Error: No SQL query could be generated. |
| 11 | Which city has the most patients? | `SELECT city, COUNT(id) AS patient_count
FROM patients
GROUP BY city
ORDER BY patient_count DESC
LIMIT 1;` | Yes | Success (1 rows) |
| 12 | List patients who visited more than 3 times | `None generated` | No | Error: No SQL query could be generated. |
| 13 | Show unpaid invoices | `None generated` | No | Error: No SQL query could be generated. |
| 14 | What percentage of appointments are no-shows? | `None generated` | No | Error: No SQL query could be generated. |
| 15 | Show the busiest day of the week for appointments | `None generated` | No | Error: No SQL query could be generated. |
| 16 | Revenue trend by month | `None generated` | No | Error: No SQL query could be generated. |
| 17 | Average appointment duration by doctor | `SELECT
  d.name AS doctor_name,
  AVG(t.duration_minutes) AS average_duration_minutes
FROM doctors AS d
JOIN appointments AS a
  ON d.id = a.doctor_id
JOIN treatments AS t
  ON a.id = t.appointment_id
GROUP BY
  d.name
ORDER BY
  d.name;` | Yes | Success (15 rows) |
| 18 | List patients with overdue invoices | `None generated` | No | Error: No SQL query could be generated. |
| 19 | Compare revenue between departments | `None generated` | No | Error: No SQL query could be generated. |
| 20 | Show patient registration trend by month | `None generated` | No | Error: No SQL query could be generated. |

## Summary
Total Passed: 2 out of 20
