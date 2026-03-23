package com.assignment.leavemanagement.controller;

import java.time.LocalDate;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.leavemanagement.entity.Employee;
import com.assignment.leavemanagement.entity.LeaveRequest;
import com.assignment.leavemanagement.entity.Manager;
import com.assignment.leavemanagement.service.LeaveManagementService;

@RestController
@RequestMapping("/api/leave")
public class LeaveManagementRestController {

    private final LeaveManagementService leaveManagementService;

    public LeaveManagementRestController(LeaveManagementService leaveManagementService) {
        this.leaveManagementService = leaveManagementService;
    }

    @GetMapping("/managers")
    public List<Manager> getManagers() {
        return leaveManagementService.getAllManagers();
    }

    @GetMapping("/employees")
    public List<Employee> getEmployees() {
        return leaveManagementService.getAllEmployees();
    }

    @GetMapping("/requests")
    public List<LeaveRequest> getRequests() {
        return leaveManagementService.getAllRequests();
    }

    @PostMapping("/managers")
    public Manager addManager(@RequestBody Manager manager) {
        return leaveManagementService.saveManager(manager);
    }

    @PostMapping("/employees")
    public Employee addEmployee(@RequestParam Long managerId, @RequestBody Employee employee) {
        return leaveManagementService.saveEmployee(managerId, employee);
    }

    @PostMapping("/apply")
    public LeaveRequest applyLeave(@RequestParam Long employeeId, @RequestParam String fromDate,
            @RequestParam String toDate, @RequestParam String reason) {
        return leaveManagementService.applyLeave(employeeId, LocalDate.parse(fromDate), LocalDate.parse(toDate), reason);
    }

    @PostMapping("/update-status")
    public LeaveRequest updateStatus(@RequestParam Long requestId, @RequestParam String status) {
        return leaveManagementService.updateStatus(requestId, status);
    }
}
