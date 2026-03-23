package com.assignment.collegemanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.collegemanagement.entity.Student;
        import java.util.List;

        public interface StudentRepository extends JpaRepository<Student, Long> {
}
