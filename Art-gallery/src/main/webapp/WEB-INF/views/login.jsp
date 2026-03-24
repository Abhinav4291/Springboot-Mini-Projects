<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="panel-card p-5">
                <div class="text-center mb-4">
                    <h2 class="fw-bold" style="color: var(--accent);">Welcome back</h2>
                    <p class="text-secondary">Sign in to discover premium art.</p>
                </div>
                
                <c:if test="${not empty error}">
                    <div class="alert alert-danger rounded-3">${error}</div>
                </c:if>
                <c:if test="${not empty message}">
                    <div class="alert alert-success rounded-3">${message}</div>
                </c:if>

                <form action="${pageContext.request.contextPath}/login-process" method="post">
                    <div class="mb-3">
                        <label class="form-label fw-medium">Email address</label>
                        <input type="email" name="username" class="form-control" required autofocus>
                    </div>
                    <div class="mb-4">
                        <label class="form-label fw-medium">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-accent w-100 py-2 fs-5">Log in</button>
                </form>

                <p class="text-center mt-4 mb-0 text-secondary">
                    Not a member yet? <a href="${pageContext.request.contextPath}/signup" class="fw-bold text-dark text-decoration-underline">Sign up</a>
                </p>
            </div>
        </div>
    </div>
</div>

<jsp:include page="footer.jsp" />
