<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
                <h1 class="fw-bold mb-0">Edit Artwork</h1>
                <a href="${pageContext.request.contextPath}/admin/artworks" class="btn btn-outline-dark rounded-pill">Cancel</a>
            </div>

            <div class="panel-card p-5">
                <!-- Preview image -->
                <div class="text-center mb-4">
                    <img src="${artwork.imageUrl}" alt="Preview" class="img-thumbnail rounded-3" style="max-height: 200px; object-fit: contain;">
                </div>

                <form action="${pageContext.request.contextPath}/admin/artworks/${artwork.id}" method="post" enctype="multipart/form-data">
                    <div class="row g-4">
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Title</label>
                            <input class="form-control" name="title" value="${artwork.title}" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Category</label>
                            <input class="form-control" name="category" value="${artwork.category}" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Price ($)</label>
                            <input class="form-control" name="price" type="number" step="0.01" value="${artwork.price}" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Update Image</label>
                            <input type="file" class="form-control" name="imageFile" accept="image/*">
                            <div class="form-text">Leave blank to keep the current image.</div>
                        </div>
                        <div class="col-12">
                            <label class="form-label fw-bold">Artist's Name</label>
                            <input class="form-control" name="artistName" value="${artwork.artist.name}" required>
                            <div class="form-text">Type the artist's name. If they don't exist, they will be created automatically.</div>
                        </div>
                        <div class="col-12">
                            <label class="form-label fw-bold">Description</label>
                            <textarea class="form-control" name="description" rows="5" required>${artwork.description}</textarea>
                        </div>
                    </div>
                    <div class="mt-4 pt-3 border-top text-end">
                        <button class="btn btn-accent rounded-pill px-5 fs-5 w-100" type="submit">Update Details</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>


