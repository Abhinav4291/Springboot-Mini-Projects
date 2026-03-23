package com.assignment.leavemanagement.service;

import java.time.LocalDate;
import java.util.List;

import org.springframework.stereotype.Service;

import com.assignment.leavemanagement.entity.Employee;
import com.assignment.leavemanagement.entity.LeaveRequest;
import com.assignment.leavemanagement.entity.Manager;
import com.assignment.leavemanagement.exception.ResourceNotFoundException;
import com.assignment.leavemanagement.repository.EmployeeRepository;
import com.assignment.leavemanagement.repository.LeaveRequestRepository;
import com.assignment.leavemanagement.repository.ManagerRepository;

@Service
public class LeaveManagementService {

    private final ManagerRepository managerRepository;
    private final EmployeeRepository employeeRepository;
    private final LeaveRequestRepository leaveRequestRepository;

    public LeaveManagementService(ManagerRepository managerRepository, EmployeeRepository employeeRepository,
            LeaveRequestRepository leaveRequestRepository) {
        this.managerRepository = managerRepository;
        this.employeeRepository = employeeRepository;
        this.leaveRequestRepository = leaveRequestRepository;
    }

    public List<Manager> getAllManagers() {
        return managerRepository.findAll();
    }

    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    public List<LeaveRequest> getAllRequests() {
        return leaveRequestRepository.findAll();
    }

    public Manager saveManager(Manager manager) {
        return managerRepository.save(manager);
    }

    public Employee saveEmployee(Long managerId, Employee employee) {
        Manager manager = managerRepository.findById(managerId)
                .orElseThrow(() -> new ResourceNotFoundException("Manager not found"));
        employee.setManager(manager);
        return employeeRepository.save(employee);
    }

    public LeaveRequest applyLeave(Long employeeId, LocalDate fromDate, LocalDate toDate, String reason) {
        Employee employee = employeeRepository.findById(employeeId)
                .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));
        LeaveRequest request = new LeaveRequest();
        request.setEmployee(employee);
        request.setFromDate(fromDate);
        request.setToDate(toDate);
        request.setReason(reason);
        request.setStatus("PENDING");
        return leaveRequestRepository.save(request);
    }

    public LeaveRequest updateStatus(Long requestId, String status) {
        LeaveRequest request = leaveRequestRepository.findById(requestId)
                .orElseThrow(() -> new ResourceNotFoundException("Leave request not found"));
        request.setStatus(status);
        return leaveRequestRepository.save(request);
    }
}
