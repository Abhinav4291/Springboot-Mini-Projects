package com.assignment.leavemanagement.controller;

import java.time.LocalDate;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.assignment.leavemanagement.entity.Employee;
import com.assignment.leavemanagement.entity.Manager;
import com.assignment.leavemanagement.service.LeaveManagementService;

@Controller
public class LeaveManagementViewController {

    private final LeaveManagementService leaveManagementService;

    public LeaveManagementViewController(LeaveManagementService leaveManagementService) {
        this.leaveManagementService = leaveManagementService;
    }

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("managers", leaveManagementService.getAllManagers());
        model.addAttribute("employees", leaveManagementService.getAllEmployees());
        model.addAttribute("requests", leaveManagementService.getAllRequests());
        model.addAttribute("manager", new Manager());
        model.addAttribute("employee", new Employee());
        return "index";
    }

    @PostMapping("/managers/save")
    public String saveManager(Manager manager) {
        leaveManagementService.saveManager(manager);
        return "redirect:/";
    }

    @PostMapping("/employees/save")
    public String saveEmployee(@RequestParam Long managerId, Employee employee) {
        leaveManagementService.saveEmployee(managerId, employee);
        return "redirect:/";
    }

    @PostMapping("/leave/apply")
    public String applyLeave(@RequestParam Long employeeId, @RequestParam String fromDate, @RequestParam String toDate,
            @RequestParam String reason) {
        leaveManagementService.applyLeave(employeeId, LocalDate.parse(fromDate), LocalDate.parse(toDate), reason);
        return "redirect:/";
    }

    @PostMapping("/leave/status")
    public String updateStatus(@RequestParam Long requestId, @RequestParam String status) {
        leaveManagementService.updateStatus(requestId, status);
        return "redirect:/";
    }
}
