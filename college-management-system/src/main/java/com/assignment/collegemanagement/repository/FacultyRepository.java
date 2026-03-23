package com.assignment.collegemanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.collegemanagement.entity.Faculty;
        import java.util.List;

        public interface FacultyRepository extends JpaRepository<Faculty, Long> {
}
