package com.assignment.hospitalmanagement.controller;

import java.time.LocalDate;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.hospitalmanagement.entity.Appointment;
import com.assignment.hospitalmanagement.entity.Doctor;
import com.assignment.hospitalmanagement.entity.Patient;
import com.assignment.hospitalmanagement.service.HospitalService;

@RestController
@RequestMapping("/api/hospital")
public class HospitalRestController {

    private final HospitalService hospitalService;

    public HospitalRestController(HospitalService hospitalService) {
        this.hospitalService = hospitalService;
    }

    @GetMapping("/doctors")
    public List<Doctor> getDoctors() {
        return hospitalService.getAllDoctors();
    }

    @GetMapping("/patients")
    public List<Patient> getPatients() {
        return hospitalService.getAllPatients();
    }

    @GetMapping("/appointments")
    public List<Appointment> getAppointments() {
        return hospitalService.getAllAppointments();
    }

    @GetMapping("/appointments/by-doctor")
    public List<Appointment> getAppointmentsByDoctor(@RequestParam Long doctorId) {
        return hospitalService.getAppointmentsForDoctor(doctorId);
    }

    @GetMapping("/patients/by-date")
    public List<Patient> getPatientsByDate(@RequestParam String appointmentDate) {
        return hospitalService.getPatientsVisitedOnDate(LocalDate.parse(appointmentDate));
    }

    @PostMapping("/doctors")
    public Doctor addDoctor(@RequestBody Doctor doctor) {
        return hospitalService.saveDoctor(doctor);
    }

    @PostMapping("/patients")
    public Patient addPatient(@RequestBody Patient patient) {
        return hospitalService.savePatient(patient);
    }

    @PostMapping("/appointments")
    public Appointment bookAppointment(@RequestParam Long doctorId, @RequestParam Long patientId,
            @RequestParam String appointmentDate, @RequestParam String reason) {
        return hospitalService.bookAppointment(doctorId, patientId, LocalDate.parse(appointmentDate), reason);
    }
}
