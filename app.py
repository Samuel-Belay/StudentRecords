import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import tempfile
import os
import subprocess

class Student:
    def __init__(self, rn=None, name="", marks=None):
        self.rn = rn
        self.name = name
        self.marks = marks if marks else {}
    
    def total(self):
        return sum(self.marks.values())
    
    def average(self):
        return self.total() / len(self.marks) if self.marks else 0
    
    def grade(self):
        avg = self.average()
        if avg >= 90: return "A+"
        elif avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else: return "F"

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x700")
        self.students = []
        self.subjects = []
        self.current_edit_id = None
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Subject Management Frame
        subject_frame = ttk.LabelFrame(self.main_frame, text="Subject Management", padding=10)
        subject_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ttk.Label(subject_frame, text="Subject Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.subject_name = ttk.Entry(subject_frame)
        self.subject_name.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        
        ttk.Button(subject_frame, text="Add Subject", command=self.add_subject).grid(row=0, column=2, padx=5)
        ttk.Button(subject_frame, text="Delete Subject", command=self.delete_subject).grid(row=0, column=3, padx=5)
        
        # Subject List
        self.subject_listbox = tk.Listbox(subject_frame, height=5)
        self.subject_listbox.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=5)
        
        # Student Input Frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Student Information", padding=10)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Roll Number
        ttk.Label(input_frame, text="Roll Number:").grid(row=0, column=0, sticky="w", pady=2)
        self.roll_number = ttk.Entry(input_frame)
        self.roll_number.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        
        # Name
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky="w", pady=2)
        self.name = ttk.Entry(input_frame)
        self.name.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        
        # Marks Frame
        self.marks_frame = ttk.Frame(input_frame)
        self.marks_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.add_button = ttk.Button(button_frame, text="Add Student", command=self.add_student)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.update_button = ttk.Button(button_frame, text="Update", command=self.update_student, state=tk.DISABLED)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_edit, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Display Frame
        display_frame = ttk.LabelFrame(self.main_frame, text="Student Records", padding=10)
        display_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Treeview
        self.tree = ttk.Treeview(display_frame, columns=("RollNo", "Name", "Total", "Average", "Grade"), show="headings")
        self.tree.heading("RollNo", text="Roll No")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Average", text="Average")
        self.tree.heading("Grade", text="Grade")
        
        self.tree.column("RollNo", width=80, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Total", width=80, anchor="center")
        self.tree.column("Average", width=80, anchor="center")
        self.tree.column("Grade", width=60, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Treeview buttons
        tree_button_frame = ttk.Frame(display_frame)
        tree_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(tree_button_frame, text="Edit Selected", command=self.edit_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(tree_button_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(tree_button_frame, text="Print Preview", command=self.print_preview).pack(side=tk.LEFT, padx=5)
        
        # Details Frame
        details_frame = ttk.LabelFrame(self.main_frame, text="Student Details", padding=10)
        details_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=5, pady=5)
        
        self.details_text = tk.Text(details_frame, height=20, width=40, wrap=tk.WORD)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(2, weight=1)
        
        # Bind treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.show_student_details)
        
        # Initialize marks entry fields
        self.mark_entries = {}
        self.update_marks_fields()
    
    def add_subject(self):
        subject = self.subject_name.get().strip()
        if not subject:
            messagebox.showerror("Error", "Subject name cannot be empty")
            return
            
        if subject in self.subjects:
            messagebox.showerror("Error", f"Subject '{subject}' already exists")
            return
            
        self.subjects.append(subject)
        self.subject_listbox.insert(tk.END, subject)
        self.subject_name.delete(0, tk.END)
        self.update_marks_fields()
        messagebox.showinfo("Success", f"Subject '{subject}' added successfully")
    
    def delete_subject(self):
        selected = self.subject_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a subject to delete")
            return
        subject = self.subject_listbox.get(selected[0])
        if messagebox.askyesno("Delete Subject", f"Are you sure you want to delete '{subject}'?"):
            self.subjects.remove(subject)
            self.subject_listbox.delete(selected[0])
            # Remove subject from all students
            for student in self.students:
                if subject in student.marks:
                    del student.marks[subject]
            self.update_marks_fields()
            self.refresh_tree()
            messagebox.showinfo("Success", f"Subject '{subject}' deleted successfully")
    
    def update_marks_fields(self):
        # Clear existing mark entry fields
        for widget in self.marks_frame.winfo_children():
            widget.destroy()
            
        self.mark_entries = {}
        
        # Create new fields for each subject
        for i, subject in enumerate(self.subjects):
            ttk.Label(self.marks_frame, text=f"{subject}:").grid(row=i, column=0, sticky="w", pady=2)
            entry = ttk.Entry(self.marks_frame)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            self.mark_entries[subject] = entry
    
    def add_student(self):
        try:
            if not self.subjects:
                messagebox.showerror("Error", "Please add subjects first")
                return
                
            rn = self.roll_number.get().strip()
            if not rn.isdigit():
                messagebox.showerror("Error", "Please enter a valid roll number")
                return
            rn = int(rn)
            name = self.name.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            # Check for duplicate roll number (only if not editing)
            if self.current_edit_id is None:
                for student in self.students:
                    if student.rn == rn:
                        messagebox.showerror("Error", f"Roll number {rn} already exists")
                        return
            
            # Get marks for each subject
            marks = {}
            valid = True
            for subject in self.subjects:
                try:
                    mark = int(self.mark_entries[subject].get())
                    if not 0 <= mark <= 100:
                        messagebox.showerror("Error", f"Marks for {subject} must be between 0 and 100")
                        valid = False
                        break
                    marks[subject] = mark
                except ValueError:
                    messagebox.showerror("Error", f"Please enter valid marks for {subject}")
                    valid = False
                    break
                    
            if not valid:
                return
            
            if self.current_edit_id is not None:
                # Update existing student
                student = self.students[self.current_edit_id]
                student.rn = rn
                student.name = name
                student.marks = marks
                
                # Update treeview item
                selected_item = self.tree.selection()[0]
                self.tree.item(selected_item, values=(
                    student.rn,
                    student.name,
                    student.total(),
                    f"{student.average():.2f}",
                    student.grade()
                ))
                
                messagebox.showinfo("Success", "Student updated successfully")
                self.cancel_edit()
            else:
                # Create new student
                student = Student(rn, name, marks)
                self.students.append(student)
                
                # Add to treeview
                self.tree.insert("", tk.END, values=(
                    student.rn,
                    student.name,
                    student.total(),
                    f"{student.average():.2f}",
                    student.grade()
                ))
                
                self.clear_fields()
                messagebox.showinfo("Success", "Student added successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid roll number")
    # Deleting
    def clear_fields(self):
        self.roll_number.delete(0, tk.END)
        self.name.delete(0, tk.END)
        for entry in self.mark_entries.values():
            entry.delete(0, tk.END)
        self.roll_number.focus()
    
    def show_student_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        item_data = self.tree.item(selected_item)
        roll_no = item_data['values'][0]
        
        # Find the student
        for student in self.students:
            if student.rn == roll_no:
                self.display_student_details(student)
                break
    
    def display_student_details(self, student):
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = f"""Roll Number: {student.rn}
Name: {student.name}

Subject Marks:\n"""
        
        for subject, mark in student.marks.items():
            details += f"  {subject}: {mark}\n"
        
        total_marks = sum(mark for mark in student.marks.values())
        max_possible = 100 * len(student.marks)
        
        details += f"""
Summary:
Total Marks: {total_marks}/{max_possible}
Average: {student.average():.2f}%
Grade: {student.grade()}
"""
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
    
    def edit_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a student to edit")
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item)
        roll_no = item_data['values'][0]
        
        # Find the student in our list
        for i, student in enumerate(self.students):
            if student.rn == roll_no:
                self.current_edit_id = i
                self.load_student_for_edit(student)
                break
    
    def load_student_for_edit(self, student):
        self.clear_fields()
        self.roll_number.insert(0, str(student.rn))
        self.name.insert(0, student.name)
        
        for subject, mark in student.marks.items():
            if subject in self.mark_entries:
                self.mark_entries[subject].insert(0, str(mark))
        
        # Change button states
        self.add_button.config(state=tk.DISABLED)
        self.update_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.NORMAL)
    
    def update_student(self):
        self.add_student()  # Reuse the add_student logic for updates
    
    def cancel_edit(self):
        self.current_edit_id = None
        self.clear_fields()
        self.add_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
    
    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a student to delete")
            return
            
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item)
        roll_no = item_data['values'][0]
        
        # Find and remove the student from our list
        for i, student in enumerate(self.students):
            if student.rn == roll_no:
                del self.students[i]
                break
        
        # Remove from treeview
        self.tree.delete(selected_item)
        
        # Clear details if showing the deleted student
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state=tk.DISABLED)
        
        # If we were editing this student, cancel edit mode
        if self.current_edit_id is not None and self.current_edit_id >= len(self.students):
            self.cancel_edit()
        
        messagebox.showinfo("Success", "Student deleted successfully")
    
    def refresh_tree(self):
        # Clear and repopulate the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        for student in self.students:
            self.tree.insert("", tk.END, values=(
                student.rn,
                student.name,
                student.total(),
                f"{student.average():.2f}",
                student.grade()
            ))
    
    def print_preview(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a student to print")
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item)
        roll_no = item_data['values'][0]
        
        # Find the student
        for student in self.students:
            if student.rn == roll_no:
                self.show_print_dialog(student)
                break
    
    def show_print_dialog(self, student):
        # Create print preview window
        preview_win = tk.Toplevel(self.root)
        preview_win.title("Print Preview")
        preview_win.geometry("600x700")
        
        # Create scrolled text widget
        text_area = ScrolledText(
            preview_win,
            wrap=tk.WORD,
            font=("Courier New", 12),
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        
        # Generate formatted content
        content = self.generate_print_content(student)
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)
        
        # Add print button
        btn_frame = ttk.Frame(preview_win)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            btn_frame,
            text="Print",
            command=lambda: self.print_content(content)
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame,
            text="Close",
            command=preview_win.destroy
        ).pack(side=tk.RIGHT, padx=10)
    
    def generate_print_content(self, student):
        """Generate nicely formatted content for printing"""
        content = "\n"
        content += "=" * 60 + "\n"
        content += "STUDENT REPORT".center(60) + "\n"
        content += "=" * 60 + "\n\n"
        content += f"{'Roll Number:':<15} {student.rn}\n"
        content += f"{'Student Name:':<15} {student.name}\n\n"
        content += "SUBJECT MARKS:\n"
        content += "-" * 60 + "\n"
        
        for subject, mark in student.marks.items():
            content += f"{subject:<20} {mark:>3}/100\n"
        
        total = student.total()
        max_total = 100 * len(student.marks)
        avg = student.average()
        grade = student.grade()
        
        content += "\n"
        content += "PERFORMANCE SUMMARY:\n"
        content += "-" * 60 + "\n"
        content += f"{'Total Marks:':<15} {total}/{max_total}\n"
        content += f"{'Average:':<15} {avg:.2f}%\n"
        content += f"{'Grade:':<15} {grade}\n\n"
        content += "=" * 60 + "\n"
        content += "End of Report".center(60) + "\n"
        content += "=" * 60 + "\n"
        
        return content
    
    def print_content(self, content):
        """Print the content to the default printer"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write(content)
                temp_path = f.name
            
            # Platform-specific printing
            if os.name == 'nt':  # Windows
                os.startfile(temp_path, 'print')
            elif os.name == 'posix':  # Linux/Mac
                subprocess.run(['lp', temp_path])
            else:
                messagebox.showwarning(
                    "Printing",
                    "Printing not supported on this platform\n"
                    f"Content saved to: {temp_path}"
                )
                return
            
            messagebox.showinfo("Print", "Document sent to printer")
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not print:\n{str(e)}")
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
