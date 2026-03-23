package com.assignment.fooddelivery.entity;

        import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.ArrayList;
import java.util.List;

        @Entity
        public class AppUser {

        @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private String address;

    @JsonIgnore
@OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<FoodOrder> orders = new ArrayList<>();

            public AppUser() {
            }

            public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public List<FoodOrder> getOrders() {
        return orders;
    }

    public void setOrders(List<FoodOrder> orders) {
        this.orders = orders;
    }
        }
