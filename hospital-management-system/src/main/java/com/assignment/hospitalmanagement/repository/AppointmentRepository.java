package com.assignment.hospitalmanagement.repository;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.assignment.hospitalmanagement.entity.Appointment;
import com.assignment.hospitalmanagement.entity.Patient;

public interface AppointmentRepository extends JpaRepository<Appointment, Long> {

    List<Appointment> findByDoctorId(Long doctorId);

    List<Appointment> findByAppointmentDate(LocalDate appointmentDate);

    @Query("select a.patient from Appointment a where a.appointmentDate = :appointmentDate")
    List<Patient> findPatientsVisitedOnDate(LocalDate appointmentDate);
}
