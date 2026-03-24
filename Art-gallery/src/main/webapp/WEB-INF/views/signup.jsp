<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="panel-card p-5">
                <div class="text-center mb-4">
                    <h2 class="fw-bold" style="color: var(--accent);">Join Art Attack!</h2>
                    <p class="text-secondary">Find your next favorite piece.</p>
                </div>
                
                <c:if test="${not empty error}">
                    <div class="alert alert-danger rounded-3">${error}</div>
                </c:if>

                <form action="${pageContext.request.contextPath}/signup" method="post">
                    <div class="mb-3">
                        <label class="form-label fw-medium">Full Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-medium">Email address</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-4">
                        <label class="form-label fw-medium">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-dark w-100 py-2 fs-5 rounded-pill">Create Account</button>
                </form>

                <p class="text-center mt-4 mb-0 text-secondary">
                    Already have an account? <a href="${pageContext.request.contextPath}/login" class="fw-bold text-dark text-decoration-underline">Log in</a>
                </p>
            </div>
        </div>
    </div>
</div>

<jsp:include page="footer.jsp" />
