package com.artgallery.controller;

import com.artgallery.service.QueryService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class QueryController {

    private final QueryService queryService;

    public QueryController(QueryService queryService) {
        this.queryService = queryService;
    }

    @PostMapping("/query")
    public String submitQuery(@RequestParam String name, @RequestParam String email, @RequestParam String message) {
        queryService.save(name, email, message);
        return "redirect:/?querySubmitted=true";
    }
}
