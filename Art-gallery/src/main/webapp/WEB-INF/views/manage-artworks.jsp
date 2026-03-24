<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-4">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <div>
            <h1 class="fw-bold mb-1">Manage Artworks</h1>
            <p class="text-secondary mb-0">Update gallery inventory, items count: ${artworks.size()}</p>
        </div>
        <div>
            <a href="${pageContext.request.contextPath}/admin/dashboard" class="btn btn-outline-dark rounded-pill me-2">Back</a>
            <a href="${pageContext.request.contextPath}/admin/artworks/new" class="btn btn-accent rounded-pill">Add Artwork <span class="fw-light ms-1 fs-5">+</span></a>
        </div>
    </div>

    <div class="bg-white rounded-4 shadow-sm overflow-hidden mb-5">
        <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
                <tr>
                    <th class="ps-4 py-3 fw-medium text-secondary">Title</th>
                    <th class="py-3 fw-medium text-secondary">Artist</th>
                    <th class="py-3 fw-medium text-secondary">Category</th>
                    <th class="py-3 fw-medium text-secondary">Price</th>
                    <th class="text-end pe-4 py-3 fw-medium text-secondary">Actions</th>
                </tr>
            </thead>
            <tbody>
                <c:if test="${empty artworks}">
                    <tr>
                        <td colspan="5" class="text-center text-secondary py-5">
                            <span class="fs-1 d-block mb-3">📭</span>
                            No artworks found. Create one above!
                        </td>
                    </tr>
                </c:if>
                <c:forEach var="artwork" items="${artworks}">
                    <tr>
                        <td class="ps-4 py-3 fw-medium">${artwork.title}</td>
                        <td class="py-3">${artwork.artist.name}</td>
                        <td class="py-3"><span class="badge bg-light text-dark border">${artwork.category}</span></td>
                        <td class="py-3 fw-medium">$${artwork.price}</td>
                        <td class="text-end pe-4 py-3">
                            <div class="d-flex justify-content-end gap-2">
                                <a href="${pageContext.request.contextPath}/admin/artworks/${artwork.id}/edit" class="btn btn-sm btn-outline-dark rounded-pill px-3">Edit</a>
                                <form action="${pageContext.request.contextPath}/admin/artworks/${artwork.id}/delete" method="post" onsubmit="return confirm('Are you sure you want to delete this artwork?');">
                                    <button class="btn btn-sm btn-outline-danger rounded-pill px-3" type="submit">Delete</button>
                                </form>
                            </div>
                        </td>
                    </tr>
                </c:forEach>
            </tbody>
        </table>
    </div>
</div>


