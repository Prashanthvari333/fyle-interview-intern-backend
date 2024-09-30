WITH TeacherGradingCount AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
)
SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    grade = 'A'
    AND teacher_id = (
        SELECT
            teacher_id
        FROM
            TeacherGradingCount
        ORDER BY
            total_graded DESC
        LIMIT 1
    );
