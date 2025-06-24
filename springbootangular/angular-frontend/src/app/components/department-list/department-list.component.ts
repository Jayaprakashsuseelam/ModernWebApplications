import { Component, OnInit } from '@angular/core';
import { Department } from '../../models/department';
import { DepartmentService } from '../../services/department.service';
import { Router } from '@angular/router';
import { NgFor } from '@angular/common';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-department-list',
  templateUrl: './department-list.component.html',
  styleUrls: ['./department-list.component.css'],
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive]
})
export class DepartmentListComponent implements OnInit {

  departments: Department[] = [];

  constructor(private departmentService: DepartmentService,
              private router: Router) { }

  ngOnInit(): void {
    this.getDepartments();
  }

  private getDepartments() {
    this.departmentService.getDepartmentsList().subscribe(data => {
      this.departments = data;
    });
  }

  updateDepartment(id: number) {
    this.router.navigate(['update-department', id]);
  }

  deleteDepartment(id: number) {
    this.departmentService.deleteDepartment(id).subscribe(data => {
      console.log(data);
      this.getDepartments();
    });
  }

  departmentDetails(id: number) {
    this.router.navigate(['department-details', id]);
  }

  addDepartment() {
    this.router.navigate(['create-department']);
  }
} 