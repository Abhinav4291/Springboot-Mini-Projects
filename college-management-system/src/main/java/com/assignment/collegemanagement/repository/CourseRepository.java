package com.assignment.collegemanagement.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.assignment.collegemanagement.entity.Course;

public interface CourseRepository extends JpaRepository<Course, Long> {

    @Query("select distinct c from Course c left join fetch c.faculty left join fetch c.students")
    List<Course> findAllWithFacultyAndStudents();

    @Query(value = "select count(*) > 0 from student_course where course_id = :courseId and student_id = :studentId", nativeQuery = true)
    boolean existsEnrollment(@Param("courseId") Long courseId, @Param("studentId") Long studentId);

    @Modifying
    @Query(value = "insert into student_course(course_id, student_id) values (:courseId, :studentId)", nativeQuery = true)
    void enrollStudentInCourse(@Param("courseId") Long courseId, @Param("studentId") Long studentId);

    @Modifying
    @Query(value = "update course set faculty_id = :facultyId where id = :courseId", nativeQuery = true)
    void assignFacultyToCourse(@Param("facultyId") Long facultyId, @Param("courseId") Long courseId);
}
