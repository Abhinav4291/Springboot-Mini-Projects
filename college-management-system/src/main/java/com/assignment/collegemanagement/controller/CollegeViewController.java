package com.assignment.collegemanagement.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.assignment.collegemanagement.entity.Course;
import com.assignment.collegemanagement.entity.Faculty;
import com.assignment.collegemanagement.entity.Student;
import com.assignment.collegemanagement.service.CollegeService;

@Controller
public class CollegeViewController {

    private final CollegeService collegeService;

    public CollegeViewController(CollegeService collegeService) {
        this.collegeService = collegeService;
    }

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("students", collegeService.getAllStudents());
        model.addAttribute("courses", collegeService.getAllCourses());
        model.addAttribute("courseDetails", collegeService.getAllCoursesWithDetails());
        model.addAttribute("facultyList", collegeService.getAllFaculty());
        model.addAttribute("student", new Student());
        model.addAttribute("course", new Course());
        model.addAttribute("faculty", new Faculty());
        return "index";
    }

    @PostMapping("/students/save")
    public String saveStudent(Student student) {
        collegeService.saveStudent(student);
        return "redirect:/";
    }

    @PostMapping("/courses/save")
    public String saveCourse(Course course) {
        collegeService.saveCourse(course);
        return "redirect:/";
    }

    @PostMapping("/faculty/save")
    public String saveFaculty(Faculty faculty) {
        collegeService.saveFaculty(faculty);
        return "redirect:/";
    }

    @PostMapping("/enroll")
    public String enroll(@RequestParam Long studentId, @RequestParam Long courseId) {
        collegeService.enrollStudent(studentId, courseId);
        return "redirect:/";
    }

    @PostMapping("/assign-faculty")
    public String assignFaculty(@RequestParam Long facultyId, @RequestParam Long courseId) {
        collegeService.assignFaculty(facultyId, courseId);
        return "redirect:/";
    }
}
