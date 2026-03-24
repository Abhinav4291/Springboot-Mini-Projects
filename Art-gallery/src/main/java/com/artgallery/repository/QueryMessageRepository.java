package com.artgallery.repository;

import com.artgallery.entity.QueryMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface QueryMessageRepository extends JpaRepository<QueryMessage, Long> {
    List<QueryMessage> findAllByOrderByCreatedAtDesc();
}
