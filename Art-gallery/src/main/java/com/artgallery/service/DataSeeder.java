package com.artgallery.service;

import com.artgallery.entity.Artist;
import com.artgallery.entity.Role;
import com.artgallery.repository.ArtistRepository;
import com.artgallery.repository.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataSeeder implements CommandLineRunner {

    private final UserService userService;
    private final UserRepository userRepository;
    private final ArtistRepository artistRepository;

    public DataSeeder(UserService userService, UserRepository userRepository, ArtistRepository artistRepository) {
        this.userService = userService;
        this.userRepository = userRepository;
        this.artistRepository = artistRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        if (userRepository.count() == 0) {
            userService.registerUser("System Admin", "admin@gallery.com", "admin123", Role.ADMIN);
            System.out.println("Default Admin seeded: admin@gallery.com / admin123");
        }
        
        if (artistRepository.count() == 0) {
            Artist a1 = new Artist();
            a1.setName("Leonardo da Vinci");
            a1.setBio("Italian polymath of the High Renaissance.");
            artistRepository.save(a1);

            Artist a2 = new Artist();
            a2.setName("Vincent van Gogh");
            a2.setBio("Dutch Post-Impressionist painter.");
            artistRepository.save(a2);
            
            System.out.println("Default Artists seeded.");
        }
    }
}
