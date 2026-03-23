package com.assignment.fooddelivery.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.fooddelivery.entity.Restaurant;
        import java.util.List;

        public interface RestaurantRepository extends JpaRepository<Restaurant, Long> {
}
