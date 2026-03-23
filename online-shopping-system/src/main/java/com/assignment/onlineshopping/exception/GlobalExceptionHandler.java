package com.assignment.onlineshopping.exception;

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
            body.put("message", exception.getMessage() != null ? exception.getMessage() : "Something went wrong");
            return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
        }
        String message = exception.getMessage();
        if (message == null || message.isBlank()) {
            message = exception.getClass().getSimpleName();
        }
        model.addAttribute("errorMessage", message);
        return "error";
    }
}
