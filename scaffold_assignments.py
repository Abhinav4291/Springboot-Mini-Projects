from pathlib import Path
from textwrap import dedent


ROOT = Path("/Users/abhinav/Documents/workspace-spring-tools-for-eclipse-5.1.1.RELEASE")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def entity_fields(fields):
    lines = []
    for field in fields:
        if field["type"].startswith("List<"):
            lines.append("    @JsonIgnore")
        if field.get("annotation"):
            lines.append(field["annotation"])
        if field["type"].startswith("List<"):
            lines.append(f"    private {field['type']} {field['name']} = new ArrayList<>();")
        else:
            lines.append(f"    private {field['type']} {field['name']};")
        lines.append("")
    return "\n".join(lines).rstrip()


def getter_setters(class_name, fields):
    parts = []
    for field in fields:
        field_name = field["name"]
        method = field_name[0].upper() + field_name[1:]
        if field["type"] == "boolean":
            parts.append(
                f"""    public boolean is{method}() {{
        return {field_name};
    }}

    public void set{method}(boolean {field_name}) {{
        this.{field_name} = {field_name};
    }}"""
            )
        else:
            parts.append(
                f"""    public {field["type"]} get{method}() {{
        return {field_name};
    }}

    public void set{method}({field["type"]} {field_name}) {{
        this.{field_name} = {field_name};
    }}"""
            )
    return "\n\n".join(parts)


def entity_code(package_name, class_name, fields):
    used = ["import jakarta.persistence.*;"]
    if any("List<" in field["type"] for field in fields):
        used.extend(
            [
                "import com.fasterxml.jackson.annotation.JsonIgnore;",
                "import java.util.ArrayList;",
                "import java.util.List;",
            ]
        )
    if any("LocalDateTime" in field["type"] for field in fields):
        used.append("import java.time.LocalDateTime;")
    if any("LocalDate" in field["type"] for field in fields):
        used.append("import java.time.LocalDate;")
    import_block = "\n".join(dict.fromkeys(used))
    return dedent(
        f"""
        package {package_name}.entity;

        {import_block}

        @Entity
        public class {class_name} {{

        {entity_fields(fields)}

            public {class_name}() {{
            }}

        {getter_setters(class_name, fields)}
        }}
        """
    )


PROJECTS = [
    {
        "name": "library-management-system",
        "artifact": "library-management-system",
        "package": "com.assignment.librarymanagement",
        "class": "LibraryManagementSystemApplication",
        "title": "Library Management System",
        "port": 8081,
        "db": "library_management_db",
        "service": "LibraryService",
        "entities": {
            "Author": [
                {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                {"type": "String", "name": "name"},
                {"type": "String", "name": "email"},
                {"annotation": "@ManyToMany(mappedBy = \"authors\")", "type": "List<Book>", "name": "books"},
            ],
            "Book": [
                {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                {"type": "String", "name": "title"},
                {"type": "String", "name": "isbn"},
                {"type": "boolean", "name": "issued"},
                {"annotation": "@ManyToMany\n    @JoinTable(name = \"book_author\", joinColumns = @JoinColumn(name = \"book_id\"), inverseJoinColumns = @JoinColumn(name = \"author_id\"))", "type": "List<Author>", "name": "authors"},
                {"annotation": "@ManyToMany(mappedBy = \"issuedBooks\")", "type": "List<Member>", "name": "members"},
            ],
            "Member": [
                {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                {"type": "String", "name": "name"},
                {"type": "String", "name": "phoneNumber"},
                {"annotation": "@ManyToMany\n    @JoinTable(name = \"member_book\", joinColumns = @JoinColumn(name = \"member_id\"), inverseJoinColumns = @JoinColumn(name = \"book_id\"))", "type": "List<Book>", "name": "issuedBooks"},
            ],
        },
        "repositories": {
            "AuthorRepository": "Author findByName(String name);\n\n    List<Author> findByNameContainingIgnoreCase(String name);",
            "BookRepository": "List<Book> findByTitleContainingIgnoreCase(String title);",
            "MemberRepository": "Member findByName(String name);",
        },
        "service_code": """
            package com.assignment.librarymanagement.service;

            import java.util.List;

            import org.springframework.stereotype.Service;
            import org.springframework.transaction.annotation.Transactional;

            import com.assignment.librarymanagement.entity.Author;
            import com.assignment.librarymanagement.entity.Book;
            import com.assignment.librarymanagement.entity.Member;
            import com.assignment.librarymanagement.exception.ResourceNotFoundException;
            import com.assignment.librarymanagement.repository.AuthorRepository;
            import com.assignment.librarymanagement.repository.BookRepository;
            import com.assignment.librarymanagement.repository.MemberRepository;

            @Service
            public class LibraryService {

                private final BookRepository bookRepository;
                private final AuthorRepository authorRepository;
                private final MemberRepository memberRepository;

                public LibraryService(BookRepository bookRepository, AuthorRepository authorRepository, MemberRepository memberRepository) {
                    this.bookRepository = bookRepository;
                    this.authorRepository = authorRepository;
                    this.memberRepository = memberRepository;
                }

                public List<Book> getAllBooks() {
                    return bookRepository.findAll();
                }

                public List<Author> getAllAuthors() {
                    return authorRepository.findAll();
                }

                public List<Member> getAllMembers() {
                    return memberRepository.findAll();
                }

                public Book saveBook(Book book) {
                    if (book.getAuthors() == null) {
                        book.setAuthors(new java.util.ArrayList<>());
                    }
                    if (book.getMembers() == null) {
                        book.setMembers(new java.util.ArrayList<>());
                    }
                    return bookRepository.save(book);
                }

                public Author saveAuthor(Author author) {
                    if (author.getBooks() == null) {
                        author.setBooks(new java.util.ArrayList<>());
                    }
                    return authorRepository.save(author);
                }

                public Member saveMember(Member member) {
                    if (member.getIssuedBooks() == null) {
                        member.setIssuedBooks(new java.util.ArrayList<>());
                    }
                    return memberRepository.save(member);
                }

                @Transactional
                public void issueBook(Long memberId, Long bookId) {
                    Member member = memberRepository.findById(memberId)
                            .orElseThrow(() -> new ResourceNotFoundException("Member not found"));
                    Book book = bookRepository.findById(bookId)
                            .orElseThrow(() -> new ResourceNotFoundException("Book not found"));
                    boolean alreadyIssuedToMember = member.getIssuedBooks().stream()
                            .anyMatch(existingBook -> existingBook.getId().equals(bookId));
                    if (!alreadyIssuedToMember) {
                        member.getIssuedBooks().add(book);
                    }
                    book.setIssued(true);
                    memberRepository.save(member);
                    bookRepository.save(book);
                }

                @Transactional
                public void returnBook(Long memberId, Long bookId) {
                    Member member = memberRepository.findById(memberId)
                            .orElseThrow(() -> new ResourceNotFoundException("Member not found"));
                    Book book = bookRepository.findById(bookId)
                            .orElseThrow(() -> new ResourceNotFoundException("Book not found"));
                    member.getIssuedBooks().removeIf(existingBook -> existingBook.getId().equals(bookId));
                    boolean stillIssued = memberRepository.findAll().stream()
                            .anyMatch(existingMember -> existingMember.getIssuedBooks().stream()
                                    .anyMatch(existingBook -> existingBook.getId().equals(bookId) && !existingMember.getId().equals(memberId)));
                    if (!stillIssued) {
                        book.setIssued(false);
                    }
                    memberRepository.save(member);
                    bookRepository.save(book);
                }

                public List<Book> getBooksByAuthor(String authorName) {
                    Author author = authorRepository.findByName(authorName);
                    if (author == null) {
                        throw new ResourceNotFoundException("Author not found");
                    }
                    return author.getBooks();
                }
            }
        """,
        "rest_controller": """
            package com.assignment.librarymanagement.controller;

            import java.util.List;

            import org.springframework.http.ResponseEntity;
            import org.springframework.web.bind.annotation.GetMapping;
            import org.springframework.web.bind.annotation.PathVariable;
            import org.springframework.web.bind.annotation.PostMapping;
            import org.springframework.web.bind.annotation.RequestBody;
            import org.springframework.web.bind.annotation.RequestMapping;
            import org.springframework.web.bind.annotation.RequestParam;
            import org.springframework.web.bind.annotation.RestController;

            import com.assignment.librarymanagement.entity.Author;
            import com.assignment.librarymanagement.entity.Book;
            import com.assignment.librarymanagement.entity.Member;
            import com.assignment.librarymanagement.service.LibraryService;

            @RestController
            @RequestMapping("/api/library")
            public class LibraryRestController {

                private final LibraryService libraryService;

                public LibraryRestController(LibraryService libraryService) {
                    this.libraryService = libraryService;
                }

                @GetMapping("/books")
                public List<Book> getBooks() {
                    return libraryService.getAllBooks();
                }

                @GetMapping("/authors")
                public List<Author> getAuthors() {
                    return libraryService.getAllAuthors();
                }

                @GetMapping("/members")
                public List<Member> getMembers() {
                    return libraryService.getAllMembers();
                }

                @PostMapping("/books")
                public Book addBook(@RequestBody Book book) {
                    return libraryService.saveBook(book);
                }

                @PostMapping("/authors")
                public Author addAuthor(@RequestBody Author author) {
                    return libraryService.saveAuthor(author);
                }

                @PostMapping("/members")
                public Member addMember(@RequestBody Member member) {
                    return libraryService.saveMember(member);
                }

                @PostMapping("/issue")
                public ResponseEntity<String> issueBook(@RequestParam Long memberId, @RequestParam Long bookId) {
                    libraryService.issueBook(memberId, bookId);
                    return ResponseEntity.ok("Book issued successfully");
                }

                @PostMapping("/return")
                public ResponseEntity<String> returnBook(@RequestParam Long memberId, @RequestParam Long bookId) {
                    libraryService.returnBook(memberId, bookId);
                    return ResponseEntity.ok("Book returned successfully");
                }

                @GetMapping("/books/by-author/{authorName}")
                public List<Book> getBooksByAuthor(@PathVariable String authorName) {
                    return libraryService.getBooksByAuthor(authorName);
                }
            }
        """,
        "web_controller": """
            package com.assignment.librarymanagement.controller;

            import org.springframework.stereotype.Controller;
            import org.springframework.ui.Model;
            import org.springframework.web.bind.annotation.GetMapping;
            import org.springframework.web.bind.annotation.PostMapping;
            import org.springframework.web.bind.annotation.RequestParam;

            import com.assignment.librarymanagement.entity.Author;
            import com.assignment.librarymanagement.entity.Book;
            import com.assignment.librarymanagement.entity.Member;
            import com.assignment.librarymanagement.service.LibraryService;

            @Controller
            public class LibraryViewController {

                private final LibraryService libraryService;

                public LibraryViewController(LibraryService libraryService) {
                    this.libraryService = libraryService;
                }

                @GetMapping("/")
                public String home(Model model) {
                    model.addAttribute("books", libraryService.getAllBooks());
                    model.addAttribute("authors", libraryService.getAllAuthors());
                    model.addAttribute("members", libraryService.getAllMembers());
                    model.addAttribute("book", new Book());
                    model.addAttribute("author", new Author());
                    model.addAttribute("member", new Member());
                    return "index";
                }

                @PostMapping("/authors/save")
                public String saveAuthor(Author author) {
                    libraryService.saveAuthor(author);
                    return "redirect:/";
                }

                @PostMapping("/books/save")
                public String saveBook(Book book) {
                    libraryService.saveBook(book);
                    return "redirect:/";
                }

                @PostMapping("/members/save")
                public String saveMember(Member member) {
                    libraryService.saveMember(member);
                    return "redirect:/";
                }

                @PostMapping("/issue-book")
                public String issueBook(@RequestParam Long memberId, @RequestParam Long bookId) {
                    libraryService.issueBook(memberId, bookId);
                    return "redirect:/";
                }

                @PostMapping("/return-book")
                public String returnBook(@RequestParam Long memberId, @RequestParam Long bookId) {
                    libraryService.returnBook(memberId, bookId);
                    return "redirect:/";
                }
            }
        """,
        "data_loader": """
            package com.assignment.librarymanagement.config;

            import java.util.ArrayList;

            import org.springframework.boot.CommandLineRunner;
            import org.springframework.context.annotation.Bean;
            import org.springframework.context.annotation.Configuration;

            import com.assignment.librarymanagement.entity.Author;
            import com.assignment.librarymanagement.entity.Book;
            import com.assignment.librarymanagement.entity.Member;
            import com.assignment.librarymanagement.repository.AuthorRepository;
            import com.assignment.librarymanagement.repository.BookRepository;
            import com.assignment.librarymanagement.repository.MemberRepository;

            @Configuration
            public class DataLoader {

                @Bean
                CommandLineRunner loadLibraryData(AuthorRepository authorRepository, BookRepository bookRepository,
                        MemberRepository memberRepository) {
                    return args -> {
                        if (authorRepository.count() == 0) {
                            Author author1 = new Author();
                            author1.setName("R.K. Narayan");
                            author1.setEmail("narayan@example.com");
                            author1.setBooks(new ArrayList<>());

                            Author author2 = new Author();
                            author2.setName("Chetan Bhagat");
                            author2.setEmail("chetan@example.com");
                            author2.setBooks(new ArrayList<>());

                            Book book1 = new Book();
                            book1.setTitle("Malgudi Days");
                            book1.setIsbn("LIB-101");
                            book1.setIssued(false);
                            book1.setAuthors(new ArrayList<>());
                            book1.setMembers(new ArrayList<>());

                            Book book2 = new Book();
                            book2.setTitle("Five Point Someone");
                            book2.setIsbn("LIB-102");
                            book2.setIssued(false);
                            book2.setAuthors(new ArrayList<>());
                            book2.setMembers(new ArrayList<>());

                            author1.getBooks().add(book1);
                            author2.getBooks().add(book2);
                            book1.getAuthors().add(author1);
                            book2.getAuthors().add(author2);

                            authorRepository.save(author1);
                            authorRepository.save(author2);
                            bookRepository.save(book1);
                            bookRepository.save(book2);

                            Member member = new Member();
                            member.setName("Abhinav");
                            member.setPhoneNumber("9123456789");
                            member.setIssuedBooks(new ArrayList<>());
                            memberRepository.save(member);
                        }
                    };
                }
            }
        """,
        "template": """
            <!DOCTYPE html>
            <html lang="en" xmlns:th="http://www.thymeleaf.org">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Library Management System</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="bg-light">
            <div class="container py-4">
                <h1 class="mb-4">Library Management System</h1>
                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5>Add Author</h5>
                                <form action="/authors/save" method="post">
                                    <input class="form-control mb-2" name="name" placeholder="Author name" required>
                                    <input class="form-control mb-2" name="email" placeholder="Email" required>
                                    <button class="btn btn-primary w-100">Save Author</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5>Add Book</h5>
                                <form action="/books/save" method="post">
                                    <input class="form-control mb-2" name="title" placeholder="Book title" required>
                                    <input class="form-control mb-2" name="isbn" placeholder="ISBN" required>
                                    <button class="btn btn-primary w-100">Save Book</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5>Add Member</h5>
                                <form action="/members/save" method="post">
                                    <input class="form-control mb-2" name="name" placeholder="Member name" required>
                                    <input class="form-control mb-2" name="phoneNumber" placeholder="Phone number" required>
                                    <button class="btn btn-primary w-100">Save Member</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row g-4 mt-1">
                    <div class="col-md-6">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5>Issue Book</h5>
                                <form action="/issue-book" method="post" class="row g-2">
                                    <div class="col-6">
                                        <select class="form-select" name="memberId" required>
                                            <option value="">Select member</option>
                                            <option th:each="member : ${members}" th:value="${member.id}" th:text="${member.name}"></option>
                                        </select>
                                    </div>
                                    <div class="col-6">
                                        <select class="form-select" name="bookId" required>
                                            <option value="">Select book</option>
                                            <option th:each="book : ${books}" th:value="${book.id}" th:text="${book.title}"></option>
                                        </select>
                                    </div>
                                    <div class="col-12">
                                        <button class="btn btn-success w-100">Issue Book</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5>Return Book</h5>
                                <form action="/return-book" method="post" class="row g-2">
                                    <div class="col-6">
                                        <select class="form-select" name="memberId" required>
                                            <option value="">Select member</option>
                                            <option th:each="member : ${members}" th:value="${member.id}" th:text="${member.name}"></option>
                                        </select>
                                    </div>
                                    <div class="col-6">
                                        <select class="form-select" name="bookId" required>
                                            <option value="">Select book</option>
                                            <option th:each="book : ${books}" th:value="${book.id}" th:text="${book.title}"></option>
                                        </select>
                                    </div>
                                    <div class="col-12">
                                        <button class="btn btn-outline-secondary w-100">Return Book</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card shadow-sm mt-4">
                    <div class="card-body">
                        <h5>Book List</h5>
                        <table class="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>Title</th>
                                    <th>ISBN</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr th:each="book : ${books}">
                                    <td th:text="${book.title}"></td>
                                    <td th:text="${book.isbn}"></td>
                                    <td th:text="${book.issued ? 'Issued' : 'Available'}"></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            </body>
            </html>
        """,
        "readme_api": [
            "GET /api/library/books",
            "GET /api/library/authors",
            "GET /api/library/members",
            "POST /api/library/books",
            "POST /api/library/issue?memberId=1&bookId=1",
            "POST /api/library/return?memberId=1&bookId=1",
            "GET /api/library/books/by-author/R.K. Narayan",
        ],
    },
]


COMMON_POM = """
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>3.5.11</version>
            <relativePath/>
        </parent>
        <groupId>{package}</groupId>
        <artifactId>{artifact}</artifactId>
        <version>0.0.1-SNAPSHOT</version>
        <name>{artifact}</name>
        <description>{title}</description>
        <properties>
            <java.version>17</java.version>
        </properties>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-data-jpa</artifactId>
            </dependency>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-thymeleaf</artifactId>
            </dependency>
            <dependency>
                <groupId>com.mysql</groupId>
                <artifactId>mysql-connector-j</artifactId>
                <scope>runtime</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-test</artifactId>
                <scope>test</scope>
            </dependency>
        </dependencies>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                </plugin>
            </plugins>
        </build>
    </project>
"""


COMMON_PROPERTIES = """
    spring.application.name={name}
    server.port={port}

    spring.datasource.url=jdbc:mysql://localhost:3306/{db}?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
    spring.datasource.username=root
    spring.datasource.password=root

    spring.jpa.hibernate.ddl-auto=update
    spring.jpa.show-sql=true
    spring.jpa.properties.hibernate.format_sql=true
    spring.jpa.open-in-view=false

    spring.thymeleaf.cache=false
"""


APP_CLASS = """
    package {package};

    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;

    @SpringBootApplication
    public class {class_name} {{

        public static void main(String[] args) {{
            SpringApplication.run({class_name}.class, args);
        }}
    }}
"""


RESOURCE_NOT_FOUND = """
    package {package}.exception;

    public class ResourceNotFoundException extends RuntimeException {{

        public ResourceNotFoundException(String message) {{
            super(message);
        }}
    }}
"""


GLOBAL_HANDLER = """
    package {package}.exception;

    import java.util.HashMap;
    import java.util.Map;

    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.ui.Model;
    import org.springframework.web.bind.annotation.ControllerAdvice;
    import org.springframework.web.bind.annotation.ExceptionHandler;

    import jakarta.servlet.http.HttpServletRequest;

    @ControllerAdvice
    public class GlobalExceptionHandler {{

        @ExceptionHandler(ResourceNotFoundException.class)
        public Object handleNotFound(ResourceNotFoundException exception, HttpServletRequest request, Model model) {{
            String uri = request.getRequestURI();
            if (uri.startsWith("/api/")) {{
                Map<String, String> body = new HashMap<>();
                body.put("message", exception.getMessage());
                return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
            }}
            model.addAttribute("errorMessage", exception.getMessage());
            return "error";
        }}

        @ExceptionHandler(Exception.class)
        public Object handleGeneral(Exception exception, HttpServletRequest request, Model model) {{
            String uri = request.getRequestURI();
            if (uri.startsWith("/api/")) {{
                Map<String, String> body = new HashMap<>();
                body.put("message", "Something went wrong");
                return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
            }}
            model.addAttribute("errorMessage", "Something went wrong");
            return "error";
        }}
    }}
"""


ERROR_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Error</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    <div class="container py-5">
        <div class="card shadow-sm mx-auto" style="max-width: 500px;">
            <div class="card-body text-center">
                <h3 class="mb-3">Request Failed</h3>
                <p class="text-muted" th:text="${errorMessage}">Something went wrong</p>
                <a href="/" class="btn btn-primary">Back to Home</a>
            </div>
        </div>
    </div>
    </body>
    </html>
"""


README_HEADER = """
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
"""


def add_remaining_projects():
    PROJECTS.extend(
        [
            {
                "name": "hospital-management-system",
                "artifact": "hospital-management-system",
                "package": "com.assignment.hospitalmanagement",
                "class": "HospitalManagementSystemApplication",
                "title": "Hospital Management System",
                "port": 8082,
                "db": "hospital_management_db",
                "service": "HospitalService",
                "entities": {
                    "Doctor": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "specialization"},
                        {"annotation": "@OneToMany(mappedBy = \"doctor\", cascade = CascadeType.ALL)", "type": "List<Appointment>", "name": "appointments"},
                    ],
                    "Patient": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "int", "name": "age"},
                        {"annotation": "@OneToMany(mappedBy = \"patient\", cascade = CascadeType.ALL)", "type": "List<Appointment>", "name": "appointments"},
                    ],
                    "Appointment": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "LocalDate", "name": "appointmentDate"},
                        {"type": "String", "name": "reason"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"doctor_id\")", "type": "Doctor", "name": "doctor"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"patient_id\")", "type": "Patient", "name": "patient"},
                    ],
                },
                "repositories": {
                    "DoctorRepository": "",
                    "PatientRepository": "",
                    "AppointmentRepository": "List<Appointment> findByDoctorId(Long doctorId);",
                },
                "service_code": hospital_service(),
                "rest_controller": hospital_rest(),
                "web_controller": hospital_web(),
                "data_loader": hospital_loader(),
                "template": hospital_template(),
                "readme_api": [
                    "GET /api/hospital/doctors",
                    "GET /api/hospital/patients",
                    "GET /api/hospital/appointments",
                    "POST /api/hospital/doctors",
                    "POST /api/hospital/patients",
                    "POST /api/hospital/appointments?doctorId=1&patientId=1&appointmentDate=2026-03-25&reason=Checkup",
                ],
            },
            {
                "name": "online-shopping-system",
                "artifact": "online-shopping-system",
                "package": "com.assignment.onlineshopping",
                "class": "OnlineShoppingSystemApplication",
                "title": "Online Shopping System",
                "port": 8083,
                "db": "online_shopping_db",
                "service": "ShoppingService",
                "entities": {
                    "Customer": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "email"},
                        {"annotation": "@OneToMany(mappedBy = \"customer\", cascade = CascadeType.ALL)", "type": "List<CustomerOrder>", "name": "orders"},
                    ],
                    "Product": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "double", "name": "price"},
                        {"type": "int", "name": "stock"},
                        {"annotation": "@ManyToMany(mappedBy = \"products\")", "type": "List<CustomerOrder>", "name": "orders"},
                    ],
                    "CustomerOrder": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "LocalDate", "name": "orderDate"},
                        {"type": "double", "name": "totalAmount"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"customer_id\")", "type": "Customer", "name": "customer"},
                        {"annotation": "@ManyToMany\n    @JoinTable(name = \"shopping_order_product\", joinColumns = @JoinColumn(name = \"order_id\"), inverseJoinColumns = @JoinColumn(name = \"product_id\"))", "type": "List<Product>", "name": "products"},
                    ],
                },
                "repositories": {
                    "CustomerRepository": "",
                    "ProductRepository": "",
                    "CustomerOrderRepository": "",
                },
                "service_code": shopping_service(),
                "rest_controller": shopping_rest(),
                "web_controller": shopping_web(),
                "data_loader": shopping_loader(),
                "template": shopping_template(),
                "readme_api": [
                    "GET /api/shopping/customers",
                    "GET /api/shopping/products",
                    "GET /api/shopping/orders",
                    "POST /api/shopping/products",
                    "POST /api/shopping/orders?customerId=1&productIds=1,2",
                ],
            },
            {
                "name": "college-management-system",
                "artifact": "college-management-system",
                "package": "com.assignment.collegemanagement",
                "class": "CollegeManagementSystemApplication",
                "title": "College Management System",
                "port": 8084,
                "db": "college_management_db",
                "service": "CollegeService",
                "entities": {
                    "Student": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "department"},
                        {"annotation": "@ManyToMany(mappedBy = \"students\")", "type": "List<Course>", "name": "courses"},
                    ],
                    "Faculty": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "designation"},
                        {"annotation": "@OneToMany(mappedBy = \"faculty\", cascade = CascadeType.ALL)", "type": "List<Course>", "name": "courses"},
                    ],
                    "Course": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "title"},
                        {"type": "String", "name": "code"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"faculty_id\")", "type": "Faculty", "name": "faculty"},
                        {"annotation": "@ManyToMany\n    @JoinTable(name = \"student_course\", joinColumns = @JoinColumn(name = \"course_id\"), inverseJoinColumns = @JoinColumn(name = \"student_id\"))", "type": "List<Student>", "name": "students"},
                    ],
                },
                "repositories": {
                    "StudentRepository": "",
                    "FacultyRepository": "",
                    "CourseRepository": "",
                },
                "service_code": college_service(),
                "rest_controller": college_rest(),
                "web_controller": college_web(),
                "data_loader": college_loader(),
                "template": college_template(),
                "readme_api": [
                    "GET /api/college/students",
                    "GET /api/college/faculty",
                    "GET /api/college/courses",
                    "POST /api/college/students",
                    "POST /api/college/enroll?studentId=1&courseId=1",
                    "POST /api/college/assign-faculty?facultyId=1&courseId=1",
                ],
            },
            {
                "name": "movie-booking-system",
                "artifact": "movie-booking-system",
                "package": "com.assignment.moviebooking",
                "class": "MovieBookingSystemApplication",
                "title": "Movie Booking System",
                "port": 8085,
                "db": "movie_booking_db",
                "service": "MovieBookingService",
                "entities": {
                    "Theater": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "location"},
                        {"annotation": "@OneToMany(mappedBy = \"theater\", cascade = CascadeType.ALL)", "type": "List<Movie>", "name": "movies"},
                    ],
                    "Movie": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "title"},
                        {"type": "int", "name": "availableSeats"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"theater_id\")", "type": "Theater", "name": "theater"},
                        {"annotation": "@OneToMany(mappedBy = \"movie\", cascade = CascadeType.ALL)", "type": "List<Ticket>", "name": "tickets"},
                    ],
                    "Ticket": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "customerName"},
                        {"type": "int", "name": "seatCount"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"movie_id\")", "type": "Movie", "name": "movie"},
                    ],
                },
                "repositories": {
                    "TheaterRepository": "",
                    "MovieRepository": "",
                    "TicketRepository": "",
                },
                "service_code": movie_service(),
                "rest_controller": movie_rest(),
                "web_controller": movie_web(),
                "data_loader": movie_loader(),
                "template": movie_template(),
                "readme_api": [
                    "GET /api/movies/theaters",
                    "GET /api/movies/list",
                    "GET /api/movies/tickets",
                    "POST /api/movies/book?movieId=1&customerName=Abhinav&seatCount=2",
                ],
            },
            {
                "name": "banking-system",
                "artifact": "banking-system",
                "package": "com.assignment.bankingsystem",
                "class": "BankingSystemApplication",
                "title": "Banking System",
                "port": 8086,
                "db": "banking_system_db",
                "service": "BankingService",
                "entities": {
                    "Customer": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "email"},
                        {"annotation": "@OneToMany(mappedBy = \"customer\", cascade = CascadeType.ALL)", "type": "List<Account>", "name": "accounts"},
                    ],
                    "Account": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "accountNumber"},
                        {"type": "double", "name": "balance"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"customer_id\")", "type": "Customer", "name": "customer"},
                        {"annotation": "@OneToMany(mappedBy = \"account\", cascade = CascadeType.ALL)", "type": "List<BankTransaction>", "name": "transactions"},
                    ],
                    "BankTransaction": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "transactionType"},
                        {"type": "double", "name": "amount"},
                        {"type": "LocalDateTime", "name": "transactionTime"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"account_id\")", "type": "Account", "name": "account"},
                    ],
                },
                "repositories": {
                    "CustomerRepository": "",
                    "AccountRepository": "",
                    "BankTransactionRepository": "List<BankTransaction> findByAccountIdOrderByTransactionTimeDesc(Long accountId);",
                },
                "service_code": banking_service(),
                "rest_controller": banking_rest(),
                "web_controller": banking_web(),
                "data_loader": banking_loader(),
                "template": banking_template(),
                "readme_api": [
                    "GET /api/banking/customers",
                    "GET /api/banking/accounts",
                    "GET /api/banking/transactions",
                    "POST /api/banking/deposit?accountId=1&amount=5000",
                    "POST /api/banking/withdraw?accountId=1&amount=1000",
                ],
            },
            {
                "name": "food-delivery-system",
                "artifact": "food-delivery-system",
                "package": "com.assignment.fooddelivery",
                "class": "FoodDeliverySystemApplication",
                "title": "Food Delivery System",
                "port": 8087,
                "db": "food_delivery_db",
                "service": "FoodDeliveryService",
                "entities": {
                    "AppUser": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "address"},
                        {"annotation": "@OneToMany(mappedBy = \"user\", cascade = CascadeType.ALL)", "type": "List<FoodOrder>", "name": "orders"},
                    ],
                    "Restaurant": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "cuisine"},
                        {"annotation": "@OneToMany(mappedBy = \"restaurant\", cascade = CascadeType.ALL)", "type": "List<FoodOrder>", "name": "orders"},
                    ],
                    "FoodOrder": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "items"},
                        {"type": "double", "name": "totalAmount"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"user_id\")", "type": "AppUser", "name": "user"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"restaurant_id\")", "type": "Restaurant", "name": "restaurant"},
                    ],
                },
                "repositories": {
                    "AppUserRepository": "",
                    "RestaurantRepository": "",
                    "FoodOrderRepository": "",
                },
                "service_code": food_service(),
                "rest_controller": food_rest(),
                "web_controller": food_web(),
                "data_loader": food_loader(),
                "template": food_template(),
                "readme_api": [
                    "GET /api/food/users",
                    "GET /api/food/restaurants",
                    "GET /api/food/orders",
                    "POST /api/food/orders?userId=1&restaurantId=1&items=Burger,Fries&totalAmount=250",
                ],
            },
            {
                "name": "employee-leave-management",
                "artifact": "employee-leave-management",
                "package": "com.assignment.leavemanagement",
                "class": "EmployeeLeaveManagementApplication",
                "title": "Employee Leave Management",
                "port": 8088,
                "db": "employee_leave_db",
                "service": "LeaveManagementService",
                "entities": {
                    "Manager": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "department"},
                        {"annotation": "@OneToMany(mappedBy = \"manager\", cascade = CascadeType.ALL)", "type": "List<Employee>", "name": "employees"},
                    ],
                    "Employee": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "String", "name": "name"},
                        {"type": "String", "name": "designation"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"manager_id\")", "type": "Manager", "name": "manager"},
                        {"annotation": "@OneToMany(mappedBy = \"employee\", cascade = CascadeType.ALL)", "type": "List<LeaveRequest>", "name": "leaveRequests"},
                    ],
                    "LeaveRequest": [
                        {"annotation": "@Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)", "type": "Long", "name": "id"},
                        {"type": "LocalDate", "name": "fromDate"},
                        {"type": "LocalDate", "name": "toDate"},
                        {"type": "String", "name": "reason"},
                        {"type": "String", "name": "status"},
                        {"annotation": "@ManyToOne\n    @JoinColumn(name = \"employee_id\")", "type": "Employee", "name": "employee"},
                    ],
                },
                "repositories": {
                    "ManagerRepository": "",
                    "EmployeeRepository": "",
                    "LeaveRequestRepository": "",
                },
                "service_code": leave_service(),
                "rest_controller": leave_rest(),
                "web_controller": leave_web(),
                "data_loader": leave_loader(),
                "template": leave_template(),
                "readme_api": [
                    "GET /api/leave/managers",
                    "GET /api/leave/employees",
                    "GET /api/leave/requests",
                    "POST /api/leave/apply?employeeId=1&fromDate=2026-03-28&toDate=2026-03-30&reason=Personal",
                    "POST /api/leave/update-status?requestId=1&status=APPROVED",
                ],
            },
        ]
    )


def repository_code(package_name, entity_name, repo_name, extra_methods):
    extra = f"\n\n    {extra_methods}\n" if extra_methods else "\n"
    return dedent(
        f"""
        package {package_name}.repository;

        import org.springframework.data.jpa.repository.JpaRepository;
        import {package_name}.entity.{entity_name};
        import java.util.List;

        public interface {repo_name} extends JpaRepository<{entity_name}, Long> {{{extra}}}
        """
    )


def generate():
    add_remaining_projects()
    readme = [dedent(README_HEADER).strip(), ""]
    for project in PROJECTS:
        base = ROOT / project["name"]
        src = base / "src/main/java" / project["package"].replace(".", "/")
        resources = base / "src/main/resources"

        write_file(base / "pom.xml", COMMON_POM.format(package=project["package"], artifact=project["artifact"], title=project["title"]))
        write_file(resources / "application.properties", COMMON_PROPERTIES.format(name=project["artifact"], port=project["port"], db=project["db"]))
        write_file(src / f"{project['class']}.java", APP_CLASS.format(package=project["package"], class_name=project["class"]))
        write_file(src / "exception/ResourceNotFoundException.java", RESOURCE_NOT_FOUND.format(package=project["package"]))
        write_file(src / "exception/GlobalExceptionHandler.java", GLOBAL_HANDLER.format(package=project["package"]))
        write_file(resources / "templates/error.html", ERROR_TEMPLATE)
        write_file(resources / "templates/index.html", project["template"])
        write_file(src / "service" / f"{project['service']}.java", project["service_code"])
        write_file(src / "controller" / f"{project['service'].replace('Service', '')}RestController.java", project["rest_controller"])
        write_file(src / "controller" / f"{project['service'].replace('Service', '')}ViewController.java", project["web_controller"])
        write_file(src / "config/DataLoader.java", project["data_loader"])

        entity_names = list(project["entities"].keys())
        for entity_name, fields in project["entities"].items():
            normalized = []
            for field in fields:
                current = dict(field)
                if current["type"].startswith("List<") and "name" in current and not current["type"].endswith(">"):
                    current["type"] = current["type"] + ">"
                normalized.append(current)
            write_file(src / "entity" / f"{entity_name}.java", entity_code(project["package"], entity_name, normalized))

        for repo_name, methods in project["repositories"].items():
            entity_name = repo_name.replace("Repository", "")
            write_file(src / "repository" / f"{repo_name}.java", repository_code(project["package"], entity_name, repo_name, methods))

        readme.append(f"### {project['title']}")
        readme.append(f"- Path: `{project['name']}`")
        readme.append(f"- Port: `{project['port']}`")
        readme.append("- Sample APIs:")
        for api in project["readme_api"]:
            readme.append(f"  - `{api}`")
        readme.append("")

    write_file(ROOT / "README.md", "\n".join(readme))


def hospital_service():
    return dedent("""
        package com.assignment.hospitalmanagement.service;

        import java.time.LocalDate;
        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.hospitalmanagement.entity.Appointment;
        import com.assignment.hospitalmanagement.entity.Doctor;
        import com.assignment.hospitalmanagement.entity.Patient;
        import com.assignment.hospitalmanagement.exception.ResourceNotFoundException;
        import com.assignment.hospitalmanagement.repository.AppointmentRepository;
        import com.assignment.hospitalmanagement.repository.DoctorRepository;
        import com.assignment.hospitalmanagement.repository.PatientRepository;

        @Service
        public class HospitalService {

            private final DoctorRepository doctorRepository;
            private final PatientRepository patientRepository;
            private final AppointmentRepository appointmentRepository;

            public HospitalService(DoctorRepository doctorRepository, PatientRepository patientRepository,
                    AppointmentRepository appointmentRepository) {
                this.doctorRepository = doctorRepository;
                this.patientRepository = patientRepository;
                this.appointmentRepository = appointmentRepository;
            }

            public List<Doctor> getAllDoctors() {
                return doctorRepository.findAll();
            }

            public List<Patient> getAllPatients() {
                return patientRepository.findAll();
            }

            public List<Appointment> getAllAppointments() {
                return appointmentRepository.findAll();
            }

            public Doctor saveDoctor(Doctor doctor) {
                return doctorRepository.save(doctor);
            }

            public Patient savePatient(Patient patient) {
                return patientRepository.save(patient);
            }

            public Appointment bookAppointment(Long doctorId, Long patientId, LocalDate appointmentDate, String reason) {
                Doctor doctor = doctorRepository.findById(doctorId)
                        .orElseThrow(() -> new ResourceNotFoundException("Doctor not found"));
                Patient patient = patientRepository.findById(patientId)
                        .orElseThrow(() -> new ResourceNotFoundException("Patient not found"));
                Appointment appointment = new Appointment();
                appointment.setDoctor(doctor);
                appointment.setPatient(patient);
                appointment.setAppointmentDate(appointmentDate);
                appointment.setReason(reason);
                return appointmentRepository.save(appointment);
            }
        }
    """)


def hospital_rest():
    return dedent("""
        package com.assignment.hospitalmanagement.controller;

        import java.time.LocalDate;
        import java.util.List;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.hospitalmanagement.entity.Appointment;
        import com.assignment.hospitalmanagement.entity.Doctor;
        import com.assignment.hospitalmanagement.entity.Patient;
        import com.assignment.hospitalmanagement.service.HospitalService;

        @RestController
        @RequestMapping("/api/hospital")
        public class HospitalRestController {

            private final HospitalService hospitalService;

            public HospitalRestController(HospitalService hospitalService) {
                this.hospitalService = hospitalService;
            }

            @GetMapping("/doctors")
            public List<Doctor> getDoctors() {
                return hospitalService.getAllDoctors();
            }

            @GetMapping("/patients")
            public List<Patient> getPatients() {
                return hospitalService.getAllPatients();
            }

            @GetMapping("/appointments")
            public List<Appointment> getAppointments() {
                return hospitalService.getAllAppointments();
            }

            @PostMapping("/doctors")
            public Doctor addDoctor(@RequestBody Doctor doctor) {
                return hospitalService.saveDoctor(doctor);
            }

            @PostMapping("/patients")
            public Patient addPatient(@RequestBody Patient patient) {
                return hospitalService.savePatient(patient);
            }

            @PostMapping("/appointments")
            public Appointment bookAppointment(@RequestParam Long doctorId, @RequestParam Long patientId,
                    @RequestParam String appointmentDate, @RequestParam String reason) {
                return hospitalService.bookAppointment(doctorId, patientId, LocalDate.parse(appointmentDate), reason);
            }
        }
    """)


def hospital_web():
    return dedent("""
        package com.assignment.hospitalmanagement.controller;

        import java.time.LocalDate;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.hospitalmanagement.entity.Doctor;
        import com.assignment.hospitalmanagement.entity.Patient;
        import com.assignment.hospitalmanagement.service.HospitalService;

        @Controller
        public class HospitalViewController {

            private final HospitalService hospitalService;

            public HospitalViewController(HospitalService hospitalService) {
                this.hospitalService = hospitalService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("doctors", hospitalService.getAllDoctors());
                model.addAttribute("patients", hospitalService.getAllPatients());
                model.addAttribute("appointments", hospitalService.getAllAppointments());
                model.addAttribute("doctor", new Doctor());
                model.addAttribute("patient", new Patient());
                return "index";
            }

            @PostMapping("/doctors/save")
            public String saveDoctor(Doctor doctor) {
                hospitalService.saveDoctor(doctor);
                return "redirect:/";
            }

            @PostMapping("/patients/save")
            public String savePatient(Patient patient) {
                hospitalService.savePatient(patient);
                return "redirect:/";
            }

            @PostMapping("/appointments/save")
            public String saveAppointment(@RequestParam Long doctorId, @RequestParam Long patientId,
                    @RequestParam String appointmentDate, @RequestParam String reason) {
                hospitalService.bookAppointment(doctorId, patientId, LocalDate.parse(appointmentDate), reason);
                return "redirect:/";
            }
        }
    """)


def hospital_loader():
    return dedent("""
        package com.assignment.hospitalmanagement.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.hospitalmanagement.entity.Doctor;
        import com.assignment.hospitalmanagement.entity.Patient;
        import com.assignment.hospitalmanagement.repository.DoctorRepository;
        import com.assignment.hospitalmanagement.repository.PatientRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadHospitalData(DoctorRepository doctorRepository, PatientRepository patientRepository) {
                return args -> {
                    if (doctorRepository.count() == 0) {
                        Doctor doctor = new Doctor();
                        doctor.setName("Dr. Ayush Kumar");
                        doctor.setSpecialization("Cardiology");
                        doctor.setAppointments(new ArrayList<>());
                        doctorRepository.save(doctor);

                        Patient patient = new Patient();
                        patient.setName("Priyanshu Sharma");
                        patient.setAge(29);
                        patient.setAppointments(new ArrayList<>());
                        patientRepository.save(patient);
                    }
                };
            }
        }
    """)


def hospital_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Hospital Management System</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">Hospital Management System</h1>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card shadow-sm"><div class="card-body">
                        <h5>Add Doctor</h5>
                        <form action="/doctors/save" method="post">
                            <input class="form-control mb-2" name="name" placeholder="Doctor name" required>
                            <input class="form-control mb-2" name="specialization" placeholder="Specialization" required>
                            <button class="btn btn-primary w-100">Save Doctor</button>
                        </form>
                    </div></div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-sm"><div class="card-body">
                        <h5>Add Patient</h5>
                        <form action="/patients/save" method="post">
                            <input class="form-control mb-2" name="name" placeholder="Patient name" required>
                            <input class="form-control mb-2" name="age" type="number" placeholder="Age" required>
                            <button class="btn btn-primary w-100">Save Patient</button>
                        </form>
                    </div></div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-sm"><div class="card-body">
                        <h5>Book Appointment</h5>
                        <form action="/appointments/save" method="post">
                            <select class="form-select mb-2" name="doctorId" required>
                                <option value="">Select doctor</option>
                                <option th:each="doctor : ${doctors}" th:value="${doctor.id}" th:text="${doctor.name}"></option>
                            </select>
                            <select class="form-select mb-2" name="patientId" required>
                                <option value="">Select patient</option>
                                <option th:each="patient : ${patients}" th:value="${patient.id}" th:text="${patient.name}"></option>
                            </select>
                            <input class="form-control mb-2" type="date" name="appointmentDate" required>
                            <input class="form-control mb-2" name="reason" placeholder="Reason" required>
                            <button class="btn btn-success w-100">Book</button>
                        </form>
                    </div></div>
                </div>
            </div>
            <div class="card shadow-sm mt-4"><div class="card-body">
                <h5>Appointments</h5>
                <table class="table table-bordered">
                    <thead><tr><th>Date</th><th>Doctor</th><th>Patient</th><th>Reason</th></tr></thead>
                    <tbody>
                        <tr th:each="appointment : ${appointments}">
                            <td th:text="${appointment.appointmentDate}"></td>
                            <td th:text="${appointment.doctor.name}"></td>
                            <td th:text="${appointment.patient.name}"></td>
                            <td th:text="${appointment.reason}"></td>
                        </tr>
                    </tbody>
                </table>
            </div></div>
        </div>
        </body>
        </html>
    """)


def shopping_service():
    return dedent("""
        package com.assignment.onlineshopping.service;

        import java.time.LocalDate;
        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.onlineshopping.entity.Customer;
        import com.assignment.onlineshopping.entity.CustomerOrder;
        import com.assignment.onlineshopping.entity.Product;
        import com.assignment.onlineshopping.exception.ResourceNotFoundException;
        import com.assignment.onlineshopping.repository.CustomerOrderRepository;
        import com.assignment.onlineshopping.repository.CustomerRepository;
        import com.assignment.onlineshopping.repository.ProductRepository;

        @Service
        public class ShoppingService {

            private final CustomerRepository customerRepository;
            private final ProductRepository productRepository;
            private final CustomerOrderRepository orderRepository;

            public ShoppingService(CustomerRepository customerRepository, ProductRepository productRepository,
                    CustomerOrderRepository orderRepository) {
                this.customerRepository = customerRepository;
                this.productRepository = productRepository;
                this.orderRepository = orderRepository;
            }

            public List<Customer> getAllCustomers() {
                return customerRepository.findAll();
            }

            public List<Product> getAllProducts() {
                return productRepository.findAll();
            }

            public List<CustomerOrder> getAllOrders() {
                return orderRepository.findAll();
            }

            public Customer saveCustomer(Customer customer) {
                return customerRepository.save(customer);
            }

            public Product saveProduct(Product product) {
                return productRepository.save(product);
            }

            public CustomerOrder placeOrder(Long customerId, List<Long> productIds) {
                Customer customer = customerRepository.findById(customerId)
                        .orElseThrow(() -> new ResourceNotFoundException("Customer not found"));
                List<Product> products = productRepository.findAllById(productIds);
                if (products.isEmpty()) {
                    throw new ResourceNotFoundException("Products not found");
                }
                double total = products.stream().mapToDouble(Product::getPrice).sum();
                CustomerOrder order = new CustomerOrder();
                order.setCustomer(customer);
                order.setProducts(products);
                order.setOrderDate(LocalDate.now());
                order.setTotalAmount(total);
                return orderRepository.save(order);
            }
        }
    """)


def shopping_rest():
    return dedent("""
        package com.assignment.onlineshopping.controller;

        import java.util.Arrays;
        import java.util.List;
        import java.util.stream.Collectors;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.onlineshopping.entity.Customer;
        import com.assignment.onlineshopping.entity.CustomerOrder;
        import com.assignment.onlineshopping.entity.Product;
        import com.assignment.onlineshopping.service.ShoppingService;

        @RestController
        @RequestMapping("/api/shopping")
        public class ShoppingRestController {

            private final ShoppingService shoppingService;

            public ShoppingRestController(ShoppingService shoppingService) {
                this.shoppingService = shoppingService;
            }

            @GetMapping("/customers")
            public List<Customer> getCustomers() {
                return shoppingService.getAllCustomers();
            }

            @GetMapping("/products")
            public List<Product> getProducts() {
                return shoppingService.getAllProducts();
            }

            @GetMapping("/orders")
            public List<CustomerOrder> getOrders() {
                return shoppingService.getAllOrders();
            }

            @PostMapping("/customers")
            public Customer addCustomer(@RequestBody Customer customer) {
                return shoppingService.saveCustomer(customer);
            }

            @PostMapping("/products")
            public Product addProduct(@RequestBody Product product) {
                return shoppingService.saveProduct(product);
            }

            @PostMapping("/orders")
            public CustomerOrder placeOrder(@RequestParam Long customerId, @RequestParam String productIds) {
                List<Long> ids = Arrays.stream(productIds.split(",")).map(String::trim).map(Long::parseLong)
                        .collect(Collectors.toList());
                return shoppingService.placeOrder(customerId, ids);
            }
        }
    """)


def shopping_web():
    return dedent("""
        package com.assignment.onlineshopping.controller;

        import java.util.Arrays;
        import java.util.List;
        import java.util.stream.Collectors;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.onlineshopping.entity.Customer;
        import com.assignment.onlineshopping.entity.Product;
        import com.assignment.onlineshopping.service.ShoppingService;

        @Controller
        public class ShoppingViewController {

            private final ShoppingService shoppingService;

            public ShoppingViewController(ShoppingService shoppingService) {
                this.shoppingService = shoppingService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("customers", shoppingService.getAllCustomers());
                model.addAttribute("products", shoppingService.getAllProducts());
                model.addAttribute("orders", shoppingService.getAllOrders());
                model.addAttribute("customer", new Customer());
                model.addAttribute("product", new Product());
                return "index";
            }

            @PostMapping("/customers/save")
            public String saveCustomer(Customer customer) {
                shoppingService.saveCustomer(customer);
                return "redirect:/";
            }

            @PostMapping("/products/save")
            public String saveProduct(Product product) {
                shoppingService.saveProduct(product);
                return "redirect:/";
            }

            @PostMapping("/orders/save")
            public String saveOrder(@RequestParam Long customerId, @RequestParam String productIds) {
                List<Long> ids = Arrays.stream(productIds.split(",")).map(String::trim).map(Long::parseLong)
                        .collect(Collectors.toList());
                shoppingService.placeOrder(customerId, ids);
                return "redirect:/";
            }
        }
    """)


def shopping_loader():
    return dedent("""
        package com.assignment.onlineshopping.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.onlineshopping.entity.Customer;
        import com.assignment.onlineshopping.entity.Product;
        import com.assignment.onlineshopping.repository.CustomerRepository;
        import com.assignment.onlineshopping.repository.ProductRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadShoppingData(CustomerRepository customerRepository, ProductRepository productRepository) {
                return args -> {
                    if (customerRepository.count() == 0) {
                        Customer customer = new Customer();
                        customer.setName("Rakshit Pandey");
                        customer.setEmail("rakshit@example.com");
                        customer.setOrders(new ArrayList<>());
                        customerRepository.save(customer);

                        Product product1 = new Product();
                        product1.setName("Laptop Bag");
                        product1.setPrice(1200);
                        product1.setStock(12);
                        product1.setOrders(new ArrayList<>());

                        Product product2 = new Product();
                        product2.setName("Wireless Mouse");
                        product2.setPrice(800);
                        product2.setStock(20);
                        product2.setOrders(new ArrayList<>());

                        productRepository.save(product1);
                        productRepository.save(product2);
                    }
                };
            }
        }
    """)


def shopping_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Online Shopping System</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">Online Shopping System</h1>
            <div class="row g-4">
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Customer</h5>
                    <form action="/customers/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Customer name" required>
                        <input class="form-control mb-2" name="email" placeholder="Email" required>
                        <button class="btn btn-primary w-100">Save Customer</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Product</h5>
                    <form action="/products/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Product name" required>
                        <input class="form-control mb-2" name="price" type="number" step="0.01" placeholder="Price" required>
                        <input class="form-control mb-2" name="stock" type="number" placeholder="Stock" required>
                        <button class="btn btn-primary w-100">Save Product</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Place Order</h5>
                    <form action="/orders/save" method="post">
                        <select class="form-select mb-2" name="customerId" required>
                            <option value="">Select customer</option>
                            <option th:each="customer : ${customers}" th:value="${customer.id}" th:text="${customer.name}"></option>
                        </select>
                        <input class="form-control mb-2" name="productIds" placeholder="Product IDs like 1,2" required>
                        <button class="btn btn-success w-100">Place Order</button>
                    </form>
                </div></div></div>
            </div>
            <div class="card shadow-sm mt-4"><div class="card-body">
                <h5>Order List</h5>
                <table class="table table-bordered">
                    <thead><tr><th>Customer</th><th>Date</th><th>Total Amount</th></tr></thead>
                    <tbody>
                        <tr th:each="order : ${orders}">
                            <td th:text="${order.customer.name}"></td>
                            <td th:text="${order.orderDate}"></td>
                            <td th:text="${order.totalAmount}"></td>
                        </tr>
                    </tbody>
                </table>
            </div></div>
        </div>
        </body>
        </html>
    """)


def college_service():
    return dedent("""
        package com.assignment.collegemanagement.service;

        import java.util.ArrayList;
        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.collegemanagement.entity.Course;
        import com.assignment.collegemanagement.entity.Faculty;
        import com.assignment.collegemanagement.entity.Student;
        import com.assignment.collegemanagement.exception.ResourceNotFoundException;
        import com.assignment.collegemanagement.repository.CourseRepository;
        import com.assignment.collegemanagement.repository.FacultyRepository;
        import com.assignment.collegemanagement.repository.StudentRepository;

        @Service
        public class CollegeService {

            private final StudentRepository studentRepository;
            private final CourseRepository courseRepository;
            private final FacultyRepository facultyRepository;

            public CollegeService(StudentRepository studentRepository, CourseRepository courseRepository,
                    FacultyRepository facultyRepository) {
                this.studentRepository = studentRepository;
                this.courseRepository = courseRepository;
                this.facultyRepository = facultyRepository;
            }

            public List<Student> getAllStudents() {
                return studentRepository.findAll();
            }

            public List<Course> getAllCourses() {
                return courseRepository.findAll();
            }

            public List<Faculty> getAllFaculty() {
                return facultyRepository.findAll();
            }

            public Student saveStudent(Student student) {
                if (student.getCourses() == null) {
                    student.setCourses(new ArrayList<>());
                }
                return studentRepository.save(student);
            }

            public Course saveCourse(Course course) {
                if (course.getStudents() == null) {
                    course.setStudents(new ArrayList<>());
                }
                return courseRepository.save(course);
            }

            public Faculty saveFaculty(Faculty faculty) {
                if (faculty.getCourses() == null) {
                    faculty.setCourses(new ArrayList<>());
                }
                return facultyRepository.save(faculty);
            }

            public void enrollStudent(Long studentId, Long courseId) {
                Student student = studentRepository.findById(studentId)
                        .orElseThrow(() -> new ResourceNotFoundException("Student not found"));
                Course course = courseRepository.findById(courseId)
                        .orElseThrow(() -> new ResourceNotFoundException("Course not found"));
                course.getStudents().add(student);
                courseRepository.save(course);
            }

            public void assignFaculty(Long facultyId, Long courseId) {
                Faculty faculty = facultyRepository.findById(facultyId)
                        .orElseThrow(() -> new ResourceNotFoundException("Faculty not found"));
                Course course = courseRepository.findById(courseId)
                        .orElseThrow(() -> new ResourceNotFoundException("Course not found"));
                course.setFaculty(faculty);
                courseRepository.save(course);
            }
        }
    """)


def college_rest():
    return dedent("""
        package com.assignment.collegemanagement.controller;

        import java.util.List;

        import org.springframework.http.ResponseEntity;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.collegemanagement.entity.Course;
        import com.assignment.collegemanagement.entity.Faculty;
        import com.assignment.collegemanagement.entity.Student;
        import com.assignment.collegemanagement.service.CollegeService;

        @RestController
        @RequestMapping("/api/college")
        public class CollegeRestController {

            private final CollegeService collegeService;

            public CollegeRestController(CollegeService collegeService) {
                this.collegeService = collegeService;
            }

            @GetMapping("/students")
            public List<Student> getStudents() {
                return collegeService.getAllStudents();
            }

            @GetMapping("/courses")
            public List<Course> getCourses() {
                return collegeService.getAllCourses();
            }

            @GetMapping("/faculty")
            public List<Faculty> getFaculty() {
                return collegeService.getAllFaculty();
            }

            @PostMapping("/students")
            public Student addStudent(@RequestBody Student student) {
                return collegeService.saveStudent(student);
            }

            @PostMapping("/courses")
            public Course addCourse(@RequestBody Course course) {
                return collegeService.saveCourse(course);
            }

            @PostMapping("/faculty")
            public Faculty addFaculty(@RequestBody Faculty faculty) {
                return collegeService.saveFaculty(faculty);
            }

            @PostMapping("/enroll")
            public ResponseEntity<String> enrollStudent(@RequestParam Long studentId, @RequestParam Long courseId) {
                collegeService.enrollStudent(studentId, courseId);
                return ResponseEntity.ok("Student enrolled successfully");
            }

            @PostMapping("/assign-faculty")
            public ResponseEntity<String> assignFaculty(@RequestParam Long facultyId, @RequestParam Long courseId) {
                collegeService.assignFaculty(facultyId, courseId);
                return ResponseEntity.ok("Faculty assigned successfully");
            }
        }
    """)


def college_web():
    return dedent("""
        package com.assignment.collegemanagement.controller;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.collegemanagement.entity.Course;
        import com.assignment.collegemanagement.entity.Faculty;
        import com.assignment.collegemanagement.entity.Student;
        import com.assignment.collegemanagement.service.CollegeService;

        @Controller
        public class CollegeViewController {

            private final CollegeService collegeService;

            public CollegeViewController(CollegeService collegeService) {
                this.collegeService = collegeService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("students", collegeService.getAllStudents());
                model.addAttribute("courses", collegeService.getAllCourses());
                model.addAttribute("facultyList", collegeService.getAllFaculty());
                model.addAttribute("student", new Student());
                model.addAttribute("course", new Course());
                model.addAttribute("faculty", new Faculty());
                return "index";
            }

            @PostMapping("/students/save")
            public String saveStudent(Student student) {
                collegeService.saveStudent(student);
                return "redirect:/";
            }

            @PostMapping("/courses/save")
            public String saveCourse(Course course) {
                collegeService.saveCourse(course);
                return "redirect:/";
            }

            @PostMapping("/faculty/save")
            public String saveFaculty(Faculty faculty) {
                collegeService.saveFaculty(faculty);
                return "redirect:/";
            }

            @PostMapping("/enroll")
            public String enroll(@RequestParam Long studentId, @RequestParam Long courseId) {
                collegeService.enrollStudent(studentId, courseId);
                return "redirect:/";
            }

            @PostMapping("/assign-faculty")
            public String assignFaculty(@RequestParam Long facultyId, @RequestParam Long courseId) {
                collegeService.assignFaculty(facultyId, courseId);
                return "redirect:/";
            }
        }
    """)


def college_loader():
    return dedent("""
        package com.assignment.collegemanagement.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.collegemanagement.entity.Course;
        import com.assignment.collegemanagement.entity.Faculty;
        import com.assignment.collegemanagement.entity.Student;
        import com.assignment.collegemanagement.repository.CourseRepository;
        import com.assignment.collegemanagement.repository.FacultyRepository;
        import com.assignment.collegemanagement.repository.StudentRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadCollegeData(StudentRepository studentRepository, CourseRepository courseRepository,
                    FacultyRepository facultyRepository) {
                return args -> {
                    if (studentRepository.count() == 0) {
                        Student student = new Student();
                        student.setName("Rishabh Shukla");
                        student.setDepartment("Computer Science");
                        student.setCourses(new ArrayList<>());
                        studentRepository.save(student);

                        Faculty faculty = new Faculty();
                        faculty.setName("Prof. Sandeep Rao");
                        faculty.setDesignation("Assistant Professor");
                        faculty.setCourses(new ArrayList<>());
                        facultyRepository.save(faculty);

                        Course course = new Course();
                        course.setTitle("Database Systems");
                        course.setCode("CS301");
                        course.setStudents(new ArrayList<>());
                        courseRepository.save(course);
                    }
                };
            }
        }
    """)


def college_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>College Management System</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">College Management System</h1>
            <div class="row g-4">
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Student</h5>
                    <form action="/students/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Student name" required>
                        <input class="form-control mb-2" name="department" placeholder="Department" required>
                        <button class="btn btn-primary w-100">Save Student</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Faculty</h5>
                    <form action="/faculty/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Faculty name" required>
                        <input class="form-control mb-2" name="designation" placeholder="Designation" required>
                        <button class="btn btn-primary w-100">Save Faculty</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Course</h5>
                    <form action="/courses/save" method="post">
                        <input class="form-control mb-2" name="title" placeholder="Course title" required>
                        <input class="form-control mb-2" name="code" placeholder="Course code" required>
                        <button class="btn btn-primary w-100">Save Course</button>
                    </form>
                </div></div></div>
            </div>
            <div class="row g-4 mt-1">
                <div class="col-md-6"><div class="card shadow-sm"><div class="card-body">
                    <h5>Enroll Student</h5>
                    <form action="/enroll" method="post" class="row g-2">
                        <div class="col-6">
                            <select class="form-select" name="studentId" required>
                                <option value="">Student</option>
                                <option th:each="student : ${students}" th:value="${student.id}" th:text="${student.name}"></option>
                            </select>
                        </div>
                        <div class="col-6">
                            <select class="form-select" name="courseId" required>
                                <option value="">Course</option>
                                <option th:each="course : ${courses}" th:value="${course.id}" th:text="${course.title}"></option>
                            </select>
                        </div>
                        <div class="col-12"><button class="btn btn-success w-100">Enroll</button></div>
                    </form>
                </div></div></div>
                <div class="col-md-6"><div class="card shadow-sm"><div class="card-body">
                    <h5>Assign Faculty</h5>
                    <form action="/assign-faculty" method="post" class="row g-2">
                        <div class="col-6">
                            <select class="form-select" name="facultyId" required>
                                <option value="">Faculty</option>
                                <option th:each="faculty : ${facultyList}" th:value="${faculty.id}" th:text="${faculty.name}"></option>
                            </select>
                        </div>
                        <div class="col-6">
                            <select class="form-select" name="courseId" required>
                                <option value="">Course</option>
                                <option th:each="course : ${courses}" th:value="${course.id}" th:text="${course.title}"></option>
                            </select>
                        </div>
                        <div class="col-12"><button class="btn btn-outline-secondary w-100">Assign</button></div>
                    </form>
                </div></div></div>
            </div>
        </div>
        </body>
        </html>
    """)


def movie_service():
    return dedent("""
        package com.assignment.moviebooking.service;

        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.moviebooking.entity.Movie;
        import com.assignment.moviebooking.entity.Theater;
        import com.assignment.moviebooking.entity.Ticket;
        import com.assignment.moviebooking.exception.ResourceNotFoundException;
        import com.assignment.moviebooking.repository.MovieRepository;
        import com.assignment.moviebooking.repository.TheaterRepository;
        import com.assignment.moviebooking.repository.TicketRepository;

        @Service
        public class MovieBookingService {

            private final TheaterRepository theaterRepository;
            private final MovieRepository movieRepository;
            private final TicketRepository ticketRepository;

            public MovieBookingService(TheaterRepository theaterRepository, MovieRepository movieRepository,
                    TicketRepository ticketRepository) {
                this.theaterRepository = theaterRepository;
                this.movieRepository = movieRepository;
                this.ticketRepository = ticketRepository;
            }

            public List<Theater> getAllTheaters() {
                return theaterRepository.findAll();
            }

            public List<Movie> getAllMovies() {
                return movieRepository.findAll();
            }

            public List<Ticket> getAllTickets() {
                return ticketRepository.findAll();
            }

            public Theater saveTheater(Theater theater) {
                return theaterRepository.save(theater);
            }

            public Movie saveMovie(Long theaterId, Movie movie) {
                Theater theater = theaterRepository.findById(theaterId)
                        .orElseThrow(() -> new ResourceNotFoundException("Theater not found"));
                movie.setTheater(theater);
                return movieRepository.save(movie);
            }

            public Ticket bookTicket(Long movieId, String customerName, int seatCount) {
                Movie movie = movieRepository.findById(movieId)
                        .orElseThrow(() -> new ResourceNotFoundException("Movie not found"));
                if (movie.getAvailableSeats() < seatCount) {
                    throw new ResourceNotFoundException("Requested seats not available");
                }
                movie.setAvailableSeats(movie.getAvailableSeats() - seatCount);
                movieRepository.save(movie);
                Ticket ticket = new Ticket();
                ticket.setMovie(movie);
                ticket.setCustomerName(customerName);
                ticket.setSeatCount(seatCount);
                return ticketRepository.save(ticket);
            }
        }
    """)


def movie_rest():
    return dedent("""
        package com.assignment.moviebooking.controller;

        import java.util.List;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.moviebooking.entity.Movie;
        import com.assignment.moviebooking.entity.Theater;
        import com.assignment.moviebooking.entity.Ticket;
        import com.assignment.moviebooking.service.MovieBookingService;

        @RestController
        @RequestMapping("/api/movies")
        public class MovieBookingRestController {

            private final MovieBookingService movieBookingService;

            public MovieBookingRestController(MovieBookingService movieBookingService) {
                this.movieBookingService = movieBookingService;
            }

            @GetMapping("/theaters")
            public List<Theater> getTheaters() {
                return movieBookingService.getAllTheaters();
            }

            @GetMapping("/list")
            public List<Movie> getMovies() {
                return movieBookingService.getAllMovies();
            }

            @GetMapping("/tickets")
            public List<Ticket> getTickets() {
                return movieBookingService.getAllTickets();
            }

            @PostMapping("/theaters")
            public Theater addTheater(@RequestBody Theater theater) {
                return movieBookingService.saveTheater(theater);
            }

            @PostMapping("/movies")
            public Movie addMovie(@RequestParam Long theaterId, @RequestBody Movie movie) {
                return movieBookingService.saveMovie(theaterId, movie);
            }

            @PostMapping("/book")
            public Ticket bookTicket(@RequestParam Long movieId, @RequestParam String customerName,
                    @RequestParam int seatCount) {
                return movieBookingService.bookTicket(movieId, customerName, seatCount);
            }
        }
    """)


def movie_web():
    return dedent("""
        package com.assignment.moviebooking.controller;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.moviebooking.entity.Movie;
        import com.assignment.moviebooking.entity.Theater;
        import com.assignment.moviebooking.service.MovieBookingService;

        @Controller
        public class MovieBookingViewController {

            private final MovieBookingService movieBookingService;

            public MovieBookingViewController(MovieBookingService movieBookingService) {
                this.movieBookingService = movieBookingService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("theaters", movieBookingService.getAllTheaters());
                model.addAttribute("movies", movieBookingService.getAllMovies());
                model.addAttribute("tickets", movieBookingService.getAllTickets());
                model.addAttribute("theater", new Theater());
                model.addAttribute("movie", new Movie());
                return "index";
            }

            @PostMapping("/theaters/save")
            public String saveTheater(Theater theater) {
                movieBookingService.saveTheater(theater);
                return "redirect:/";
            }

            @PostMapping("/movies/save")
            public String saveMovie(@RequestParam Long theaterId, Movie movie) {
                movieBookingService.saveMovie(theaterId, movie);
                return "redirect:/";
            }

            @PostMapping("/tickets/save")
            public String bookTicket(@RequestParam Long movieId, @RequestParam String customerName,
                    @RequestParam int seatCount) {
                movieBookingService.bookTicket(movieId, customerName, seatCount);
                return "redirect:/";
            }
        }
    """)


def movie_loader():
    return dedent("""
        package com.assignment.moviebooking.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.moviebooking.entity.Movie;
        import com.assignment.moviebooking.entity.Theater;
        import com.assignment.moviebooking.repository.MovieRepository;
        import com.assignment.moviebooking.repository.TheaterRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadMovieData(TheaterRepository theaterRepository, MovieRepository movieRepository) {
                return args -> {
                    if (theaterRepository.count() == 0) {
                        Theater theater = new Theater();
                        theater.setName("PVR Central");
                        theater.setLocation("City Mall");
                        theater.setMovies(new ArrayList<>());
                        theaterRepository.save(theater);

                        Movie movie = new Movie();
                        movie.setTitle("Campus Days");
                        movie.setAvailableSeats(80);
                        movie.setTheater(theater);
                        movie.setTickets(new ArrayList<>());
                        movieRepository.save(movie);
                    }
                };
            }
        }
    """)


def movie_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Movie Booking System</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">Movie Booking System</h1>
            <div class="row g-4">
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Theater</h5>
                    <form action="/theaters/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Theater name" required>
                        <input class="form-control mb-2" name="location" placeholder="Location" required>
                        <button class="btn btn-primary w-100">Save Theater</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Movie</h5>
                    <form action="/movies/save" method="post">
                        <select class="form-select mb-2" name="theaterId" required>
                            <option value="">Select theater</option>
                            <option th:each="theater : ${theaters}" th:value="${theater.id}" th:text="${theater.name}"></option>
                        </select>
                        <input class="form-control mb-2" name="title" placeholder="Movie title" required>
                        <input class="form-control mb-2" name="availableSeats" type="number" placeholder="Available seats" required>
                        <button class="btn btn-primary w-100">Save Movie</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Book Ticket</h5>
                    <form action="/tickets/save" method="post">
                        <select class="form-select mb-2" name="movieId" required>
                            <option value="">Select movie</option>
                            <option th:each="movie : ${movies}" th:value="${movie.id}" th:text="${movie.title}"></option>
                        </select>
                        <input class="form-control mb-2" name="customerName" placeholder="Customer name" required>
                        <input class="form-control mb-2" name="seatCount" type="number" placeholder="Seat count" required>
                        <button class="btn btn-success w-100">Book Ticket</button>
                    </form>
                </div></div></div>
            </div>
            <div class="card shadow-sm mt-4"><div class="card-body">
                <h5>Available Seats</h5>
                <table class="table table-bordered">
                    <thead><tr><th>Movie</th><th>Theater</th><th>Seats Left</th></tr></thead>
                    <tbody>
                        <tr th:each="movie : ${movies}">
                            <td th:text="${movie.title}"></td>
                            <td th:text="${movie.theater != null ? movie.theater.name : '-'}"></td>
                            <td th:text="${movie.availableSeats}"></td>
                        </tr>
                    </tbody>
                </table>
            </div></div>
        </div>
        </body>
        </html>
    """)


def banking_service():
    return dedent("""
        package com.assignment.bankingsystem.service;

        import java.time.LocalDateTime;
        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.bankingsystem.entity.Account;
        import com.assignment.bankingsystem.entity.BankTransaction;
        import com.assignment.bankingsystem.entity.Customer;
        import com.assignment.bankingsystem.exception.ResourceNotFoundException;
        import com.assignment.bankingsystem.repository.AccountRepository;
        import com.assignment.bankingsystem.repository.BankTransactionRepository;
        import com.assignment.bankingsystem.repository.CustomerRepository;

        @Service
        public class BankingService {

            private final CustomerRepository customerRepository;
            private final AccountRepository accountRepository;
            private final BankTransactionRepository transactionRepository;

            public BankingService(CustomerRepository customerRepository, AccountRepository accountRepository,
                    BankTransactionRepository transactionRepository) {
                this.customerRepository = customerRepository;
                this.accountRepository = accountRepository;
                this.transactionRepository = transactionRepository;
            }

            public List<Customer> getAllCustomers() {
                return customerRepository.findAll();
            }

            public List<Account> getAllAccounts() {
                return accountRepository.findAll();
            }

            public List<BankTransaction> getAllTransactions() {
                return transactionRepository.findAll();
            }

            public Customer saveCustomer(Customer customer) {
                return customerRepository.save(customer);
            }

            public Account saveAccount(Long customerId, Account account) {
                Customer customer = customerRepository.findById(customerId)
                        .orElseThrow(() -> new ResourceNotFoundException("Customer not found"));
                account.setCustomer(customer);
                return accountRepository.save(account);
            }

            public Account deposit(Long accountId, double amount) {
                Account account = accountRepository.findById(accountId)
                        .orElseThrow(() -> new ResourceNotFoundException("Account not found"));
                account.setBalance(account.getBalance() + amount);
                accountRepository.save(account);
                saveTransaction(account, "DEPOSIT", amount);
                return account;
            }

            public Account withdraw(Long accountId, double amount) {
                Account account = accountRepository.findById(accountId)
                        .orElseThrow(() -> new ResourceNotFoundException("Account not found"));
                if (account.getBalance() < amount) {
                    throw new ResourceNotFoundException("Insufficient balance");
                }
                account.setBalance(account.getBalance() - amount);
                accountRepository.save(account);
                saveTransaction(account, "WITHDRAW", amount);
                return account;
            }

            private void saveTransaction(Account account, String type, double amount) {
                BankTransaction transaction = new BankTransaction();
                transaction.setAccount(account);
                transaction.setTransactionType(type);
                transaction.setAmount(amount);
                transaction.setTransactionTime(LocalDateTime.now());
                transactionRepository.save(transaction);
            }
        }
    """)


def banking_rest():
    return dedent("""
        package com.assignment.bankingsystem.controller;

        import java.util.List;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.bankingsystem.entity.Account;
        import com.assignment.bankingsystem.entity.BankTransaction;
        import com.assignment.bankingsystem.entity.Customer;
        import com.assignment.bankingsystem.service.BankingService;

        @RestController
        @RequestMapping("/api/banking")
        public class BankingRestController {

            private final BankingService bankingService;

            public BankingRestController(BankingService bankingService) {
                this.bankingService = bankingService;
            }

            @GetMapping("/customers")
            public List<Customer> getCustomers() {
                return bankingService.getAllCustomers();
            }

            @GetMapping("/accounts")
            public List<Account> getAccounts() {
                return bankingService.getAllAccounts();
            }

            @GetMapping("/transactions")
            public List<BankTransaction> getTransactions() {
                return bankingService.getAllTransactions();
            }

            @PostMapping("/customers")
            public Customer addCustomer(@RequestBody Customer customer) {
                return bankingService.saveCustomer(customer);
            }

            @PostMapping("/accounts")
            public Account addAccount(@RequestParam Long customerId, @RequestBody Account account) {
                return bankingService.saveAccount(customerId, account);
            }

            @PostMapping("/deposit")
            public Account deposit(@RequestParam Long accountId, @RequestParam double amount) {
                return bankingService.deposit(accountId, amount);
            }

            @PostMapping("/withdraw")
            public Account withdraw(@RequestParam Long accountId, @RequestParam double amount) {
                return bankingService.withdraw(accountId, amount);
            }
        }
    """)


def banking_web():
    return dedent("""
        package com.assignment.bankingsystem.controller;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.bankingsystem.entity.Account;
        import com.assignment.bankingsystem.entity.Customer;
        import com.assignment.bankingsystem.service.BankingService;

        @Controller
        public class BankingViewController {

            private final BankingService bankingService;

            public BankingViewController(BankingService bankingService) {
                this.bankingService = bankingService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("customers", bankingService.getAllCustomers());
                model.addAttribute("accounts", bankingService.getAllAccounts());
                model.addAttribute("transactions", bankingService.getAllTransactions());
                model.addAttribute("customer", new Customer());
                model.addAttribute("account", new Account());
                return "index";
            }

            @PostMapping("/customers/save")
            public String saveCustomer(Customer customer) {
                bankingService.saveCustomer(customer);
                return "redirect:/";
            }

            @PostMapping("/accounts/save")
            public String saveAccount(@RequestParam Long customerId, Account account) {
                bankingService.saveAccount(customerId, account);
                return "redirect:/";
            }

            @PostMapping("/deposit")
            public String deposit(@RequestParam Long accountId, @RequestParam double amount) {
                bankingService.deposit(accountId, amount);
                return "redirect:/";
            }

            @PostMapping("/withdraw")
            public String withdraw(@RequestParam Long accountId, @RequestParam double amount) {
                bankingService.withdraw(accountId, amount);
                return "redirect:/";
            }
        }
    """)


def banking_loader():
    return dedent("""
        package com.assignment.bankingsystem.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.bankingsystem.entity.Account;
        import com.assignment.bankingsystem.entity.Customer;
        import com.assignment.bankingsystem.repository.AccountRepository;
        import com.assignment.bankingsystem.repository.CustomerRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadBankingData(CustomerRepository customerRepository, AccountRepository accountRepository) {
                return args -> {
                    if (customerRepository.count() == 0) {
                        Customer customer = new Customer();
                        customer.setName("Abhinav");
                        customer.setEmail("abhinav@example.com");
                        customer.setAccounts(new ArrayList<>());
                        customerRepository.save(customer);

                        Account account = new Account();
                        account.setAccountNumber("SB1001");
                        account.setBalance(10000);
                        account.setCustomer(customer);
                        account.setTransactions(new ArrayList<>());
                        accountRepository.save(account);
                    }
                };
            }
        }
    """)


def banking_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Banking System</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">Banking System</h1>
            <div class="row g-4">
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Customer</h5>
                    <form action="/customers/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Customer name" required>
                        <input class="form-control mb-2" name="email" placeholder="Email" required>
                        <button class="btn btn-primary w-100">Save Customer</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Account</h5>
                    <form action="/accounts/save" method="post">
                        <select class="form-select mb-2" name="customerId" required>
                            <option value="">Select customer</option>
                            <option th:each="customer : ${customers}" th:value="${customer.id}" th:text="${customer.name}"></option>
                        </select>
                        <input class="form-control mb-2" name="accountNumber" placeholder="Account number" required>
                        <input class="form-control mb-2" name="balance" type="number" step="0.01" placeholder="Opening balance" required>
                        <button class="btn btn-primary w-100">Save Account</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Transactions</h5>
                    <form action="/deposit" method="post" class="mb-2">
                        <input class="form-control mb-2" name="accountId" placeholder="Account ID" required>
                        <input class="form-control mb-2" name="amount" placeholder="Amount" required>
                        <button class="btn btn-success w-100">Deposit</button>
                    </form>
                    <form action="/withdraw" method="post">
                        <input class="form-control mb-2" name="accountId" placeholder="Account ID" required>
                        <input class="form-control mb-2" name="amount" placeholder="Amount" required>
                        <button class="btn btn-outline-danger w-100">Withdraw</button>
                    </form>
                </div></div></div>
            </div>
            <div class="card shadow-sm mt-4"><div class="card-body">
                <h5>Accounts</h5>
                <table class="table table-bordered">
                    <thead><tr><th>Account Number</th><th>Customer</th><th>Balance</th></tr></thead>
                    <tbody>
                        <tr th:each="account : ${accounts}">
                            <td th:text="${account.accountNumber}"></td>
                            <td th:text="${account.customer.name}"></td>
                            <td th:text="${account.balance}"></td>
                        </tr>
                    </tbody>
                </table>
            </div></div>
        </div>
        </body>
        </html>
    """)


def food_service():
    return dedent("""
        package com.assignment.fooddelivery.service;

        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.fooddelivery.entity.AppUser;
        import com.assignment.fooddelivery.entity.FoodOrder;
        import com.assignment.fooddelivery.entity.Restaurant;
        import com.assignment.fooddelivery.exception.ResourceNotFoundException;
        import com.assignment.fooddelivery.repository.AppUserRepository;
        import com.assignment.fooddelivery.repository.FoodOrderRepository;
        import com.assignment.fooddelivery.repository.RestaurantRepository;

        @Service
        public class FoodDeliveryService {

            private final AppUserRepository appUserRepository;
            private final RestaurantRepository restaurantRepository;
            private final FoodOrderRepository foodOrderRepository;

            public FoodDeliveryService(AppUserRepository appUserRepository, RestaurantRepository restaurantRepository,
                    FoodOrderRepository foodOrderRepository) {
                this.appUserRepository = appUserRepository;
                this.restaurantRepository = restaurantRepository;
                this.foodOrderRepository = foodOrderRepository;
            }

            public List<AppUser> getAllUsers() {
                return appUserRepository.findAll();
            }

            public List<Restaurant> getAllRestaurants() {
                return restaurantRepository.findAll();
            }

            public List<FoodOrder> getAllOrders() {
                return foodOrderRepository.findAll();
            }

            public AppUser saveUser(AppUser user) {
                return appUserRepository.save(user);
            }

            public Restaurant saveRestaurant(Restaurant restaurant) {
                return restaurantRepository.save(restaurant);
            }

            public FoodOrder placeOrder(Long userId, Long restaurantId, String items, double totalAmount) {
                AppUser user = appUserRepository.findById(userId)
                        .orElseThrow(() -> new ResourceNotFoundException("User not found"));
                Restaurant restaurant = restaurantRepository.findById(restaurantId)
                        .orElseThrow(() -> new ResourceNotFoundException("Restaurant not found"));
                FoodOrder order = new FoodOrder();
                order.setUser(user);
                order.setRestaurant(restaurant);
                order.setItems(items);
                order.setTotalAmount(totalAmount);
                return foodOrderRepository.save(order);
            }
        }
    """)


def food_rest():
    return dedent("""
        package com.assignment.fooddelivery.controller;

        import java.util.List;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.fooddelivery.entity.AppUser;
        import com.assignment.fooddelivery.entity.FoodOrder;
        import com.assignment.fooddelivery.entity.Restaurant;
        import com.assignment.fooddelivery.service.FoodDeliveryService;

        @RestController
        @RequestMapping("/api/food")
        public class FoodDeliveryRestController {

            private final FoodDeliveryService foodDeliveryService;

            public FoodDeliveryRestController(FoodDeliveryService foodDeliveryService) {
                this.foodDeliveryService = foodDeliveryService;
            }

            @GetMapping("/users")
            public List<AppUser> getUsers() {
                return foodDeliveryService.getAllUsers();
            }

            @GetMapping("/restaurants")
            public List<Restaurant> getRestaurants() {
                return foodDeliveryService.getAllRestaurants();
            }

            @GetMapping("/orders")
            public List<FoodOrder> getOrders() {
                return foodDeliveryService.getAllOrders();
            }

            @PostMapping("/users")
            public AppUser addUser(@RequestBody AppUser user) {
                return foodDeliveryService.saveUser(user);
            }

            @PostMapping("/restaurants")
            public Restaurant addRestaurant(@RequestBody Restaurant restaurant) {
                return foodDeliveryService.saveRestaurant(restaurant);
            }

            @PostMapping("/orders")
            public FoodOrder placeOrder(@RequestParam Long userId, @RequestParam Long restaurantId,
                    @RequestParam String items, @RequestParam double totalAmount) {
                return foodDeliveryService.placeOrder(userId, restaurantId, items, totalAmount);
            }
        }
    """)


def food_web():
    return dedent("""
        package com.assignment.fooddelivery.controller;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.fooddelivery.entity.AppUser;
        import com.assignment.fooddelivery.entity.Restaurant;
        import com.assignment.fooddelivery.service.FoodDeliveryService;

        @Controller
        public class FoodDeliveryViewController {

            private final FoodDeliveryService foodDeliveryService;

            public FoodDeliveryViewController(FoodDeliveryService foodDeliveryService) {
                this.foodDeliveryService = foodDeliveryService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("users", foodDeliveryService.getAllUsers());
                model.addAttribute("restaurants", foodDeliveryService.getAllRestaurants());
                model.addAttribute("orders", foodDeliveryService.getAllOrders());
                model.addAttribute("user", new AppUser());
                model.addAttribute("restaurant", new Restaurant());
                return "index";
            }

            @PostMapping("/users/save")
            public String saveUser(AppUser user) {
                foodDeliveryService.saveUser(user);
                return "redirect:/";
            }

            @PostMapping("/restaurants/save")
            public String saveRestaurant(Restaurant restaurant) {
                foodDeliveryService.saveRestaurant(restaurant);
                return "redirect:/";
            }

            @PostMapping("/orders/save")
            public String saveOrder(@RequestParam Long userId, @RequestParam Long restaurantId, @RequestParam String items,
                    @RequestParam double totalAmount) {
                foodDeliveryService.placeOrder(userId, restaurantId, items, totalAmount);
                return "redirect:/";
            }
        }
    """)


def food_loader():
    return dedent("""
        package com.assignment.fooddelivery.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.fooddelivery.entity.AppUser;
        import com.assignment.fooddelivery.entity.Restaurant;
        import com.assignment.fooddelivery.repository.AppUserRepository;
        import com.assignment.fooddelivery.repository.RestaurantRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadFoodData(AppUserRepository appUserRepository, RestaurantRepository restaurantRepository) {
                return args -> {
                    if (appUserRepository.count() == 0) {
                        AppUser user = new AppUser();
                        user.setName("Ayush Kumar");
                        user.setAddress("Lake View Road");
                        user.setOrders(new ArrayList<>());
                        appUserRepository.save(user);

                        Restaurant restaurant = new Restaurant();
                        restaurant.setName("Spice Hub");
                        restaurant.setCuisine("Indian");
                        restaurant.setOrders(new ArrayList<>());
                        restaurantRepository.save(restaurant);
                    }
                };
            }
        }
    """)


def food_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Food Delivery System</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">Food Delivery System</h1>
            <div class="row g-4">
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add User</h5>
                    <form action="/users/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="User name" required>
                        <input class="form-control mb-2" name="address" placeholder="Address" required>
                        <button class="btn btn-primary w-100">Save User</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Restaurant</h5>
                    <form action="/restaurants/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Restaurant name" required>
                        <input class="form-control mb-2" name="cuisine" placeholder="Cuisine" required>
                        <button class="btn btn-primary w-100">Save Restaurant</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Place Order</h5>
                    <form action="/orders/save" method="post">
                        <select class="form-select mb-2" name="userId" required>
                            <option value="">Select user</option>
                            <option th:each="user : ${users}" th:value="${user.id}" th:text="${user.name}"></option>
                        </select>
                        <select class="form-select mb-2" name="restaurantId" required>
                            <option value="">Select restaurant</option>
                            <option th:each="restaurant : ${restaurants}" th:value="${restaurant.id}" th:text="${restaurant.name}"></option>
                        </select>
                        <input class="form-control mb-2" name="items" placeholder="Items" required>
                        <input class="form-control mb-2" name="totalAmount" type="number" step="0.01" placeholder="Total amount" required>
                        <button class="btn btn-success w-100">Place Order</button>
                    </form>
                </div></div></div>
            </div>
            <div class="card shadow-sm mt-4"><div class="card-body">
                <h5>Order History</h5>
                <table class="table table-bordered">
                    <thead><tr><th>User</th><th>Restaurant</th><th>Items</th><th>Total</th></tr></thead>
                    <tbody>
                        <tr th:each="order : ${orders}">
                            <td th:text="${order.user.name}"></td>
                            <td th:text="${order.restaurant.name}"></td>
                            <td th:text="${order.items}"></td>
                            <td th:text="${order.totalAmount}"></td>
                        </tr>
                    </tbody>
                </table>
            </div></div>
        </div>
        </body>
        </html>
    """)


def leave_service():
    return dedent("""
        package com.assignment.leavemanagement.service;

        import java.time.LocalDate;
        import java.util.List;

        import org.springframework.stereotype.Service;

        import com.assignment.leavemanagement.entity.Employee;
        import com.assignment.leavemanagement.entity.LeaveRequest;
        import com.assignment.leavemanagement.entity.Manager;
        import com.assignment.leavemanagement.exception.ResourceNotFoundException;
        import com.assignment.leavemanagement.repository.EmployeeRepository;
        import com.assignment.leavemanagement.repository.LeaveRequestRepository;
        import com.assignment.leavemanagement.repository.ManagerRepository;

        @Service
        public class LeaveManagementService {

            private final ManagerRepository managerRepository;
            private final EmployeeRepository employeeRepository;
            private final LeaveRequestRepository leaveRequestRepository;

            public LeaveManagementService(ManagerRepository managerRepository, EmployeeRepository employeeRepository,
                    LeaveRequestRepository leaveRequestRepository) {
                this.managerRepository = managerRepository;
                this.employeeRepository = employeeRepository;
                this.leaveRequestRepository = leaveRequestRepository;
            }

            public List<Manager> getAllManagers() {
                return managerRepository.findAll();
            }

            public List<Employee> getAllEmployees() {
                return employeeRepository.findAll();
            }

            public List<LeaveRequest> getAllRequests() {
                return leaveRequestRepository.findAll();
            }

            public Manager saveManager(Manager manager) {
                return managerRepository.save(manager);
            }

            public Employee saveEmployee(Long managerId, Employee employee) {
                Manager manager = managerRepository.findById(managerId)
                        .orElseThrow(() -> new ResourceNotFoundException("Manager not found"));
                employee.setManager(manager);
                return employeeRepository.save(employee);
            }

            public LeaveRequest applyLeave(Long employeeId, LocalDate fromDate, LocalDate toDate, String reason) {
                Employee employee = employeeRepository.findById(employeeId)
                        .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));
                LeaveRequest request = new LeaveRequest();
                request.setEmployee(employee);
                request.setFromDate(fromDate);
                request.setToDate(toDate);
                request.setReason(reason);
                request.setStatus("PENDING");
                return leaveRequestRepository.save(request);
            }

            public LeaveRequest updateStatus(Long requestId, String status) {
                LeaveRequest request = leaveRequestRepository.findById(requestId)
                        .orElseThrow(() -> new ResourceNotFoundException("Leave request not found"));
                request.setStatus(status);
                return leaveRequestRepository.save(request);
            }
        }
    """)


def leave_rest():
    return dedent("""
        package com.assignment.leavemanagement.controller;

        import java.time.LocalDate;
        import java.util.List;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestBody;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import com.assignment.leavemanagement.entity.Employee;
        import com.assignment.leavemanagement.entity.LeaveRequest;
        import com.assignment.leavemanagement.entity.Manager;
        import com.assignment.leavemanagement.service.LeaveManagementService;

        @RestController
        @RequestMapping("/api/leave")
        public class LeaveManagementRestController {

            private final LeaveManagementService leaveManagementService;

            public LeaveManagementRestController(LeaveManagementService leaveManagementService) {
                this.leaveManagementService = leaveManagementService;
            }

            @GetMapping("/managers")
            public List<Manager> getManagers() {
                return leaveManagementService.getAllManagers();
            }

            @GetMapping("/employees")
            public List<Employee> getEmployees() {
                return leaveManagementService.getAllEmployees();
            }

            @GetMapping("/requests")
            public List<LeaveRequest> getRequests() {
                return leaveManagementService.getAllRequests();
            }

            @PostMapping("/managers")
            public Manager addManager(@RequestBody Manager manager) {
                return leaveManagementService.saveManager(manager);
            }

            @PostMapping("/employees")
            public Employee addEmployee(@RequestParam Long managerId, @RequestBody Employee employee) {
                return leaveManagementService.saveEmployee(managerId, employee);
            }

            @PostMapping("/apply")
            public LeaveRequest applyLeave(@RequestParam Long employeeId, @RequestParam String fromDate,
                    @RequestParam String toDate, @RequestParam String reason) {
                return leaveManagementService.applyLeave(employeeId, LocalDate.parse(fromDate), LocalDate.parse(toDate), reason);
            }

            @PostMapping("/update-status")
            public LeaveRequest updateStatus(@RequestParam Long requestId, @RequestParam String status) {
                return leaveManagementService.updateStatus(requestId, status);
            }
        }
    """)


def leave_web():
    return dedent("""
        package com.assignment.leavemanagement.controller;

        import java.time.LocalDate;

        import org.springframework.stereotype.Controller;
        import org.springframework.ui.Model;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.PostMapping;
        import org.springframework.web.bind.annotation.RequestParam;

        import com.assignment.leavemanagement.entity.Employee;
        import com.assignment.leavemanagement.entity.Manager;
        import com.assignment.leavemanagement.service.LeaveManagementService;

        @Controller
        public class LeaveManagementViewController {

            private final LeaveManagementService leaveManagementService;

            public LeaveManagementViewController(LeaveManagementService leaveManagementService) {
                this.leaveManagementService = leaveManagementService;
            }

            @GetMapping("/")
            public String home(Model model) {
                model.addAttribute("managers", leaveManagementService.getAllManagers());
                model.addAttribute("employees", leaveManagementService.getAllEmployees());
                model.addAttribute("requests", leaveManagementService.getAllRequests());
                model.addAttribute("manager", new Manager());
                model.addAttribute("employee", new Employee());
                return "index";
            }

            @PostMapping("/managers/save")
            public String saveManager(Manager manager) {
                leaveManagementService.saveManager(manager);
                return "redirect:/";
            }

            @PostMapping("/employees/save")
            public String saveEmployee(@RequestParam Long managerId, Employee employee) {
                leaveManagementService.saveEmployee(managerId, employee);
                return "redirect:/";
            }

            @PostMapping("/leave/apply")
            public String applyLeave(@RequestParam Long employeeId, @RequestParam String fromDate, @RequestParam String toDate,
                    @RequestParam String reason) {
                leaveManagementService.applyLeave(employeeId, LocalDate.parse(fromDate), LocalDate.parse(toDate), reason);
                return "redirect:/";
            }

            @PostMapping("/leave/status")
            public String updateStatus(@RequestParam Long requestId, @RequestParam String status) {
                leaveManagementService.updateStatus(requestId, status);
                return "redirect:/";
            }
        }
    """)


def leave_loader():
    return dedent("""
        package com.assignment.leavemanagement.config;

        import java.util.ArrayList;

        import org.springframework.boot.CommandLineRunner;
        import org.springframework.context.annotation.Bean;
        import org.springframework.context.annotation.Configuration;

        import com.assignment.leavemanagement.entity.Employee;
        import com.assignment.leavemanagement.entity.Manager;
        import com.assignment.leavemanagement.repository.EmployeeRepository;
        import com.assignment.leavemanagement.repository.ManagerRepository;

        @Configuration
        public class DataLoader {

            @Bean
            CommandLineRunner loadLeaveData(ManagerRepository managerRepository, EmployeeRepository employeeRepository) {
                return args -> {
                    if (managerRepository.count() == 0) {
                        Manager manager = new Manager();
                        manager.setName("Priyanshu Sharma");
                        manager.setDepartment("HR");
                        manager.setEmployees(new ArrayList<>());
                        managerRepository.save(manager);

                        Employee employee = new Employee();
                        employee.setName("Rakshit Pandey");
                        employee.setDesignation("Developer");
                        employee.setManager(manager);
                        employee.setLeaveRequests(new ArrayList<>());
                        employeeRepository.save(employee);
                    }
                };
            }
        }
    """)


def leave_template():
    return dedent("""
        <!DOCTYPE html>
        <html lang="en" xmlns:th="http://www.thymeleaf.org">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Employee Leave Management</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">Employee Leave Management</h1>
            <div class="row g-4">
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Manager</h5>
                    <form action="/managers/save" method="post">
                        <input class="form-control mb-2" name="name" placeholder="Manager name" required>
                        <input class="form-control mb-2" name="department" placeholder="Department" required>
                        <button class="btn btn-primary w-100">Save Manager</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Add Employee</h5>
                    <form action="/employees/save" method="post">
                        <select class="form-select mb-2" name="managerId" required>
                            <option value="">Select manager</option>
                            <option th:each="manager : ${managers}" th:value="${manager.id}" th:text="${manager.name}"></option>
                        </select>
                        <input class="form-control mb-2" name="name" placeholder="Employee name" required>
                        <input class="form-control mb-2" name="designation" placeholder="Designation" required>
                        <button class="btn btn-primary w-100">Save Employee</button>
                    </form>
                </div></div></div>
                <div class="col-md-4"><div class="card shadow-sm"><div class="card-body">
                    <h5>Apply Leave</h5>
                    <form action="/leave/apply" method="post">
                        <select class="form-select mb-2" name="employeeId" required>
                            <option value="">Select employee</option>
                            <option th:each="employee : ${employees}" th:value="${employee.id}" th:text="${employee.name}"></option>
                        </select>
                        <input class="form-control mb-2" type="date" name="fromDate" required>
                        <input class="form-control mb-2" type="date" name="toDate" required>
                        <input class="form-control mb-2" name="reason" placeholder="Reason" required>
                        <button class="btn btn-success w-100">Apply</button>
                    </form>
                </div></div></div>
            </div>
            <div class="card shadow-sm mt-4"><div class="card-body">
                <h5>Leave Requests</h5>
                <table class="table table-bordered">
                    <thead><tr><th>Employee</th><th>From</th><th>To</th><th>Status</th><th>Action</th></tr></thead>
                    <tbody>
                        <tr th:each="request : ${requests}">
                            <td th:text="${request.employee.name}"></td>
                            <td th:text="${request.fromDate}"></td>
                            <td th:text="${request.toDate}"></td>
                            <td th:text="${request.status}"></td>
                            <td>
                                <form action="/leave/status" method="post" class="d-flex gap-2">
                                    <input type="hidden" name="requestId" th:value="${request.id}">
                                    <select class="form-select" name="status">
                                        <option>APPROVED</option>
                                        <option>REJECTED</option>
                                    </select>
                                    <button class="btn btn-outline-secondary">Update</button>
                                </form>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div></div>
        </div>
        </body>
        </html>
    """)


if __name__ == "__main__":
    generate()
