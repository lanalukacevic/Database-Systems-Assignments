/* Chapter 3, Slide 52: List all departments along with the number of instructors in each department*/
select dept_name,
             ( select count(*)
                from instructor
                where department.dept_name = instructor.dept_name)
             as num_instructors
from department;

/*Chapter 3, Slide 14: Find the department names of all instructors, and remove duplicates */
select distinct dept_name
    from instructor;

/* Chapter 3, Slide 14: Find the department names of all instructors and does not remove the duplicates */
select all dept_name
from instructor;

/* Chapter 3, Slide 17: Find all instructors in the Comp. Sci department */
select name
from instructor
where dept_name = 'Comp. Sci.';

/* Chapter 3, Slide 17: Find all instructors in Comp. Sci. dept with salary > 70000 */
select name
from instructor
where dept_name = 'Comp. Sci.'  and salary > 70000;

/* Chapter 3, Slide 19: Find the names of all instructors who have taught some course and the course_id */
select name, course_id
from instructor , teaches
where instructor.ID = teaches.ID;

/* Chapter 3, Slide 19: Find the names of all instructors who have taught some course and the course_id */
select name, course_id
from instructor , teaches
where instructor.ID = teaches.ID
  and instructor. dept_name = 'Art';

/* Chapter 3, Slide 22: Find the names of all instructors whose name includes the substring dar */
select name
from instructor
where name like '%dar%';

/* Chapter 3, Slide 24: List in alphabetic order the names of all instructors */
select distinct name
    from instructor
       order by name;

/* Chapter 3, Slide 25: Find the names of all instructors with salary between $90,000 and $100,000 */
select name
from instructor
where salary between 90000 and 100000;


/* Sample query for testing */
SELECT * FROM instructor;

/*Homework Query #1: Retrieve all courses that have the letters a, e, i in THAT order in their names */
SELECT * FROM course
WHERE lower(title) like '%a%e%i%';

/*Homework Query #2: Retrieve all courses that have the letters a, e, i in ANY order in their names */
SELECT *
FROM course
WHERE LOWER(title) LIKE '%a%' AND LOWER(title) LIKE '%e%' AND LOWER(title) LIKE '%i%';

/*Homework Query #3: Retrieve the names of all students who failed a course (grade of F) along with the name of the course that they failed */
SELECT s.name AS student_name, c.title AS course_name
FROM student s
JOIN takes t ON s.ID = t.ID
JOIN course c ON t.course_id = c.course_id
WHERE t.grade = 'F';

/* Homework Query #4: Retrieve the percentage of solid A grades compared to all courses, and rename that column "Percent_A" */
SELECT count(grade) * 100/(SELECT count(grade) FROM takes) as Percent_A
From takes
where grade = 'A';

/* Homework Query #5: Retrieve the names and numbers of all courses that do not have prerequisites */
select title, course_id
from course
where course_id not in (select course_id from prereq);

/* Homework Query #6: Retrieve the names of all students and their advisors if they have one */
select s.name as student_name, a.i_ID as advisor_id, i.name as advisor_name
from student as s
left join advisor as a
on s.ID = a.s_id
left join instructor as i
on a.i_id = i.id;