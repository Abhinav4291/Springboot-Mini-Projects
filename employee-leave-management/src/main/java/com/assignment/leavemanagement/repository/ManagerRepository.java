package com.assignment.leavemanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.leavemanagement.entity.Manager;
        import java.util.List;

        public interface ManagerRepository extends JpaRepository<Manager, Long> {
}
