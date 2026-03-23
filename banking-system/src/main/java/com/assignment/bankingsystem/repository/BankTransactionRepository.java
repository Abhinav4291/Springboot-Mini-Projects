package com.assignment.bankingsystem.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.bankingsystem.entity.BankTransaction;
        import java.util.List;

        public interface BankTransactionRepository extends JpaRepository<BankTransaction, Long> {

    List<BankTransaction> findByAccountIdOrderByTransactionTimeDesc(Long accountId);
}
