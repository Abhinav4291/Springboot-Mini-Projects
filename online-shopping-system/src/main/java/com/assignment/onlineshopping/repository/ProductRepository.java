package com.assignment.onlineshopping.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.onlineshopping.entity.Product;
        import java.util.List;

        public interface ProductRepository extends JpaRepository<Product, Long> {
}
