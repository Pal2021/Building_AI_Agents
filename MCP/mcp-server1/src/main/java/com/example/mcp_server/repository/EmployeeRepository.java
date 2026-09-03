package com.example.mcp_server.repository;


import com.example.mcp_server.Employee.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    List<Employee> findByDepartmentIgnoreCase(String department);
    List<Employee> findBySalaryGreaterThan(Double salary);
    List<Employee> findByCityIgnoreCase(String city);
    long countByDepartmentIgnoreCase(String department);
}
