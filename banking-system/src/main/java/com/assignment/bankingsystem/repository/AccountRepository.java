package com.assignment.bankingsystem.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.bankingsystem.entity.Account;
        import java.util.List;

        public interface AccountRepository extends JpaRepository<Account, Long> {
}
