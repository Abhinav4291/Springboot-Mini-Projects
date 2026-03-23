package com.assignment.fooddelivery.controller;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

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
    public String home(@RequestParam(value = "restaurantFilter", required = false) Long restaurantFilter, Model model) {
        model.addAttribute("users", foodDeliveryService.getAllUsers());
        model.addAttribute("restaurants", foodDeliveryService.getAllRestaurants());
        model.addAttribute("orders", restaurantFilter == null
                ? foodDeliveryService.getAllOrders()
                : foodDeliveryService.getOrdersByRestaurant(restaurantFilter));
        model.addAttribute("restaurantMenus", foodDeliveryService.getRestaurantMenus());
        model.addAttribute("restaurantFilter", restaurantFilter);
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
    public String saveOrder(@RequestParam("userId") Long userId,
            @RequestParam("restaurantId") Long restaurantId,
            @RequestParam("menuItem") List<String> menuItems,
            @RequestParam("quantity") List<Integer> quantities,
            RedirectAttributes redirectAttributes) {
        try {
            foodDeliveryService.placeOrder(userId, restaurantId, menuItems, quantities);
            redirectAttributes.addFlashAttribute("successMessage", "Food order placed successfully.");
        } catch (Exception exception) {
            redirectAttributes.addFlashAttribute("errorMessage", exception.getMessage());
        }
        return "redirect:/";
    }
}
