<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
                <h1 class="fw-bold mb-0">Create User</h1>
                <a href="${pageContext.request.contextPath}/admin/dashboard" class="btn btn-outline-dark rounded-pill btn-sm px-3">Back</a>
            </div>

            <div class="panel-card p-4">
                <p class="text-secondary mb-4">Create a new user or admin account directly into the database.</p>
                
                <c:if test="${not empty error}">
                    <div class="alert alert-danger rounded-3">${error}</div>
                </c:if>

                <form action="${pageContext.request.contextPath}/admin/users" method="post">
                    <div class="mb-3">
                        <label class="form-label fw-medium">Full Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-medium">Email address</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-medium">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <div class="mb-4">
                        <label class="form-label fw-medium">Role</label>
                        <select name="role" class="form-select" required>
                            <option value="USER">User (Standard)</option>
                            <option value="ADMIN">Administrator</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-dark w-100 rounded-pill py-2">Create Account</button>
                </form>
            </div>
        </div>
    </div>
</div>


