import { Component, OnInit } from '@angular/core';
import { Employee } from '../../models/employee';
import { EmployeeService } from '../../services/employee.service';
import { Router } from '@angular/router';
import { NgFor } from '@angular/common';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-employee-list',
  templateUrl: './employee-list.component.html',
  styleUrls: ['./employee-list.component.css'],
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive]
})
export class EmployeeListComponent implements OnInit {

  employees: Employee[] = [];

  constructor(private employeeService: EmployeeService,
              private router: Router) { }

  ngOnInit(): void {
    this.getEmployees();
  }

  private getEmployees() {
    this.employeeService.getEmployeesList().subscribe(data => {
      this.employees = data;
    });
  }

  updateEmployee(id: number) {
    this.router.navigate(['update-employee', id]);
  }

  deleteEmployee(id: number) {
    this.employeeService.deleteEmployee(id).subscribe(data => {
      console.log(data);
      this.getEmployees();
    });
  }

  employeeDetails(id: number) {
    this.router.navigate(['employee-details', id]);
  }

  addEmployee() {
    this.router.navigate(['create-employee']);
  }
}
