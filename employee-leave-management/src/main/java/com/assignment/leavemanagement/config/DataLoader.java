package com.assignment.leavemanagement.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.leavemanagement.entity.Employee;
import com.assignment.leavemanagement.entity.Manager;
import com.assignment.leavemanagement.repository.EmployeeRepository;
import com.assignment.leavemanagement.repository.ManagerRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadLeaveData(ManagerRepository managerRepository, EmployeeRepository employeeRepository) {
        return args -> {
            if (managerRepository.count() == 0) {
                        Manager manager = new Manager();
                        manager.setName("Priyanshu Sharma");
                        manager.setDepartment("Project Management");
                manager.setEmployees(new ArrayList<>());
                managerRepository.save(manager);

                        Employee employee = new Employee();
                        employee.setName("Rakshit Pandey");
                        employee.setDesignation("Software Engineer");
                employee.setManager(manager);
                employee.setLeaveRequests(new ArrayList<>());
                employeeRepository.save(employee);
            }
        };
    }
}
