package com.example.mcp_server.tools;

import com.example.mcp_server.Employee.Employee;
import com.example.mcp_server.repository.EmployeeRepository;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class EmployeeTools {

    private final EmployeeRepository employeeRepository;

    public EmployeeTools(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
    }

    @Tool(description = "Returns the list of all employees with name, department, salary and city")
    public String getAllEmployees() {
        return formatList(employeeRepository.findAll());
    }

    @Tool(description = "Returns all employees in a specific department. Use when user asks about employees in HR, Engineering, Finance etc.")
    public String getEmployeesByDepartment(
            @ToolParam(description = "Department name like HR, Engineering, Finance, Marketing")
            String department) {
        List<Employee> list = employeeRepository.findByDepartmentIgnoreCase(department);
        return list.isEmpty() ? "No employees found in: " + department : formatList(list);
    }

    @Tool(description = "Returns the employee with the highest salary. Use when user asks who earns the most or who is highest paid.")
    public String getHighestPaidEmployee() {
        return employeeRepository.findAll().stream()
                .max(Comparator.comparingDouble(Employee::getSalary))
                .map(this::format)
                .orElse("No employees found");
    }

    @Tool(description = "Returns the employee with the lowest salary. Use when user asks who earns the least or who is lowest paid.")
    public String getLowestPaidEmployee() {
        return employeeRepository.findAll().stream()
                .min(Comparator.comparingDouble(Employee::getSalary))
                .map(this::format)
                .orElse("No employees found");
    }

    @Tool(description = "Returns total count of employees in a department. Use when user asks how many employees are in a department.")
    public String countEmployeesInDepartment(
            @ToolParam(description = "Department name like HR, Engineering, Finance")
            String department) {
        long count = employeeRepository.countByDepartmentIgnoreCase(department);
        return "Total employees in " + department + ": " + count;
    }

    @Tool(description = "Returns average salary of employees in a department. Use when user asks about average pay in a department.")
    public String getAverageSalaryByDepartment(
            @ToolParam(description = "Department name like HR, Engineering, Finance")
            String department) {
        List<Employee> list = employeeRepository.findByDepartmentIgnoreCase(department);
        if (list.isEmpty()) return "No employees found in: " + department;
        double avg = list.stream().mapToDouble(Employee::getSalary).average().orElse(0);
        return String.format("Average salary in %s: %.0f", department, avg);
    }

    @Tool(description = "Returns employees earning more than a given salary. Use when user asks who earns more than X amount.")
    public String getEmployeesWithSalaryGreaterThan(
            @ToolParam(description = "Minimum salary amount as a number e.g. 70000")
            Double salary) {
        List<Employee> list = employeeRepository.findBySalaryGreaterThan(salary);
        return list.isEmpty() ? "No employees found with salary > " + salary : formatList(list);
    }

    @Tool(description = "Returns top N highest paid employees. Use when user asks for top 3 or top 5 highest paid.")
    public String getTopNHighestPaidEmployees(
            @ToolParam(description = "Number of top employees to return e.g. 3 or 5")
            int count) {
        List<Employee> top = employeeRepository.findAll().stream()
                .sorted(Comparator.comparingDouble(Employee::getSalary).reversed())
                .limit(count)
                .collect(Collectors.toList());
        return top.isEmpty() ? "No employees found" :
                "Top " + count + " highest paid:\n" + formatList(top);
    }

    @Tool(description = "Returns all employees in a specific city. Use when user asks about employees in Bangalore, Mumbai, Delhi etc.")
    public String getEmployeesByCity(
            @ToolParam(description = "City name like Bangalore, Mumbai, Pune, Delhi")
            String city) {
        List<Employee> list = employeeRepository.findByCityIgnoreCase(city);
        return list.isEmpty() ? "No employees found in: " + city : formatList(list);
    }

    private String formatList(List<Employee> employees) {
        return employees.stream()
                .map(this::format)
                .collect(Collectors.joining("\n"));
    }

    private String format(Employee e) {
        return String.format("ID: %d | Name: %s | Dept: %s | Salary: %.0f | City: %s",
                e.getId(), e.getName(), e.getDepartment(), e.getSalary(), e.getCity());
    }
}