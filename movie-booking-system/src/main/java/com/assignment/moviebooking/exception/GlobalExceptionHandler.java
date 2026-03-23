package com.assignment.moviebooking.exception;

import java.util.HashMap;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import jakarta.servlet.http.HttpServletRequest;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public Object handleNotFound(ResourceNotFoundException exception, HttpServletRequest request, Model model) {
        String uri = request.getRequestURI();
        if (uri.startsWith("/api/")) {
            Map<String, String> body = new HashMap<>();
            body.put("message", exception.getMessage());
            return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
        }
        model.addAttribute("errorMessage", exception.getMessage());
        return "error";
    }

    @ExceptionHandler(Exception.class)
    public Object handleGeneral(Exception exception, HttpServletRequest request, Model model) {
        String uri = request.getRequestURI();
        if (uri.startsWith("/api/")) {
            Map<String, String> body = new HashMap<>();
            body.put("message", "Something went wrong");
            return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
        }
        model.addAttribute("errorMessage", "Something went wrong");
        return "error";
    }
}
