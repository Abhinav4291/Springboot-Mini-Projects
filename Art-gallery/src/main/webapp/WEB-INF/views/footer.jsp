</main>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<footer class="bg-white border-top py-5 mt-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-md-6 mb-4 mb-md-0">
                <c:choose>
                    <c:when test="${not empty pageContext.request.userPrincipal}">
                        <h4 class="fw-bold mb-3">Get in Touch</h4>
                        <p class="text-secondary">To upload your image on the site mail to: <a href="mailto:art@gmail.com" class="fw-medium text-dark">art@gmail.com</a> with your image name and a description.</p>
                    </c:when>
                    <c:otherwise>
                        <h4 class="fw-bold text-secondary mb-3">Art Attack!</h4>
                        <p class="text-secondary">Join our community to access exclusive contact information, send customized art, and more.</p>
                    </c:otherwise>
                </c:choose>
                <p class="text-secondary small mt-4">&copy; 2026 Art Attack! Platform. All rights reserved.</p>
            </div>
            <div class="col-md-6">
                <div class="panel-card p-4 m-0 shadow-sm border-0">
                    <h5 class="fw-bold mb-3">Send a Query</h5>
                    <form action="${pageContext.request.contextPath}/query" method="post" ${empty pageContext.request.userPrincipal ? 'onsubmit="return false;"' : ''}>
                        <div class="mb-3">
                            <input type="text" name="name" class="form-control" required onfocus="checkAuth(this)">
                        </div>
                        <div class="mb-3">
                            <input type="email" name="email" class="form-control" required onfocus="checkAuth(this)">
                        </div>
                        <div class="mb-3">
                            <textarea name="message" class="form-control" rows="3" required onfocus="checkAuth(this)"></textarea>
                        </div>
                        <button type="submit" class="btn btn-dark w-100 rounded-pill fw-medium" onclick="checkAuth(this)">Submit Query</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</footer>

<script>
function checkAuth(element) {
    <c:if test="${empty pageContext.request.userPrincipal}">
        if(element) element.blur();
        alert("Please login first to send a query.");
        window.location.href = "${pageContext.request.contextPath}/login";
    </c:if>
}
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
