-- Write query to get number of graded assignments for each student:
-- number_of_graded_assignments_for_each_student.sql

SELECT 
    s.id AS student_id,
    u.username AS student_name,
    COUNT(a.id) AS graded_assignments_count
FROM 
    students s
JOIN 
    users u ON s.user_id = u.id
LEFT JOIN 
    assignments a ON s.id = a.student_id AND a.state = 'GRADED'
GROUP BY 
    s.id, u.username
ORDER BY 
    s.id;