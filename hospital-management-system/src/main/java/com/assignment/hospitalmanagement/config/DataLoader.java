package com.assignment.hospitalmanagement.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.hospitalmanagement.entity.Doctor;
import com.assignment.hospitalmanagement.entity.Patient;
import com.assignment.hospitalmanagement.repository.DoctorRepository;
import com.assignment.hospitalmanagement.repository.PatientRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadHospitalData(DoctorRepository doctorRepository, PatientRepository patientRepository) {
        return args -> {
            if (doctorRepository.count() == 0) {
                        Doctor doctor = new Doctor();
                        doctor.setName("Dr. Ayush Kumar");
                doctor.setSpecialization("Cardiology");
                doctor.setAppointments(new ArrayList<>());
                doctorRepository.save(doctor);

                        Patient patient = new Patient();
                        patient.setName("Priyanshu Sharma");
                patient.setAge(29);
                patient.setAppointments(new ArrayList<>());
                patientRepository.save(patient);
            }
        };
    }
}
