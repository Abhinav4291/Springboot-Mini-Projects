<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<jsp:include page="header.jsp" />

<!-- Hero Carousel -->
<div id="heroCarousel" class="carousel slide carousel-fade mb-5" data-bs-ride="carousel">
    <div class="carousel-inner" style="height: 50vh; min-height: 400px;">
        <div class="carousel-item active h-100">
            <img src="https://images.unsplash.com/photo-1518998053901-5348d3961a04?auto=format&fit=crop&q=80&w=1920" class="d-block w-100 h-100 object-fit-cover" alt="Art 1">
            <div class="position-absolute top-0 start-0 w-100 h-100 bg-dark bg-opacity-50"></div>
            <div class="carousel-caption d-flex flex-column justify-content-center h-100 align-items-center">
                <h1 class="display-3 fw-bold text-white">Discover Timeless Art</h1>
                <p class="lead text-light">Explore curated collections from brilliant artists.</p>
            </div>
        </div>
        <div class="carousel-item h-100">
            <img src="https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8?auto=format&fit=crop&q=80&w=1920" class="d-block w-100 h-100 object-fit-cover" alt="Art 2">
            <div class="position-absolute top-0 start-0 w-100 h-100 bg-dark bg-opacity-50"></div>
            <div class="carousel-caption d-flex flex-column justify-content-center h-100 align-items-center">
                <h1 class="display-3 fw-bold text-white">Abstract & Modern</h1>
                <p class="lead text-light">Vibrant colors and new perspectives.</p>
            </div>
        </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
    </button>
</div>

<div class="container py-4">
    <c:if test="${param.querySubmitted}">
        <div class="alert alert-success alert-dismissible fade show rounded-pill" role="alert">
            Your query has been submitted successfully!
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </c:if>

    <c:choose>
        <c:when test="${not empty keyword}">
            <h2 class="fw-bold mb-4">Search Results for "<c:out value="${keyword}"/>"</h2>
        </c:when>
        <c:otherwise>
            <h2 class="fw-bold mb-4">Featured Collection</h2>
        </c:otherwise>
    </c:choose>
    
    <c:if test="${empty artworks}">
        <div class="text-center py-5">
            <h4 class="text-secondary">No artworks found.</h4>
            <a href="${pageContext.request.contextPath}/" class="btn btn-outline-dark rounded-pill mt-3">Clear Search</a>
        </div>
    </c:if>

    <div class="row" data-masonry='{"percentPosition": true }'>
        <c:forEach var="artwork" items="${artworks}">
            <div class="col-sm-6 col-lg-4 mb-4">
                <div class="art-card" data-bs-toggle="modal" data-bs-target="#artworkModal${artwork.id}" style="cursor: pointer;">
                    <img src="${artwork.imageUrl}" class="card-img-top" alt="${artwork.title}" style="height: 320px;">
                    <div class="card-body p-3">
                        <h5 class="fw-bold mb-1">${artwork.title}</h5>
                        <p class="text-secondary small mb-2">${artwork.artist.name}</p>
                    </div>
                </div>
            </div>
        </c:forEach>
    </div>

    <!-- Pagination -->
    <c:if test="${totalPages > 1}">
        <nav aria-label="Page navigation" class="mt-5">
            <ul class="pagination justify-content-center">
                <li class="page-item ${currentPage == 0 ? 'disabled' : ''}">
                    <a class="page-link rounded-pill border-0 mx-1 px-4 text-dark bg-light" href="?page=${currentPage - 1}${not empty keyword ? '&keyword='.concat(keyword) : ''}">Prev</a>
                </li>
                <c:forEach begin="0" end="${totalPages - 1}" var="i">
                    <li class="page-item">
                        <a class="page-link rounded-pill border-0 mx-1 px-3 ${currentPage == i ? 'bg-dark text-white' : 'text-dark bg-light'}" 
                           href="?page=${i}${not empty keyword ? '&keyword='.concat(keyword) : ''}">${i + 1}</a>
                    </li>
                </c:forEach>
                <li class="page-item ${currentPage == totalPages - 1 ? 'disabled' : ''}">
                    <a class="page-link rounded-pill border-0 mx-1 px-4 text-dark bg-light" href="?page=${currentPage + 1}${not empty keyword ? '&keyword='.concat(keyword) : ''}">Next</a>
                </li>
            </ul>
        </nav>
    </c:if>

    <!-- Modals for Artwork Details (Outside Masonry Grid) -->
    <c:forEach var="artwork" items="${artworks}">
        <div class="modal fade" id="artworkModal${artwork.id}" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content border-0 rounded-4 overflow-hidden">
                    <sec:authorize access="isAuthenticated()">
                        <div class="row g-0">
                            <div class="col-md-6">
                                <img src="${artwork.imageUrl}" class="img-fluid h-100 object-fit-cover" alt="${artwork.title}" style="min-height: 400px; width: 100%;">
                            </div>
                            <div class="col-md-6 position-relative">
                                <button type="button" class="btn-close position-absolute top-0 end-0 m-3" data-bs-dismiss="modal" aria-label="Close"></button>
                                <div class="p-4 d-flex flex-column h-100">
                                    <h3 class="fw-bold mb-1">${artwork.title}</h3>
                                    <p class="text-secondary mb-3">By ${artwork.artist.name}</p>
                                    <p>${artwork.description}</p>
                                    <span class="badge bg-light text-dark align-self-start border mb-4">${artwork.category}</span>
                                    <div class="mt-auto d-flex justify-content-between align-items-center">
                                        <span class="fs-5 fw-bold">$${artwork.price}</span>
                                        
                                        <!-- Calculate if current user favorited this -->
                                        <c:set var="isFav" value="false"/>
                                        <c:if test="${not empty pageContext.request.userPrincipal}">
                                            <c:forEach var="fav" items="${artwork.favorites}">
                                                <c:if test="${fav.user.email == pageContext.request.userPrincipal.name}">
                                                    <c:set var="isFav" value="true"/>
                                                </c:if>
                                            </c:forEach>
                                        </c:if>

                                        <div class="d-flex flex-column gap-2 align-items-end">
                                            <div class="d-flex align-items-center gap-3">
                                                <form action="${pageContext.request.contextPath}/artworks/${artwork.id}/like" method="post" class="m-0">
                                                    <button type="submit" class="btn btn-outline-danger rounded-pill px-3 d-flex align-items-center gap-2">
                                                        <i class="bi bi-heart-fill"></i> <span class="fw-bold">${artwork.likeCount}</span>
                                                    </button>
                                                </form>
                                            </div>
                                            <form action="${pageContext.request.contextPath}/favorites/toggle/${artwork.id}" method="post" class="m-0">
                                                <button type="submit" class="btn ${isFav ? 'btn-outline-dark' : 'btn-accent'} rounded-pill px-4">
                                                    <i class="bi bi-bookmark-plus me-1"></i> ${isFav ? 'Remove from Fav' : 'Add to Fav'}
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </sec:authorize>
                    <sec:authorize access="!isAuthenticated()">
                        <div class="modal-body text-center p-5">
                            <h4 class="fw-bold mb-3">Sign in required</h4>
                            <p class="text-secondary mb-4">Join our community to view artwork details and add pieces to your favorites collection.</p>
                            <a href="${pageContext.request.contextPath}/login" class="btn btn-accent px-5 py-2">Log in</a>
                        </div>
                    </sec:authorize>
                </div>
            </div>
        </div>
    </c:forEach>
    </div>
</div>

<!-- Add Masonry via CDN for grid layout -->
<script src="https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/dist/masonry.pkgd.min.js"></script>

<jsp:include page="footer.jsp" />
