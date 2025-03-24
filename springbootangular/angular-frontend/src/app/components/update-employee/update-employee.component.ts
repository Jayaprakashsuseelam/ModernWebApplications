import { Component, OnInit } from '@angular/core';
import { Employee } from '../../models/employee';
import { EmployeeService } from '../../services/employee.service';
import { Router, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-update-employee',
  templateUrl: './update-employee.component.html',
  styleUrls: ['./update-employee.component.css'],
  standalone: true,
  imports: [FormsModule]
})
export class UpdateEmployeeComponent implements OnInit {
  id: number = 0;
  employee: Employee = new Employee();

  constructor(private employeeService: EmployeeService,
              private router: Router,
              private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.params['id'];
    this.employeeService.getEmployee(this.id).subscribe((data: Employee) => {
      this.employee = data;
    }, (error: any) => console.log(error));
  }

  onSubmit() {
    this.employeeService.updateEmployee(this.id, this.employee).subscribe((data: Object) => {
      this.goToEmployeeList();
    }, (error: any) => console.log(error));
  }

  goToEmployeeList() {
    this.router.navigate(['/employees']);
  }
}
