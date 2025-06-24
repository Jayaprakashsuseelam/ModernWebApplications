import { Routes } from '@angular/router';
import { EmployeeListComponent } from './components/employee-list/employee-list.component';
import { CreateEmployeeComponent } from './components/create-employee/create-employee.component';
import { UpdateEmployeeComponent } from './components/update-employee/update-employee.component';
import { EmployeeDetailsComponent } from './components/employee-details/employee-details.component';
import { DepartmentListComponent } from './components/department-list/department-list.component';
import { CreateDepartmentComponent } from './components/create-department/create-department.component';
import { UpdateDepartmentComponent } from './components/update-department/update-department.component';
import { DepartmentDetailsComponent } from './components/department-details/department-details.component';

export const routes: Routes = [
  { path: '', redirectTo: 'employees', pathMatch: 'full' },
  { path: 'employees', component: EmployeeListComponent },
  { path: 'create-employee', component: CreateEmployeeComponent },
  { path: 'update-employee/:id', component: UpdateEmployeeComponent },
  { path: 'employee-details/:id', component: EmployeeDetailsComponent },
  { path: 'departments', component: DepartmentListComponent },
  { path: 'create-department', component: CreateDepartmentComponent },
  { path: 'update-department/:id', component: UpdateDepartmentComponent },
  { path: 'department-details/:id', component: DepartmentDetailsComponent }
];

