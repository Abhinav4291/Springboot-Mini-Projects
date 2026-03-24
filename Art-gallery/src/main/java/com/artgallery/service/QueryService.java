package com.artgallery.service;

import com.artgallery.entity.QueryMessage;
import com.artgallery.repository.QueryMessageRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class QueryService {

    private final QueryMessageRepository repository;

    public QueryService(QueryMessageRepository repository) {
        this.repository = repository;
    }

    public void save(String name, String email, String message) {
        QueryMessage q = new QueryMessage();
        q.setName(name);
        q.setEmail(email);
        q.setMessage(message);
        repository.save(q);
    }

    public List<QueryMessage> findAll() {
        return repository.findAllByOrderByCreatedAtDesc();
    }
}
