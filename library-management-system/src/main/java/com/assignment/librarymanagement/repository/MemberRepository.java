package com.assignment.librarymanagement.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import com.assignment.librarymanagement.entity.Member;
        import java.util.List;

        public interface MemberRepository extends JpaRepository<Member, Long> {

    Member findByName(String name);
}
