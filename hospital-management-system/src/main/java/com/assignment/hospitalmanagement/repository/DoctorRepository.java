package com.assignment.hospitalmanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.hospitalmanagement.entity.Doctor;
        import java.util.List;

        public interface DoctorRepository extends JpaRepository<Doctor, Long> {
}
