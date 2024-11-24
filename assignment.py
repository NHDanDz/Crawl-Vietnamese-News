from datetime import datetime
from typing import List, Optional

class Person:
    def __init__(self, id: str, name: str, dob: datetime, address: str, 
                 phone: str, email: str, position: str):
        self.id = id
        self.name = name
        self.dob = dob
        self.address = address
        self.phone = phone
        self.email = email
        self.position = position

    def __str__(self):
        return f"ID: {self.id}\nHọ tên: {self.name}\nNgày sinh: {self.dob.strftime('%d/%m/%Y')}\n" \
            f"Địa chỉ: {self.address}\nSĐT: {self.phone}\nEmail: {self.email}\nVị trí: {self.position}"

class Employee(Person):
    def __init__(self, id: str, name: str, dob: datetime, address: str,
                 phone: str, email: str, position: str, department: str):
        super().__init__(id, name, dob, address, phone, email, position)
        self.department = department
        self.projects = []

    def __str__(self):
        return super().__str__() + f"\nPhòng ban: {self.department}\n" \
            f"Dự án tham gia: {len(self.projects)}"

class Candidate(Person):
    def __init__(self, id: str, name: str, dob: datetime, address: str,
                 phone: str, email: str, position: str):
        super().__init__(id, name, dob, address, phone, email, position)
        self.status = "New"
        self.interview_notes = []

    def __str__(self):
        return super().__str__() + f"\nTrạng thái: {self.status}"

    def convert_to_employee(self, department: str) -> Employee:
        emp_id = f"EMP{self.id[4:]}"
        return Employee(
            id=emp_id,
            name=self.name,
            dob=self.dob,
            address=self.address,
            phone=self.phone,
            email=self.email,
            position=self.position,
            department=department
        )

class Project:
    def __init__(self, proj_id: str, name: str, location: str, 
                 start_date: datetime, end_date: datetime):
        self.proj_id = proj_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.status = "New"
        self.employees = []

    def __str__(self):
        return f"Mã dự án: {self.proj_id}\nTên dự án: {self.name}\n" \
            f"Địa điểm: {self.location}\nBắt đầu: {self.start_date.strftime('%d/%m/%Y')}\n" \
            f"Kết thúc: {self.end_date.strftime('%d/%m/%Y')}\n" \
            f"Trạng thái: {self.status}\nSố nhân viên: {len(self.employees)}"

class Department:
    def __init__(self, dept_id: str, name: str, manager: Employee = None):
        self.dept_id = dept_id
        self.name = name
        self.manager = manager
        self.employees = []

    def __str__(self):
        return f"Mã phòng: {self.dept_id}\nTên phòng: {self.name}\n" \
            f"Trưởng phòng: {self.manager.name if self.manager else 'Chưa có'}\n" \
            f"Số nhân viên: {len(self.employees)}"

class Benefit:
    def __init__(self, benefit_id: str, name: str, value: float, 
                 start_date: datetime, end_date: datetime):
        self.benefit_id = benefit_id
        self.name = name
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
        self.eligible_employees = []

    def __str__(self):
        return f"Mã phúc lợi: {self.benefit_id}\nTên phúc lợi: {self.name}\n" \
            f"Giá trị: {self.value}\nThời gian: {self.start_date.strftime('%d/%m/%Y')} - " \
            f"{self.end_date.strftime('%d/%m/%Y')}\n" \
            f"Số người hưởng: {len(self.eligible_employees)}"

class HRManagementSystem:
    def __init__(self):
        self.employees = {}
        self.candidates = {}
        self.projects = {}
        self.departments = {}
        self.benefits = {}

    def add_employee(self, employee: Employee):
        if employee.id in self.employees:
            return False
        self.employees[employee.id] = employee
        return True

    def remove_employee(self, emp_id: str):
        if emp_id not in self.employees:
            return False
        del self.employees[emp_id]
        return True

    def update_employee(self, emp_id: str, **kwargs):
        if emp_id not in self.employees:
            return False
        employee = self.employees[emp_id]
        for key, value in kwargs.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        return True

    def search_employees(self, **criteria):
        results = []
        for employee in self.employees.values():
            matches = True
            for key, value in criteria.items():
                if hasattr(employee, key):
                    if getattr(employee, key) != value:
                        matches = False
                        break
            if matches:
                results.append(employee)
        return results

    def add_candidate(self, candidate: Candidate):
        if candidate.id in self.candidates:
            return False
        self.candidates[candidate.id] = candidate
        return True

    def process_candidate(self, candidate: Candidate, status: str, department: str = ""):
        if candidate.id not in self.candidates:
            return False
        candidate.status = status
        if status == "Hired":
            new_employee = candidate.convert_to_employee(department)
            self.add_employee(new_employee)
        return True

    def add_project(self, project: Project):
        if project.proj_id in self.projects:
            return False
        self.projects[project.proj_id] = project
        return True

    def update_project_status(self, proj_id: str, status: str):
        if proj_id not in self.projects:
            return False
        self.projects[proj_id].status = status
        return True

    def assign_to_project(self, emp_id: str, proj_id: str):
        if emp_id not in self.employees or proj_id not in self.projects:
            return False
        employee = self.employees[emp_id]
        project = self.projects[proj_id]
        
        if project not in employee.projects:
            employee.projects.append(project)
        if employee not in project.employees:
            project.employees.append(employee)
        return True

    def add_department(self, department: Department):
        if department.dept_id in self.departments:
            return False
        self.departments[department.dept_id] = department
        return True

    def assign_department_manager(self, dept_id: str, emp_id: str):
        if dept_id not in self.departments or emp_id not in self.employees:
            return False
        self.departments[dept_id].manager = self.employees[emp_id]
        return True

    def add_employee_to_department(self, emp_id: str, dept_id: str):
        if emp_id not in self.employees or dept_id not in self.departments:
            return False
        department = self.departments[dept_id]
        employee = self.employees[emp_id]
        
        if employee not in department.employees:
            department.employees.append(employee)
            employee.department = department.name
        return True

    def add_benefit(self, benefit: Benefit):
        if benefit.benefit_id in self.benefits:
            return False
        self.benefits[benefit.benefit_id] = benefit
        return True

    def assign_benefit(self, benefit_id: str, emp_id: str):
        if benefit_id not in self.benefits or emp_id not in self.employees:
            return False
        benefit = self.benefits[benefit_id]
        employee = self.employees[emp_id]
        
        if employee not in benefit.eligible_employees:
            benefit.eligible_employees.append(employee)
        return True

def print_menu():
    print("\n=== QUẢN LÝ NHÂN SỰ COTECCONS ===")
    print("1. Quản lý nhân viên")
    print("2. Quản lý ứng viên")
    print("3. Quản lý dự án")
    print("4. Quản lý phòng ban")
    print("5. Quản lý phúc lợi")
    print("0. Thoát")

def employee_menu():
    print("\n--- QUẢN LÝ NHÂN VIÊN ---")
    print("1. Thêm nhân viên")
    print("2. Tìm kiếm nhân viên")
    print("3. Cập nhật thông tin")
    print("4. Xóa nhân viên")
    print("5. Xem thông tin nhân viên")
    print("6. Danh sách nhân viên")
    print("0. Quay lại")

def candidate_menu():
    print("\n--- QUẢN LÝ ỨNG VIÊN ---")
    print("1. Thêm ứng viên")
    print("2. Xử lý ứng viên")
    print("3. Danh sách ứng viên")
    print("4. Xem thông tin chi tiết")
    print("0. Quay lại")

def project_menu():
    print("\n--- QUẢN LÝ DỰ ÁN ---")
    print("1. Tạo dự án mới")
    print("2. Phân công nhân viên")
    print("3. Cập nhật trạng thái")
    print("4. Xem thông tin dự án")
    print("5. Danh sách dự án")
    print("0. Quay lại")

def department_menu():
    print("\n--- QUẢN LÝ PHÒNG BAN ---")
    print("1. Thêm phòng ban")
    print("2. Phân công trưởng phòng")
    print("3. Thêm nhân viên vào phòng")
    print("4. Xem thông tin phòng ban")
    print("5. Danh sách phòng ban")
    print("0. Quay lại")

def benefit_menu():
    print("\n--- QUẢN LÝ PHÚC LỢI ---")
    print("1. Thêm phúc lợi")
    print("2. Phân bổ phúc lợi")
    print("3. Danh sách phúc lợi")
    print("4. Xem chi tiết phúc lợi")
    print("0. Quay lại")

def display_employee(hr_system):
    emp_id = input("Nhập mã nhân viên cần xem: ")
    if emp_id in hr_system.employees:
        print(hr_system.employees[emp_id])
    else:
        print("Không tìm thấy nhân viên!")

def display_candidate(hr_system):
    cand_id = input("Nhập mã ứng viên cần xem: ")
    if cand_id in hr_system.candidates:
        print(hr_system.candidates[cand_id])
    else:
        print("Không tìm thấy ứng viên!")

def display_project(hr_system):
    proj_id = input("Nhập mã dự án cần xem: ")
    if proj_id in hr_system.projects:
        print(hr_system.projects[proj_id])
    else:
        print("Không tìm thấy dự án!")

def list_employees(hr_system):
    if not hr_system.employees:
        print("Chưa có nhân viên nào!")
        return
    print("\nDanh sách nhân viên:")
    for emp in hr_system.employees.values():
        print(f"- {emp.id}: {emp.name} ({emp.position})")

def list_candidates(hr_system):
    if not hr_system.candidates:
        print("Chưa có ứng viên nào!")
        return
    print("\nDanh sách ứng viên:")
    for cand in hr_system.candidates.values():
        print(f"- {cand.id}: {cand.name} ({cand.position}) - {cand.status}")

def list_projects(hr_system):
    if not hr_system.projects:
        print("Chưa có dự án nào!")
        return
    print("\nDanh sách dự án:")
    for proj in hr_system.projects.values():
        print(f"- {proj.proj_id}: {proj.name} ({proj.status})")

def list_departments(hr_system):
    if not hr_system.departments:
        print("Chưa có phòng ban nào!")
        return
    print("\nDanh sách phòng ban:")
    for dept in hr_system.departments.values():
        print(f"- {dept.dept_id}: {dept.name}")

def list_benefits(hr_system):
    if not hr_system.benefits:
        print("Chưa có phúc lợi nào!")
        return
    print("\nDanh sách phúc lợi:")
    for ben in hr_system.benefits.values():
        print(f"- {ben.benefit_id}: {ben.name} (Giá trị: {ben.value})")

def main():
    hr_system = HRManagementSystem()
    
    while True:
        print_menu()
        choice = input("Nhập lựa chọn: ")
        
        if choice == "1":  # Quản lý nhân viên
            while True:
                employee_menu()
                emp_choice = input("Nhập lựa chọn: ")
                
                if emp_choice == "1":  # Thêm nhân viên 
                    id = input("Mã nhân viên: ")
                    name = input("Họ tên: ")
                    dob = datetime.strptime(input("Ngày sinh (YYYY-MM-DD): "), "%Y-%m-%d")
                    address = input("Địa chỉ: ")
                    phone = input("Số điện thoại: ")
                    email = input("Email: ")
                    position = input("Vị trí: ")
                    department = input("Phòng ban: ")
                    
                    employee = Employee(id, name, dob, address, phone, email, position, department)
                    if hr_system.add_employee(employee):
                        print("Thêm nhân viên thành công!") 
                elif emp_choice == "2":  # Tìm kiếm
                    search_term = input("Nhập tên nhân viên cần tìm: ")
                    results = hr_system.search_employees(name=search_term)
                    if results:
                        print("\nKết quả tìm kiếm:")
                        for emp in results:
                            print(f"- {emp.id}: {emp.name} ({emp.position})")
                    else:
                        print("Không tìm thấy nhân viên!")

                elif emp_choice == "3":  # Cập nhật
                    emp_id = input("Nhập mã nhân viên cần cập nhật: ")
                    if emp_id in hr_system.employees:
                        position = input("Vị trí mới (Enter để bỏ qua): ")
                        department = input("Phòng ban mới (Enter để bỏ qua): ")
                        
                        updates = {}
                        if position: updates['position'] = position
                        if department: updates['department'] = department
                        
                        if hr_system.update_employee(emp_id, **updates):
                            print("Cập nhật thành công!")
                    else:
                        print("Không tìm thấy nhân viên!")

                elif emp_choice == "4":  # Xóa
                    emp_id = input("Nhập mã nhân viên cần xóa: ")
                    if hr_system.remove_employee(emp_id):
                        print("Xóa nhân viên thành công!")
                    else:
                        print("Không tìm thấy nhân viên!")

                elif emp_choice == "5":  # Xem thông tin
                    display_employee(hr_system)
                    
                elif emp_choice == "6":  # Danh sách
                    list_employees(hr_system)

                elif emp_choice == "0":
                    break

        elif choice == "2":  # Quản lý ứng viên
            while True:
                candidate_menu()
                cand_choice = input("Nhập lựa chọn: ")
                
                if cand_choice == "1":  # Thêm ứng viên
                    try:
                        id = input("Mã ứng viên: ")
                        name = input("Họ tên: ")
                        dob = datetime.strptime(input("Ngày sinh (YYYY-MM-DD): "), "%Y-%m-%d")
                        address = input("Địa chỉ: ")
                        phone = input("Số điện thoại: ")
                        email = input("Email: ")
                        position = input("Vị trí ứng tuyển: ")
                        
                        candidate = Candidate(id, name, dob, address, phone, email, position)
                        if hr_system.add_candidate(candidate):
                            print("Thêm ứng viên thành công!")
                        else:
                            print("Lỗi: Mã ứng viên đã tồn tại!")
                    except ValueError as e:
                        print(f"Lỗi: {e}")

                elif cand_choice == "2":  # Xử lý ứng viên
                    cand_id = input("Nhập mã ứng viên: ")
                    if cand_id in hr_system.candidates:
                        status = input("Trạng thái mới (Hired/Rejected): ")
                        if status == "Hired":
                            department = input("Nhập phòng ban: ")
                            if hr_system.process_candidate(hr_system.candidates[cand_id], status, department):
                                print("Đã chuyển ứng viên thành nhân viên!")
                        elif status == "Rejected":
                            hr_system.process_candidate(hr_system.candidates[cand_id], status)
                            print("Đã cập nhật trạng thái ứng viên!")
                    else:
                        print("Không tìm thấy ứng viên!")

                elif cand_choice == "3":  # Danh sách
                    list_candidates(hr_system)

                elif cand_choice == "4":  # Xem chi tiết
                    display_candidate(hr_system)

                elif cand_choice == "0":
                    break

        elif choice == "3":  # Quản lý dự án
            while True:
                project_menu()
                proj_choice = input("Nhập lựa chọn: ")
                
                if proj_choice == "1":  # Tạo dự án
                    try:
                        proj_id = input("Mã dự án: ")
                        name = input("Tên dự án: ")
                        location = input("Địa điểm: ")
                        start_date = datetime.strptime(input("Ngày bắt đầu (YYYY-MM-DD): "), "%Y-%m-%d")
                        end_date = datetime.strptime(input("Ngày kết thúc (YYYY-MM-DD): "), "%Y-%m-%d")
                        
                        project = Project(proj_id, name, location, start_date, end_date)
                        if hr_system.add_project(project):
                            print("Thêm dự án thành công!")
                        else:
                            print("Lỗi: Mã dự án đã tồn tại!")
                    except ValueError as e:
                        print(f"Lỗi: {e}")

                elif proj_choice == "2":  # Phân công
                    emp_id = input("Mã nhân viên: ")
                    proj_id = input("Mã dự án: ")
                    if hr_system.assign_to_project(emp_id, proj_id):
                        print("Phân công thành công!")
                    else:
                        print("Lỗi: Kiểm tra lại mã nhân viên và mã dự án!")

                elif proj_choice == "3":  # Cập nhật trạng thái
                    proj_id = input("Mã dự án: ")
                    status = input("Trạng thái mới: ")
                    if hr_system.update_project_status(proj_id, status):
                        print("Cập nhật trạng thái thành công!")
                    else:
                        print("Không tìm thấy dự án!")

                elif proj_choice == "4":  # Xem thông tin
                    display_project(hr_system)

                elif proj_choice == "5":  # Danh sách
                    list_projects(hr_system)

                elif proj_choice == "0":
                    break

        elif choice == "4":  # Quản lý phòng ban
            while True:
                department_menu()
                dept_choice = input("Nhập lựa chọn: ")
                
                if dept_choice == "1":  # Thêm phòng ban
                    dept_id = input("Mã phòng ban: ")
                    name = input("Tên phòng ban: ")
                    department = Department(dept_id, name)
                    if hr_system.add_department(department):
                        print("Thêm phòng ban thành công!")
                    else:
                        print("Lỗi: Mã phòng ban đã tồn tại!")

                elif dept_choice == "2":  # Phân công trưởng phòng
                    dept_id = input("Mã phòng ban: ")
                    emp_id = input("Mã nhân viên: ")
                    if hr_system.assign_department_manager(dept_id, emp_id):
                        print("Phân công trưởng phòng thành công!")
                    else:
                        print("Lỗi: Kiểm tra lại mã phòng ban và mã nhân viên!")

                elif dept_choice == "3":  # Thêm nhân viên
                    dept_id = input("Mã phòng ban: ")
                    emp_id = input("Mã nhân viên: ")
                    if hr_system.add_employee_to_department(emp_id, dept_id):
                        print("Thêm nhân viên vào phòng ban thành công!")
                    else:
                        print("Lỗi: Kiểm tra lại mã phòng ban và mã nhân viên!")

                elif dept_choice == "4":  # Xem thông tin
                    dept_id = input("Nhập mã phòng ban: ")
                    if dept_id in hr_system.departments:
                        print(hr_system.departments[dept_id])
                    else:
                        print("Không tìm thấy phòng ban!")

                elif dept_choice == "5":  # Danh sách
                    list_departments(hr_system)

                elif dept_choice == "0":
                    break

        elif choice == "5":  # Quản lý phúc lợi
            while True:
                benefit_menu()
                ben_choice = input("Nhập lựa chọn: ")
                
                if ben_choice == "1":  # Thêm phúc lợi
                    try:
                        benefit_id = input("Mã phúc lợi: ")
                        name = input("Tên phúc lợi: ")
                        value = float(input("Giá trị: "))
                        start_date = datetime.strptime(input("Ngày bắt đầu (YYYY-MM-DD): "), "%Y-%m-%d")
                        end_date = datetime.strptime(input("Ngày kết thúc (YYYY-MM-DD): "), "%Y-%m-%d")
                        
                        benefit = Benefit(benefit_id, name, value, start_date, end_date)
                        if hr_system.add_benefit(benefit):
                            print("Thêm phúc lợi thành công!")
                        else:
                            print("Lỗi: Mã phúc lợi đã tồn tại!")
                    except ValueError as e:
                        print(f"Lỗi: {e}")

                elif ben_choice == "2":  # Phân bổ
                    benefit_id = input("Mã phúc lợi: ")
                    emp_id = input("Mã nhân viên: ")
                    if hr_system.assign_benefit(benefit_id, emp_id):
                        print("Phân bổ phúc lợi thành công!")
                    else:
                        print("Lỗi: Kiểm tra lại mã phúc lợi và mã nhân viên!")

                elif ben_choice == "3":  # Danh sách
                    list_benefits(hr_system)

                elif ben_choice == "4":  # Xem chi tiết
                    ben_id = input("Nhập mã phúc lợi: ")
                    if ben_id in hr_system.benefits:
                        print(hr_system.benefits[ben_id])
                    else:
                        print("Không tìm thấy phúc lợi!")

                elif ben_choice == "0":
                    break

        elif choice == "0":
            print("Tạm biệt!")
            break

if __name__ == "__main__":
    main()