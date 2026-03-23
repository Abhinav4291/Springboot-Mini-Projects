package com.assignment.moviebooking.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.moviebooking.entity.Movie;
        import java.util.List;

        public interface MovieRepository extends JpaRepository<Movie, Long> {
}
