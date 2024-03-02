DROP TABLE IF EXISTS grade_points;
/* Assignment 6, Task 4: Create a table grade_points (grade, points) that maps letter grades to number grades */
CREATE TABLE grade_points(
    grade  VARCHAR(2) NOT NULL PRIMARY KEY,
    points FLOAT NOT NULL,
    CONSTRAINT check_points_range CHECK (points >= 0 AND points <= 4)
);
/* Insert values into the grade_points table */
INSERT INTO grade_points (grade, points)
VALUES ('A', 4.0);

INSERT INTO grade_points (grade, points)
VALUES ('A-', 3.7);

INSERT INTO grade_points (grade, points)
VALUES ('B+', 3.3);

INSERT INTO grade_points (grade, points)
VALUES ('B', 3.0);

INSERT INTO grade_points (grade, points)
VALUES ('B-', 2.7);

INSERT INTO grade_points (grade, points)
VALUES ('C+', 2.3);

INSERT INTO grade_points (grade, points)
VALUES ('C', 2.0);

INSERT INTO grade_points (grade, points)
VALUES ('C-', 1.7);

INSERT INTO grade_points (grade, points)
VALUES ('D+', 1.3);

INSERT INTO grade_points (grade, points)
VALUES ('D', 1.0);

INSERT INTO grade_points (grade, points)
VALUES ('D-', 0.7);

INSERT INTO grade_points (grade, points)
VALUES ('F+', 0.3);

INSERT INTO grade_points (grade, points)
VALUES ('F', 0.0);

/*Grade Points Table*/
SELECT * FROM grade_points ORDER BY points DESC;

/* Assignment 6, Task 5: Add a foreign key from the grade column in the existing takes table to the new grade_points table */
ALTER TABLE takes
ADD CONSTRAINT fk_grade
FOREIGN KEY(grade)
REFERENCES grade_points(grade);

/* Assignment 6, Task 6: Create a view v_takes_points that returns the data in takes table along with the numeric equivalent of the grade */
CREATE OR REPLACE VIEW v_takes_points AS
SELECT ID as student_id, course_id, sec_id, semester, year, takes.grade, points
FROM takes
LEFT JOIN grade_points
on takes.grade = grade_points.grade;

/* View table takes_points */
SELECT * FROM v_takes_points;

/* Assignment 6, Task 7: Total Grade Points for Shankar */
SELECT student.ID as student_id, student.name as student_name,
    ROUND(COALESCE(SUM(credits * points),0),3) AS total_grade_points
    FROM student
    LEFT JOIN takes
    ON student.id = takes.id
    JOIN course
    ON takes.course_id = course.course_id
    JOIN grade_points
    ON takes.grade = grade_points.grade
    WHERE student.ID = '12345' and takes.grade IS NOT NULL
    GROUP BY student.ID;

/*  Assignment 6, Task 8: GPA for Shankar */
SELECT
    s.id as student_id,
    ROUND(IFNULL(SUM(c.credits * gp.points)/SUM(c.credits),0),3) AS GPA
    FROM student as s
    LEFT JOIN takes as t
    ON s.id = t.id
    LEFT JOIN course as c
    ON t.course_id = c.course_id
    LEFT JOIN grade_points as gp
    ON t.grade = gp.grade
    WHERE t.id = '12345'
    GROUP BY t.id;

/* Assignment 6, Task 9: GPA for all students */
SELECT s.id as student_id,
    ROUND(IFNULL(SUM(c.credits * gp.points)/SUM(c.credits),0),3) AS GPA
    FROM student as s
    LEFT JOIN takes as t
    ON s.id = t.id
    LEFT JOIN course as c
    ON t.course_id = c.course_id
    LEFT JOIN grade_points as gp
    ON t.grade = gp.grade
    GROUP BY t.id;

/* Assignment 6, Task 10: Create a view v_student_gpa (id, gpa) that gives a dynamic version of the information in the previous question*/
CREATE OR REPLACE VIEW v_student_gpa AS
SELECT s.id as student_id,
    ROUND(IFNULL(SUM(c.credits * gp.points)/SUM(c.credits),0),3) AS GPA
    FROM student as s
    LEFT JOIN takes as t
    ON s.id = t.id
    LEFT JOIN course as c
    ON t.course_id = c.course_id
    LEFT JOIN grade_points as gp
    ON t.grade = gp.grade
    GROUP BY t.id;

/* View table v_student_gpa */
SELECT * FROM v_student_gpa;