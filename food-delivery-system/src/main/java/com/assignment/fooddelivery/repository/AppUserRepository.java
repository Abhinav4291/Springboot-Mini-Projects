package com.assignment.fooddelivery.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.fooddelivery.entity.AppUser;
        import java.util.List;

        public interface AppUserRepository extends JpaRepository<AppUser, Long> {
}
