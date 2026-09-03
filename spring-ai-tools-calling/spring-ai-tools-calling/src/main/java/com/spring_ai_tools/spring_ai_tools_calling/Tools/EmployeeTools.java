package com.spring_ai_tools.spring_ai_tools_calling.Tools;

import com.spring_ai_tools.spring_ai_tools_calling.entity.Employee;
import com.spring_ai_tools.spring_ai_tools_calling.repository.EmployeeRepository;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

@Component
public class EmployeeTools {
    private final EmployeeRepository employeeRepository;

    public EmployeeTools(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;

    }

    // Private helper — formats list to readable string for LLM
    private String formatList(List<Employee> employees) {
        return employees.stream()
                .map(e -> String.format(
                        "ID: %d | Name: %s | Dept: %s | Salary: %.0f | City: %s",
                        e.getId(), e.getName(), e.getDepartment(), e.getSalary(), e.getCity()))
                .collect(Collectors.joining("\n"));
    }

    // Tool 1 — Get all employees
    @Tool(description = "Returns the list of all employees in the company " +
            "with their name, department, salary and city")
    public String getAllEmployees() {
        List<Employee> employees = employeeRepository.findAll();
        return formatList(employees);
    }

    // Tool 2 — Get employees by department
    @Tool(description = "Returns all employees belonging to a specific department. " +
            "Use this when user asks about employees in HR, Engineering, Finance etc.")
    public String getEmployeesByDepartment(
            @ToolParam(description = "Department name like HR, Engineering, Finance, Marketing")
            String department) {

        List<Employee> employees = employeeRepository.findByDepartmentIgnoreCase(department);

        if (employees.isEmpty()) {
            return "No employees found in department: " + department;
        }
        return formatList(employees);
    }

    // Tool 3 — Get employees by salary threshold
    @Tool(description = "Returns all employees whose salary is greater than the given amount. " +
            "Use when user asks who earns more than X amount.")
    public String getEmployeesWithSalaryGreaterThan(
            @ToolParam(description = "Minimum salary amount as a number, e.g. 70000")
            Double salary) {

        List<Employee> employees = employeeRepository.findBySalaryGreaterThan(salary);

        if (employees.isEmpty()) {
            return "No employees found with salary greater than " + salary;
        }
        return formatList(employees);
    }
    // Tool 4 — Count employees in a department
    @Tool(description = "Returns the total count of employees in a given department. " +
            "Use this when user asks how many employees are in a department.")
    public String countEmployeesInDepartment(
            @ToolParam(description = "Department name like HR, Engineering, Finance, Marketing")
            String department) {

        long count = employeeRepository.countByDepartmentIgnoreCase(department);
        return "Total employees in " + department + " department: " + count;
    }

    // Tool 5 — Get employees by city
    @Tool(description = "Returns all employees located in a specific city. " +
            "Use when user asks about employees in Bangalore, Mumbai, Delhi etc.")
    public String getEmployeesByCity(
            @ToolParam(description = "City name like Bangalore, Mumbai, Pune, Delhi, Chennai")
            String city) {

        List<Employee> employees = employeeRepository.findByCityIgnoreCase(city);

        if (employees.isEmpty()) {
            return "No employees found in city: " + city;
        }
        return formatList(employees);
    }

    @Tool(description = "Returns employee details by their ID number. " +
            "Use when user asks about a specific employee by their ID.")
    public String getEmployeeById(
            @ToolParam(description = "Numeric employee ID") Long id) {

        if (id <= 0) {
            throw new IllegalArgumentException("Employee ID must be a positive number");
        }

        return employeeRepository.findById(id)
                .map(e -> String.format(
                        "Name: %s | Dept: %s | Salary: %.0f | City: %s",
                        e.getName(), e.getDepartment(), e.getSalary(), e.getCity()))
                .orElseThrow(() -> new RuntimeException(
                        "No employee exists with ID: " + id));
    }

}
