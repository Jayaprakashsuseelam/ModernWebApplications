import { Component, OnInit } from '@angular/core';
import { Department } from '../../models/department';
import { DepartmentService } from '../../services/department.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-create-department',
  templateUrl: './create-department.component.html',
  styleUrls: ['./create-department.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class CreateDepartmentComponent implements OnInit {

  department: Department = new Department();

  constructor(private departmentService: DepartmentService,
              private router: Router) { }

  ngOnInit(): void {
  }

  saveDepartment() {
    this.departmentService.createDepartment(this.department).subscribe(data => {
      console.log(data);
      this.goToDepartmentList();
    },
    error => console.log(error));
  }

  goToDepartmentList() {
    this.router.navigate(['/departments']);
  }

  onSubmit() {
    console.log(this.department);
    this.saveDepartment();
  }
} 