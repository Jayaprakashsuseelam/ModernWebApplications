import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Department } from '../models/department';

@Injectable({
  providedIn: 'root'
})
export class DepartmentService {

  private baseUrl = 'http://localhost:8030/api/v1/departments';

  constructor(private http: HttpClient) { }

  getDepartmentsList(): Observable<Department[]> {
    return this.http.get<Department[]>(this.baseUrl);
  }

  getDepartment(id: number): Observable<Department> {
    return this.http.get<Department>(`${this.baseUrl}/${id}`);
  }

  createDepartment(department: Department): Observable<Object> {
    return this.http.post(this.baseUrl, department);
  }

  updateDepartment(id: number, department: Department): Observable<Object> {
    return this.http.put(`${this.baseUrl}/${id}`, department);
  }

  deleteDepartment(id: number): Observable<Object> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }
} 