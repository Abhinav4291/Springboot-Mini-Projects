package com.assignment.hospitalmanagement.service;

import java.time.LocalDate;
import java.util.List;

import org.springframework.stereotype.Service;

import com.assignment.hospitalmanagement.entity.Appointment;
import com.assignment.hospitalmanagement.entity.Doctor;
import com.assignment.hospitalmanagement.entity.Patient;
import com.assignment.hospitalmanagement.exception.ResourceNotFoundException;
import com.assignment.hospitalmanagement.repository.AppointmentRepository;
import com.assignment.hospitalmanagement.repository.DoctorRepository;
import com.assignment.hospitalmanagement.repository.PatientRepository;

@Service
public class HospitalService {

    private final DoctorRepository doctorRepository;
    private final PatientRepository patientRepository;
    private final AppointmentRepository appointmentRepository;

    public HospitalService(DoctorRepository doctorRepository, PatientRepository patientRepository,
            AppointmentRepository appointmentRepository) {
        this.doctorRepository = doctorRepository;
        this.patientRepository = patientRepository;
        this.appointmentRepository = appointmentRepository;
    }

    public List<Doctor> getAllDoctors() {
        return doctorRepository.findAll();
    }

    public List<Patient> getAllPatients() {
        return patientRepository.findAll();
    }

    public List<Appointment> getAllAppointments() {
        return appointmentRepository.findAll();
    }

    public Doctor saveDoctor(Doctor doctor) {
        return doctorRepository.save(doctor);
    }

    public Patient savePatient(Patient patient) {
        return patientRepository.save(patient);
    }

    public Appointment bookAppointment(Long doctorId, Long patientId, LocalDate appointmentDate, String reason) {
        Doctor doctor = doctorRepository.findById(doctorId)
                .orElseThrow(() -> new ResourceNotFoundException("Doctor not found"));
        Patient patient = patientRepository.findById(patientId)
                .orElseThrow(() -> new ResourceNotFoundException("Patient not found"));
        Appointment appointment = new Appointment();
        appointment.setDoctor(doctor);
        appointment.setPatient(patient);
        appointment.setAppointmentDate(appointmentDate);
        appointment.setReason(reason);
        return appointmentRepository.save(appointment);
    }

    public List<Appointment> getAppointmentsForDoctor(Long doctorId) {
        return appointmentRepository.findByDoctorId(doctorId);
    }

    public List<Patient> getPatientsVisitedOnDate(LocalDate appointmentDate) {
        return appointmentRepository.findPatientsVisitedOnDate(appointmentDate);
    }
}
