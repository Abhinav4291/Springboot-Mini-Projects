package com.assignment.bankingsystem.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.bankingsystem.entity.Customer;
        import java.util.List;

        public interface CustomerRepository extends JpaRepository<Customer, Long> {
}
