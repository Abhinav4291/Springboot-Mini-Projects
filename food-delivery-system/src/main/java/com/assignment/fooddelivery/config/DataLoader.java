package com.assignment.fooddelivery.config;

import java.util.ArrayList;
import java.util.List;

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
                AppUser user1 = new AppUser();
                user1.setName("Ayush Kumar");
                user1.setAddress("Lake View Road");
                user1.setOrders(new ArrayList<>());
                appUserRepository.save(user1);

                AppUser user2 = new AppUser();
                user2.setName("Abhinav");
                user2.setAddress("Central Avenue");
                user2.setOrders(new ArrayList<>());
                appUserRepository.save(user2);
            }

            if (restaurantRepository.count() == 0) {
                saveRestaurant(restaurantRepository, "Spice Hub", "North Indian", getSpiceHubMenu());
                saveRestaurant(restaurantRepository, "KFC", "Fried Chicken", getKfcMenu());
                saveRestaurant(restaurantRepository, "Bowl Story", "Asian", getBowlStoryMenu());
            } else {
                List<Restaurant> restaurants = restaurantRepository.findAll();
                for (Restaurant restaurant : restaurants) {
                    if ("Spice Hub".equalsIgnoreCase(restaurant.getName())) {
                        restaurant.setCuisine("North Indian");
                        restaurant.setMenuItems(getSpiceHubMenu());
                    } else if ("KFC".equalsIgnoreCase(restaurant.getName())) {
                        restaurant.setCuisine("Fried Chicken");
                        restaurant.setMenuItems(getKfcMenu());
                    } else if ("Pizza Town".equalsIgnoreCase(restaurant.getName())) {
                        restaurant.setCuisine("Italian");
                        restaurant.setMenuItems(getPizzaTownMenu());
                    } else if ("Bowl Story".equalsIgnoreCase(restaurant.getName())) {
                        restaurant.setCuisine("Asian");
                        restaurant.setMenuItems(getBowlStoryMenu());
                    } else {
                        restaurant.setMenuItems(getSpiceHubMenu());
                    }
                    restaurantRepository.save(restaurant);
                }
            }
        };
    }

    private void saveRestaurant(RestaurantRepository restaurantRepository, String name, String cuisine, String menuItems) {
        Restaurant restaurant = new Restaurant();
        restaurant.setName(name);
        restaurant.setCuisine(cuisine);
        restaurant.setMenuItems(menuItems);
        restaurant.setOrders(new ArrayList<>());
        restaurantRepository.save(restaurant);
    }

    private String getSpiceHubMenu() {
        return "Paneer Butter Masala:260|Butter Naan:45|Veg Biryani:220|Dal Makhani:240|Shahi Paneer:255|Tandoori Roti:25|Jeera Rice:150|Malai Kofta:265|Chole Bhature:180|Aloo Paratha:90";
    }

    private String getKfcMenu() {
        return "Hot Crispy Chicken:249|Chicken Bucket:599|Zinger Burger:219|Chicken Popcorn:199|Chicken Strips:229|Veg Zinger Burger:179|French Fries:119|Chicken Rice Bowl:189|Smoky Grilled Chicken:279|Pepsi Can:60";
    }

    private String getPizzaTownMenu() {
        return "Margherita Pizza:299|Farmhouse Pizza:399|Garlic Bread:149|Veggie Supreme Pizza:429|Cheese Burst Pizza:469|Paneer Tikka Pizza:449|Classic Corn Pizza:279|White Sauce Pasta:239|Potato Wedges:129|Choco Lava Cake:109";
    }

    private String getBowlStoryMenu() {
        return "Veg Noodles:189|Fried Rice:199|Chilli Paneer:229|Schezwan Noodles:209|Hakka Noodles:199|Manchurian Gravy:219|Spring Rolls:169|Thai Green Curry Bowl:259|Dim Sums:249|Teriyaki Rice Bowl:269";
    }
}
