import { Component, OnInit } from '@angular/core';
import { Department } from '../../models/department';
import { DepartmentService } from '../../services/department.service';
import { Router, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-department-details',
  templateUrl: './department-details.component.html',
  styleUrls: ['./department-details.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class DepartmentDetailsComponent implements OnInit {

  id: number = 0;
  department: Department = new Department();

  constructor(private departmentService: DepartmentService,
              private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.params['id'];
    this.department = new Department();
    this.departmentService.getDepartment(this.id).subscribe(data => {
      this.department = data;
    });
  }

  goToDepartmentList() {
    this.router.navigate(['/departments']);
  }
} 