import { Component, OnInit } from '@angular/core';
import { Department } from '../../models/department';
import { DepartmentService } from '../../services/department.service';
import { Router, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-update-department',
  templateUrl: './update-department.component.html',
  styleUrls: ['./update-department.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class UpdateDepartmentComponent implements OnInit {

  id: number = 0;
  department: Department = new Department();

  constructor(private departmentService: DepartmentService,
              private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.params['id'];
    this.departmentService.getDepartment(this.id).subscribe(data => {
      this.department = data;
    }, error => console.log(error));
  }

  onSubmit() {
    this.departmentService.updateDepartment(this.id, this.department).subscribe(data => {
      this.goToDepartmentList();
    }, error => console.log(error));
  }

  goToDepartmentList() {
    this.router.navigate(['/departments']);
  }
} 