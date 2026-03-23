package com.assignment.hospitalmanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.hospitalmanagement.entity.Patient;
        import java.util.List;

        public interface PatientRepository extends JpaRepository<Patient, Long> {
}
