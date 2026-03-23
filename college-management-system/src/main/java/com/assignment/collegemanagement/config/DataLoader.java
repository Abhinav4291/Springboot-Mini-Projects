package com.assignment.collegemanagement.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.collegemanagement.entity.Course;
import com.assignment.collegemanagement.entity.Student;
import com.assignment.collegemanagement.repository.CourseRepository;
import com.assignment.collegemanagement.repository.StudentRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadCollegeData(StudentRepository studentRepository, CourseRepository courseRepository) {
        return args -> {
            if (studentRepository.count() == 0) {
                Student student = new Student();
                student.setName("Rishabh Shukla");
                student.setDepartment("Computer Science / IT");
                student.setCourses(new ArrayList<>());
                studentRepository.save(student);

                Course course = new Course();
                course.setTitle("Database Systems");
                course.setCode("CS301");
                course.setStudents(new ArrayList<>());
                courseRepository.save(course);
            }
        };
    }
}
