package com.assignment.leavemanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.leavemanagement.entity.LeaveRequest;
        import java.util.List;

        public interface LeaveRequestRepository extends JpaRepository<LeaveRequest, Long> {
}
