# Spring Boot Hibernate Assignments

This workspace contains 8 separate Maven-based Spring Boot projects.
Each project uses Java 17, Spring Data JPA (Hibernate), MySQL, Thymeleaf, and `application.properties`.

## Common Notes

- Update MySQL username and password in each `application.properties` file if needed.
- Database creation is handled by Hibernate using `spring.jpa.hibernate.ddl-auto=update`.
- Each project runs on a different port so they can be started independently.
- The projects are intentionally simple and suitable for student assignment work.

## Import Into Spring Tool Suite

1. Open Spring Tool Suite.
2. Use `File -> Import -> Existing Maven Projects`.
3. Select this workspace folder: `/Users/abhinav/Documents/workspace-spring-tools-for-eclipse-5.1.1.RELEASE`.
4. Import any project you want to run.
5. Update MySQL credentials if required.
6. Run the main application class as `Spring Boot App`.

## Projects and Sample APIs

### Library Management System
- Path: `library-management-system`
- Port: `8081`
- Sample APIs:
  - `GET /api/library/books`
  - `GET /api/library/authors`
  - `GET /api/library/members`
  - `POST /api/library/books`
  - `POST /api/library/issue?memberId=1&bookId=1`
  - `POST /api/library/return?memberId=1&bookId=1`
  - `GET /api/library/books/by-author/R.K. Narayan`

### Hospital Management System
- Path: `hospital-management-system`
- Port: `8082`
- Sample APIs:
  - `GET /api/hospital/doctors`
  - `GET /api/hospital/patients`
  - `GET /api/hospital/appointments`
  - `POST /api/hospital/doctors`
  - `POST /api/hospital/patients`
  - `POST /api/hospital/appointments?doctorId=1&patientId=1&appointmentDate=2026-03-25&reason=Checkup`

### Online Shopping System
- Path: `online-shopping-system`
- Port: `8083`
- Sample APIs:
  - `GET /api/shopping/customers`
  - `GET /api/shopping/products`
  - `GET /api/shopping/orders`
  - `POST /api/shopping/products`
  - `POST /api/shopping/orders?customerId=1&productIds=1,2`

### College Management System
- Path: `college-management-system`
- Port: `8084`
- Sample APIs:
  - `GET /api/college/students`
  - `GET /api/college/faculty`
  - `GET /api/college/courses`
  - `POST /api/college/students`
  - `POST /api/college/enroll?studentId=1&courseId=1`
  - `POST /api/college/assign-faculty?facultyId=1&courseId=1`

### Movie Booking System
- Path: `movie-booking-system`
- Port: `8085`
- Sample APIs:
  - `GET /api/movies/theaters`
  - `GET /api/movies/list`
  - `GET /api/movies/tickets`
  - `POST /api/movies/book?movieId=1&customerName=Abhinav&seatCount=2`

### Banking System
- Path: `banking-system`
- Port: `8086`
- Sample APIs:
  - `GET /api/banking/customers`
  - `GET /api/banking/accounts`
  - `GET /api/banking/transactions`
  - `POST /api/banking/deposit?accountId=1&amount=5000`
  - `POST /api/banking/withdraw?accountId=1&amount=1000`

### Food Delivery System
- Path: `food-delivery-system`
- Port: `8087`
- Sample APIs:
  - `GET /api/food/users`
  - `GET /api/food/restaurants`
  - `GET /api/food/orders`
  - `POST /api/food/orders?userId=1&restaurantId=1&items=Burger,Fries&totalAmount=250`

### Employee Leave Management
- Path: `employee-leave-management`
- Port: `8088`
- Sample APIs:
  - `GET /api/leave/managers`
  - `GET /api/leave/employees`
  - `GET /api/leave/requests`
  - `POST /api/leave/apply?employeeId=1&fromDate=2026-03-28&toDate=2026-03-30&reason=Personal`
  - `POST /api/leave/update-status?requestId=1&status=APPROVED`
