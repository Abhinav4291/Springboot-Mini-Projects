package com.assignment.collegemanagement.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.collegemanagement.entity.Course;
import com.assignment.collegemanagement.entity.Faculty;
import com.assignment.collegemanagement.entity.Student;
import com.assignment.collegemanagement.service.CollegeService;

@RestController
@RequestMapping("/api/college")
public class CollegeRestController {

    private final CollegeService collegeService;

    public CollegeRestController(CollegeService collegeService) {
        this.collegeService = collegeService;
    }

    @GetMapping("/students")
    public List<Student> getStudents() {
        return collegeService.getAllStudents();
    }

    @GetMapping("/courses")
    public List<Course> getCourses() {
        return collegeService.getAllCourses();
    }

    @GetMapping("/faculty")
    public List<Faculty> getFaculty() {
        return collegeService.getAllFaculty();
    }

    @GetMapping("/students/by-course")
    public List<Student> getStudentsByCourse(@RequestParam Long courseId) {
        return collegeService.getStudentsForCourse(courseId);
    }

    @GetMapping("/courses/by-faculty")
    public List<Course> getCoursesByFaculty(@RequestParam Long facultyId) {
        return collegeService.getCoursesHandledByFaculty(facultyId);
    }

    @PostMapping("/students")
    public Student addStudent(@RequestBody Student student) {
        return collegeService.saveStudent(student);
    }

    @PostMapping("/courses")
    public Course addCourse(@RequestBody Course course) {
        return collegeService.saveCourse(course);
    }

    @PostMapping("/faculty")
    public Faculty addFaculty(@RequestBody Faculty faculty) {
        return collegeService.saveFaculty(faculty);
    }

    @PostMapping("/enroll")
    public ResponseEntity<String> enrollStudent(@RequestParam Long studentId, @RequestParam Long courseId) {
        collegeService.enrollStudent(studentId, courseId);
        return ResponseEntity.ok("Student enrolled successfully");
    }

    @PostMapping("/assign-faculty")
    public ResponseEntity<String> assignFaculty(@RequestParam Long facultyId, @RequestParam Long courseId) {
        collegeService.assignFaculty(facultyId, courseId);
        return ResponseEntity.ok("Faculty assigned successfully");
    }
}
