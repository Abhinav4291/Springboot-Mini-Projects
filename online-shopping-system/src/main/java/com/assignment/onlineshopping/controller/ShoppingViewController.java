package com.assignment.onlineshopping.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.assignment.onlineshopping.entity.Customer;
import com.assignment.onlineshopping.entity.CustomerOrder;
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
        model.addAttribute("orderRows", buildOrderRows(shoppingService.getAllOrders()));
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
    public String saveOrder(@RequestParam("customerId") Long customerId,
            @RequestParam("productId") Long productId,
            @RequestParam("quantity") int quantity,
            RedirectAttributes redirectAttributes) {
        try {
            shoppingService.placeOrder(customerId, productId, quantity);
            redirectAttributes.addFlashAttribute("successMessage", "Order placed successfully.");
        } catch (Exception exception) {
            redirectAttributes.addFlashAttribute("errorMessage", exception.getMessage());
        }
        return "redirect:/";
    }

    private List<Map<String, Object>> buildOrderRows(List<CustomerOrder> orders) {
        List<Map<String, Object>> rows = new ArrayList<>();
        for (CustomerOrder order : orders) {
            Map<String, Object> row = new HashMap<>();
            row.put("customerName", order.getCustomer() != null ? order.getCustomer().getName() : "N/A");
            String productName = "N/A";
            double productPrice = 0;
            if (order.getProducts() != null && !order.getProducts().isEmpty()) {
                Product firstProduct = order.getProducts().get(0);
                productName = firstProduct.getName();
                productPrice = firstProduct.getPrice();
            }
            row.put("productName", productName);

            int quantity = order.getQuantity();
            if (quantity <= 0 && productPrice > 0) {
                quantity = (int) Math.round(order.getTotalAmount() / productPrice);
            }
            row.put("quantity", quantity);
            row.put("totalAmount", order.getTotalAmount());
            rows.add(row);
        }
        return rows;
    }
}
