package com.example.springbootangular.repository;

import com.example.springbootangular.model.Department;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DepartmentRepository extends JpaRepository<Department, Long> {
    // Spring Data JPA provides all basic CRUD operations
} 