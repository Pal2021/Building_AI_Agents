package com.spring_ai_tools.spring_ai_tools_calling.repository;


import com.spring_ai_tools.spring_ai_tools_calling.entity.Employee;
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