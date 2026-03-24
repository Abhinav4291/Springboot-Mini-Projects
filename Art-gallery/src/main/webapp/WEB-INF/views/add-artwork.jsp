<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<jsp:include page="header.jsp" />

<div class="container py-5 my-4">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
                <h1 class="fw-bold mb-0">Add New Artwork</h1>
                <a href="${pageContext.request.contextPath}/admin/artworks" class="btn btn-outline-dark rounded-pill">Cancel</a>
            </div>

            <div class="panel-card p-5">
                <form action="${pageContext.request.contextPath}/admin/artworks" method="post" enctype="multipart/form-data">
                    <div class="row g-4">
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Title</label>
                            <input class="form-control" name="title" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Category</label>
                            <input class="form-control" name="category" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Price ($)</label>
                            <input class="form-control" name="price" type="number" step="0.01" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Image Upload</label>
                            <input type="file" class="form-control" name="imageFile" accept="image/*" required>
                        </div>
                        <div class="col-12">
                            <label class="form-label fw-bold">Artist's Name</label>
                            <input class="form-control" name="artistName" required>
                            <div class="form-text">Type the artist's name. If they don't exist, they will be created automatically.</div>
                        </div>
                        <div class="col-12">
                            <label class="form-label fw-bold">Description</label>
                            <textarea class="form-control" name="description" rows="5" required></textarea>
                        </div>
                    </div>
                    <div class="mt-4 pt-3 border-top text-end">
                        <button class="btn btn-accent rounded-pill px-5 fs-5 w-100" type="submit">Publish Artwork</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>


