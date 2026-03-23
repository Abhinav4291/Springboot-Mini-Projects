package com.assignment.hospitalmanagement.controller;

import java.time.LocalDate;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.assignment.hospitalmanagement.entity.Doctor;
import com.assignment.hospitalmanagement.entity.Patient;
import com.assignment.hospitalmanagement.service.HospitalService;

@Controller
public class HospitalViewController {

    private final HospitalService hospitalService;

    public HospitalViewController(HospitalService hospitalService) {
        this.hospitalService = hospitalService;
    }

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("doctors", hospitalService.getAllDoctors());
        model.addAttribute("patients", hospitalService.getAllPatients());
        model.addAttribute("appointments", hospitalService.getAllAppointments());
        model.addAttribute("doctor", new Doctor());
        model.addAttribute("patient", new Patient());
        return "index";
    }

    @PostMapping("/doctors/save")
    public String saveDoctor(Doctor doctor) {
        hospitalService.saveDoctor(doctor);
        return "redirect:/";
    }

    @PostMapping("/patients/save")
    public String savePatient(Patient patient) {
        hospitalService.savePatient(patient);
        return "redirect:/";
    }

    @PostMapping("/appointments/save")
    public String saveAppointment(@RequestParam Long doctorId, @RequestParam Long patientId,
            @RequestParam String appointmentDate, @RequestParam String reason) {
        hospitalService.bookAppointment(doctorId, patientId, LocalDate.parse(appointmentDate), reason);
        return "redirect:/";
    }
}
