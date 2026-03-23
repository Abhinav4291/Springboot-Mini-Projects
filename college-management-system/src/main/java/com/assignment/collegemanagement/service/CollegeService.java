package com.assignment.collegemanagement.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.assignment.collegemanagement.entity.Course;
import com.assignment.collegemanagement.entity.Faculty;
import com.assignment.collegemanagement.entity.Student;
import com.assignment.collegemanagement.exception.ResourceNotFoundException;
import com.assignment.collegemanagement.repository.CourseRepository;
import com.assignment.collegemanagement.repository.FacultyRepository;
import com.assignment.collegemanagement.repository.StudentRepository;

@Service
public class CollegeService {

    private final StudentRepository studentRepository;
    private final CourseRepository courseRepository;
    private final FacultyRepository facultyRepository;

    public CollegeService(StudentRepository studentRepository, CourseRepository courseRepository,
            FacultyRepository facultyRepository) {
        this.studentRepository = studentRepository;
        this.courseRepository = courseRepository;
        this.facultyRepository = facultyRepository;
    }

    public List<Student> getAllStudents() {
        return studentRepository.findAll();
    }

    public List<Course> getAllCourses() {
        return courseRepository.findAll();
    }

    public List<Course> getAllCoursesWithDetails() {
        return courseRepository.findAllWithFacultyAndStudents();
    }

    public List<Faculty> getAllFaculty() {
        return facultyRepository.findAll();
    }

    public List<Student> getStudentsForCourse(Long courseId) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new ResourceNotFoundException("Course not found"));
        return course.getStudents();
    }

    public List<Course> getCoursesHandledByFaculty(Long facultyId) {
        return courseRepository.findAllWithFacultyAndStudents().stream()
                .filter(course -> course.getFaculty() != null && course.getFaculty().getId().equals(facultyId))
                .toList();
    }

    public Student saveStudent(Student student) {
        if (student.getCourses() == null) {
            student.setCourses(new ArrayList<>());
        }
        return studentRepository.save(student);
    }

    public Course saveCourse(Course course) {
        if (course.getStudents() == null) {
            course.setStudents(new ArrayList<>());
        }
        return courseRepository.save(course);
    }

    public Faculty saveFaculty(Faculty faculty) {
        if (faculty.getCourses() == null) {
            faculty.setCourses(new ArrayList<>());
        }
        return facultyRepository.save(faculty);
    }

    @Transactional
    public void enrollStudent(Long studentId, Long courseId) {
        if (!studentRepository.existsById(studentId)) {
            throw new ResourceNotFoundException("Student not found");
        }
        if (!courseRepository.existsById(courseId)) {
            throw new ResourceNotFoundException("Course not found");
        }
        if (!courseRepository.existsEnrollment(courseId, studentId)) {
            courseRepository.enrollStudentInCourse(courseId, studentId);
        }
    }

    @Transactional
    public void assignFaculty(Long facultyId, Long courseId) {
        if (!facultyRepository.existsById(facultyId)) {
            throw new ResourceNotFoundException("Faculty not found");
        }
        if (!courseRepository.existsById(courseId)) {
            throw new ResourceNotFoundException("Course not found");
        }
        courseRepository.assignFacultyToCourse(facultyId, courseId);
    }
}
