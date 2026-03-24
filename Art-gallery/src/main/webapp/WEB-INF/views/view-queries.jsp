<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-4">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h1 class="fw-bold mb-1">Visitor Queries</h1>
            <p class="text-secondary mb-0">Messages submitted from the website footer.</p>
        </div>
        <a href="${pageContext.request.contextPath}/admin/dashboard" class="btn btn-outline-dark rounded-pill">Back to Dashboard</a>
    </div>

    <div class="row g-4" data-masonry='{"percentPosition": true }'>
        <c:forEach var="query" items="${queries}">
            <div class="col-sm-6 col-md-4 mb-4">
                <div class="panel-card p-4 h-100 d-flex flex-column border-top border-4 border-accent" style="border-top-color: var(--accent) !important;">
                    <div class="mb-3 border-bottom pb-3">
                        <div class="d-flex justify-content-between align-items-start mb-1">
                            <h5 class="fw-bold mb-0">${query.name}</h5>
                            <span class="badge bg-light text-secondary border fw-normal shadow-sm" style="font-size: 0.75rem;">
                                ${query.createdAt.toLocalDate()}
                            </span>
                        </div>
                        <a href="mailto:${query.email}" class="text-decoration-underline text-secondary small">${query.email}</a>
                    </div>
                    <p class="mb-0 text-dark flex-grow-1" style="font-family: Georgia, serif; line-height: 1.6;">
                        "${query.message}"
                    </p>
                </div>
            </div>
        </c:forEach>
    </div>
    
    <c:if test="${empty queries}">
        <div class="text-center py-5 mt-4">
            <span class="fs-1 d-block mb-3">📬</span>
            <h4 class="fw-bold text-secondary">Inbox empty</h4>
            <p class="text-muted">No visitor queries have been submitted yet.</p>
        </div>
    </c:if>
</div>

<script src="https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/dist/masonry.pkgd.min.js"></script>


