<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-4">
    <div class="d-flex justify-content-between align-items-center mb-5 border-bottom pb-3">
        <div>
            <h1 class="fw-bold mb-1">Admin Dashboard</h1>
            <p class="text-secondary mb-0">Manage gallery inventory, queries, and users.</p>
        </div>
        <a href="${pageContext.request.contextPath}/admin/users/new" class="btn btn-outline-dark rounded-pill">Create User Account <span class="fw-light ms-1 fs-5">+</span></a>
    </div>

    <c:if test="${param.userCreated}">
        <div class="alert alert-success alert-dismissible fade show rounded-3" role="alert">
            New user successfully created!
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </c:if>

    <div class="row g-4">
        <!-- Manage Artworks Card -->
        <div class="col-md-6">
            <div class="panel-card h-100 p-4 border-0 shadow-sm position-relative">
                <div class="d-flex align-items-center mb-3">
                    <div class="bg-light rounded p-3 me-3">
                        <span class="fs-4 text-dark">🖼️</span>
                    </div>
                    <h4 class="fw-bold mb-0">Manage Artworks</h4>
                </div>
                <p class="text-secondary mb-4">Add, update, and remove artworks from the gallery inventory. Organize your collections and artists.</p>
                <a href="${pageContext.request.contextPath}/admin/artworks" class="btn btn-accent rounded-pill stretched-link px-4">Go to Artworks</a>
            </div>
        </div>

        <!-- View Queries Card -->
        <div class="col-md-6">
            <div class="panel-card h-100 p-4 border-0 shadow-sm position-relative">
                <div class="d-flex align-items-center mb-3">
                    <div class="bg-light rounded p-3 me-3">
                        <span class="fs-4 text-dark">💬</span>
                    </div>
                    <h4 class="fw-bold mb-0">Visitor Queries</h4>
                </div>
                <p class="text-secondary mb-4">Read messages, feedback, and upload requests submitted through the query form on the footer.</p>
                <a href="${pageContext.request.contextPath}/admin/queries" class="btn btn-outline-dark rounded-pill stretched-link px-4">View Queries</a>
            </div>
        </div>
    </div>
    <div class="mt-5">
        <h3 class="fw-bold mb-4">Manage Users</h3>
        <div class="panel-card p-4 border-0 shadow-sm">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th class="text-end">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:forEach var="user" items="${users}">
                            <tr>
                                <td class="fw-medium">${user.name}</td>
                                <td>${user.email}</td>
                                <td><span class="badge bg-secondary">${user.role}</span></td>
                                <td>
                                    <c:choose>
                                        <c:when test="${user.blocked}">
                                            <span class="badge bg-danger">Blocked</span>
                                        </c:when>
                                        <c:otherwise>
                                            <span class="badge bg-success">Active</span>
                                        </c:otherwise>
                                    </c:choose>
                                </td>
                                <td class="text-end">
                                    <form action="${pageContext.request.contextPath}/admin/users/${user.id}/toggle-block" method="post" class="d-inline">
                                        <button type="submit" class="btn btn-sm ${user.blocked ? 'btn-success' : 'btn-danger'}" ${user.role == 'ADMIN' ? 'disabled' : ''}>
                                            ${user.blocked ? 'Unblock User' : 'Block User'}
                                        </button>
                                    </form>
                                </td>
                            </tr>
                        </c:forEach>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

