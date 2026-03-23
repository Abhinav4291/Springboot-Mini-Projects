package com.assignment.leavemanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.leavemanagement.entity.Employee;
        import java.util.List;

        public interface EmployeeRepository extends JpaRepository<Employee, Long> {
}
