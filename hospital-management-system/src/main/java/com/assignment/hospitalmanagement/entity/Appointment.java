package com.assignment.hospitalmanagement.entity;

        import jakarta.persistence.*;
import java.time.LocalDate;

        @Entity
        public class Appointment {

        @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDate appointmentDate;

    private String reason;

@ManyToOne
    @JoinColumn(name = "doctor_id")
    private Doctor doctor;

@ManyToOne
    @JoinColumn(name = "patient_id")
    private Patient patient;

            public Appointment() {
            }

            public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDate getAppointmentDate() {
        return appointmentDate;
    }

    public void setAppointmentDate(LocalDate appointmentDate) {
        this.appointmentDate = appointmentDate;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public Doctor getDoctor() {
        return doctor;
    }

    public void setDoctor(Doctor doctor) {
        this.doctor = doctor;
    }

    public Patient getPatient() {
        return patient;
    }

    public void setPatient(Patient patient) {
        this.patient = patient;
    }
        }
