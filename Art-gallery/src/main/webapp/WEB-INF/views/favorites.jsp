<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-5 border-bottom pb-3">
        <h1 class="fw-bold mb-0">Saved Favorites</h1>
        <span class="badge bg-dark rounded-pill px-3 py-2">${artworks.size()} pieces</span>
    </div>

    <div class="row" data-masonry='{"percentPosition": true }'>
        <c:forEach var="artwork" items="${artworks}">
            <div class="col-sm-6 col-lg-3 mb-4">
                <div class="art-card p-3 position-relative">
                    <img src="${artwork.imageUrl}" class="w-100 rounded-3 object-fit-cover mb-3" alt="${artwork.title}" style="height: 240px;">
                    <h6 class="fw-bold mb-1">${artwork.title}</h6>
                    <p class="text-secondary small mb-3">${artwork.artist.name}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="fw-bold">$${artwork.price}</span>
                        <form action="${pageContext.request.contextPath}/favorites/toggle/${artwork.id}" method="post">
                            <button type="submit" class="btn btn-sm btn-outline-danger rounded-pill">Remove</button>
                        </form>
                    </div>
                </div>
            </div>
        </c:forEach>
    </div>

    <c:if test="${empty artworks}">
        <div class="text-center py-5 mt-5">
            <h3 class="fw-bold text-secondary">No favorites yet!</h3>
            <p class="text-muted">Explore the collection and heart the pieces you love.</p>
            <a href="${pageContext.request.contextPath}/" class="btn btn-dark rounded-pill px-4 mt-3">Discover Art</a>
        </div>
    </c:if>
</div>

<script src="https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/dist/masonry.pkgd.min.js"></script>

<jsp:include page="footer.jsp" />
