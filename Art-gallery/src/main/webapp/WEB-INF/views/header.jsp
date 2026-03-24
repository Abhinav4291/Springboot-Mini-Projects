<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Art Attack!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <style>
        :root {
            --bg: #f9f9f9;
            --text: #111111;
            --accent: #E60023;
            --panel: #ffffff;
            --line: #efefef;
        }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        main { flex: 1; }
        .gallery-nav {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--line);
        }
        .brand-mark {
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--accent) !important;
        }
        .nav-link { font-weight: 500; color: var(--text) !important; }
        .nav-link:hover { color: var(--accent) !important; }
        .btn-accent {
            background-color: var(--accent);
            color: white;
            border-radius: 24px;
            font-weight: 600;
            border: none;
            padding: 0.375rem 1rem;
        }
        .btn-accent:hover { background-color: #ad081b; color: white; }
        
        /* Pinterest-style Cards */
        .art-card, .panel-card {
            background: var(--panel);
            border: none;
            border-radius: 16px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }
        .art-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        }
        .card-img-top {
            object-fit: cover;
            width: 100%;
        }
        .form-control, .form-select {
            background: #f0f0f0;
            border: 1px solid transparent;
            border-radius: 12px;
            padding: 0.75rem 1rem;
        }
        .form-control:focus, .form-select:focus {
            background: #ffffff;
            border-color: var(--accent);
            box-shadow: 0 0 0 4px rgba(230, 0, 35, 0.15);
        }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light gallery-nav sticky-top py-3">
    <div class="container">
        <a class="navbar-brand brand-mark fw-bold" style="letter-spacing: 1px;" href="${pageContext.request.contextPath}/">ART ATTACK!</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="nav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/favorites">Favorites</a></li>
                <sec:authorize access="hasRole('ADMIN')">
                    <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/admin/dashboard">Admin Dashboard</a></li>
                </sec:authorize>
            </ul>
            <form action="${pageContext.request.contextPath}/" method="get" class="d-flex mx-lg-4 my-2 my-lg-0 w-100" style="max-width: 400px;">
                <input class="form-control rounded-pill border-0 px-4" style="background:#f0f0f0;" type="search" name="keyword" placeholder="Search artworks, artists..." value="${keyword}">
            </form>
            <div class="d-flex align-items-center gap-3">
                <sec:authorize access="isAuthenticated()">
                    <span class="text-secondary fw-medium"><sec:authentication property="name"/></span>
                    <form action="${pageContext.request.contextPath}/logout" method="post" class="m-0">
                        <button class="btn btn-outline-dark rounded-pill fw-medium" type="submit">Logout</button>
                    </form>
                </sec:authorize>
                <sec:authorize access="!isAuthenticated()">
                    <a href="${pageContext.request.contextPath}/login" class="btn btn-outline-dark rounded-pill fw-medium">Login</a>
                    <a href="${pageContext.request.contextPath}/signup" class="btn btn-accent">Sign Up</a>
                </sec:authorize>
            </div>
        </div>
    </div>
</nav>
<main>
