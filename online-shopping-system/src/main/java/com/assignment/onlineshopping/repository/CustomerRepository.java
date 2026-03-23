package com.assignment.onlineshopping.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.onlineshopping.entity.Customer;
        import java.util.List;

        public interface CustomerRepository extends JpaRepository<Customer, Long> {
}
