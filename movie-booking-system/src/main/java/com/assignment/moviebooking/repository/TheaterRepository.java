package com.assignment.moviebooking.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.moviebooking.entity.Theater;
        import java.util.List;

        public interface TheaterRepository extends JpaRepository<Theater, Long> {
}
