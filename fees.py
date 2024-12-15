import tkinter as tk  
from tkinter import ttk, messagebox  
import json  
import os  
import csv  
from convertdate import islamic
from datetime import datetime

class FeesTrackerApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Fees Tracker")  
        
        self.data_file = 'students_data.json'  
        self.students = self.load_data()  
        
        self.current_year = datetime.now().year  
        self.current_month = datetime.now().month  
        self.current_day = datetime.now().day
        
        self.gregorian_months = ["January", "February", "March", "April", "May", "June",   
                  "July", "August", "September", "October", "November", "December"]  
        self.hijri_months = ["Moharram", "Safar", "Rabi ul Awwal", "Rabi ul Aakhar", 
                            "Jamadil Awwal", "Jamadil Aakhar", "Rajab", "Shaban", 
                            "Ramadan", "Shawwal", "Zilqad", "Zilhaj"]
        
        self.setup_ui()  
        self.set_focus_traversal()  

    def setup_ui(self):  
        # Student Entry Frame  
        self.student_frame = tk.Frame(self.root, padx=10, pady=10)  
        self.student_frame.pack(pady=5)  

        tk.Label(self.student_frame, text="Student Name:").grid(row=0, column=0, sticky="w")  
        self.student_name_entry = tk.Entry(self.student_frame)  
        self.student_name_entry.grid(row=0, column=1)  

        tk.Label(self.student_frame, text="Fees:").grid(row=1, column=0, sticky="w")  
        self.fees_entry = tk.Entry(self.student_frame)  
        self.fees_entry.grid(row=1, column=1)  

        tk.Label(self.student_frame, text="Calendar Type:").grid(row=2, column=0, sticky="w")  
        self.calendar_type = ttk.Combobox(self.student_frame, values=["Gregorian", "Hijri"])  
        self.calendar_type.grid(row=2, column=1)  
        self.calendar_type.bind("<<ComboboxSelected>>", self.update_months)

        tk.Label(self.student_frame, text="Starting Month:").grid(row=3, column=0, sticky="w")  
        self.starting_month = ttk.Combobox(self.student_frame, values=self.gregorian_months)  
        self.starting_month.grid(row=3, column=1)  

        tk.Label(self.student_frame, text="Mobile Number:").grid(row=4, column=0, sticky="w")  
        self.mobile_number_entry = tk.Entry(self.student_frame)  
        self.mobile_number_entry.grid(row=4, column=1)  

	# Add the Add Student button
        self.add_student_button = tk.Button(self.student_frame, text="Add Student", command=self.add_student)
        self.add_student_button.grid(row=5, columnspan=2, pady=5)

        # Add the Edit Student Entry button beside the Add Student button
        self.edit_student_button = tk.Button(self.student_frame, text="Edit Student Entry", command=self.edit_student)
        self.edit_student_button.grid(row=6, columnspan=2, pady=5)

    	# Adjust the position of the View Records button to be below the Add Student and Edit Student Entry buttons
        self.view_records_button = tk.Button(self.student_frame, text="View Records", command=self.view_records)
        self.view_records_button.grid(row=7, columnspan=2, pady=5)  

        # Update Fees Frame
        self.update_frame = tk.Frame(self.root, padx=10, pady=10)  
        self.update_frame.pack(pady=5)  

        tk.Label(self.update_frame, text="Select Student for Update:").grid(row=0, column=0, sticky="w")  
        self.select_student_update = ttk.Combobox(self.update_frame, values=[student['name'] for student in self.students])  
        self.select_student_update.grid(row=0, column=1)  
        self.select_student_update.bind("<<ComboboxSelected>>", self.show_pending_fees_for_update)  

        tk.Label(self.update_frame, text="Select Month to Pay:").grid(row=1, column=0, sticky="w")  
        self.months_to_update = ttk.Combobox(self.update_frame)  
        self.months_to_update.grid(row=1, column=1)  

        self.update_fees_button = tk.Button(self.update_frame, text="Update Fees", command=self.update_fees)  
        self.update_fees_button.grid(row=2, columnspan=2, pady=5)  

        # Delete Fees Frame
        self.delete_frame = tk.Frame(self.root, padx=10, pady=10)  
        self.delete_frame.pack(pady=5)  

        tk.Label(self.delete_frame, text="Select Student for Deletion:").grid(row=0, column=0, sticky="w")  
        self.select_student_delete = ttk.Combobox(self.delete_frame, values=[student['name'] for student in self.students])  
        self.select_student_delete.grid(row=0, column=1)  
        self.select_student_delete.bind("<<ComboboxSelected>>", self.show_paid_fees_for_deletion)  

        tk.Label(self.delete_frame, text="Select Month to Delete:").grid(row=1, column=0, sticky="w")  
        self.months_to_delete = ttk.Combobox(self.delete_frame)  
        self.months_to_delete.grid(row=1, column=1)  

        self.delete_fees_button = tk.Button(self.delete_frame, text="Delete Fees", command=self.delete_fees)  
        self.delete_fees_button.grid(row=2, columnspan=2, pady=5)  

        # Send Message Frame
        self.send_message_frame = tk.Frame(self.root, padx=10, pady=10)  
        self.send_message_frame.pack(pady=5)  

        tk.Label(self.send_message_frame, text="Select Student to Send Message:").grid(row=0, column=0, sticky="w")  
        self.select_student_message = ttk.Combobox(self.send_message_frame, values=[student['name'] for student in self.students])  
        self.select_student_message.grid(row=0, column=1)  

        self.send_reminder_button = tk.Button(self.send_message_frame, text="Send Reminder", command=self.send_reminder)  
        self.send_reminder_button.grid(row=1, column=0, pady=5)  

        self.send_acknowledgment_button = tk.Button(self.send_message_frame, text="Send Acknowledgment", command=self.send_acknowledgment)  
        self.send_acknowledgment_button.grid(row=1, column=1, pady=5)  

        # Dashboard Frame
        self.dashboard_frame = tk.Frame(self.root, padx=10, pady=10)  
        self.dashboard_frame.pack(pady=5)  

        self.update_dashboard_button = tk.Button(self.dashboard_frame, text="Update Dashboard", command=self.update_dashboard)  
        self.update_dashboard_button.grid(row=0, column=0, pady=5)  

        self.export_button = tk.Button(self.dashboard_frame, text="Export to CSV", command=self.export_data_to_csv)  
        self.export_button.grid(row=1, column=0, pady=5)  

    def edit_student(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Student Entry")

        tk.Label(edit_window, text="Select Student:").grid(row=0, column=0, sticky="w")
        self.select_student_edit = ttk.Combobox(edit_window, values=[student['name'] for student in self.students])
        self.select_student_edit.grid(row=0, column=1)
        self.select_student_edit.bind("<<ComboboxSelected>>", self.load_student_data_for_edit)

        tk.Label(edit_window, text="Monthly Fees:").grid(row=1, column=0, sticky="w")
        self.edit_fees_entry = tk.Entry(edit_window)
        self.edit_fees_entry.grid(row=1, column=1)

        tk.Label(edit_window, text="Calendar Type:").grid(row=2, column=0, sticky="w")
        self.edit_calendar_type = ttk.Combobox(edit_window, values=["Gregorian", "Hijri"])
        self.edit_calendar_type.grid(row=2, column=1)

        tk.Label(edit_window, text="Mobile Number:").grid(row=3, column=0, sticky="w")
        self.edit_mobile_number_entry = tk.Entry(edit_window)
        self.edit_mobile_number_entry.grid(row=3, column=1)

        self.update_student_button = tk.Button(edit_window, text="Update Student", command=lambda: self.update_student(edit_window))
        self.update_student_button.grid(row=4, columnspan=2, pady=5)

        self.delete_student_button = tk.Button(edit_window, text="Delete Student", command=lambda: self.delete_student(edit_window))
        self.delete_student_button.grid(row=5, columnspan=2, pady=5)

    def load_student_data_for_edit(self, event):
        selected_student_name = self.select_student_edit.get()
        if not selected_student_name:
            return

        for student in self.students:
            if student['name'] == selected_student_name:
                self.edit_fees_entry.delete(0, tk.END)
                self.edit_fees_entry.insert(0, student['fees'])
                self.edit_calendar_type.set(student['calendar_type'])
                self.edit_mobile_number_entry.delete(0, tk.END)
                self.edit_mobile_number_entry.insert(0, student.get('mobile_number', ''))
                break
    
    def update_student(self, edit_window):
        selected_student_name = self.select_student_edit.get()
        if not selected_student_name:
            messagebox.showwarning("Input Error", "Please select a student!")
            return

        for student in self.students:
            if student['name'] == selected_student_name:
                try:
                    student['fees'] = float(self.edit_fees_entry.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Fees must be a number!")
                    return

                student['calendar_type'] = self.edit_calendar_type.get()
                student['mobile_number'] = self.edit_mobile_number_entry.get()

                self.save_data()  # Save data to file
                messagebox.showinfo("Update Success", f"Student {selected_student_name} updated successfully!")
                edit_window.destroy()

                # Update the select student comboboxes for updating, deleting, and messaging
                self.select_student_update['values'] = [student['name'] for student in self.students]
                self.select_student_delete['values'] = [student['name'] for student in self.students]
                self.select_student_message['values'] = [student['name'] for student in self.students]
                break

    def delete_student(self, edit_window):
        selected_student_name = self.select_student_edit.get()
        if not selected_student_name:
            messagebox.showwarning("Input Error", "Please select a student!")
            return

        for i, student in enumerate(self.students):
            if student['name'] == selected_student_name:
                del self.students[i]
                self.save_data()  # Save data to file
                messagebox.showinfo("Delete Success", f"Student {selected_student_name} deleted successfully!")
                edit_window.destroy()

                # Update the select student comboboxes for updating, deleting, and messaging
                self.select_student_update['values'] = [student['name'] for student in self.students]
                self.select_student_delete['values'] = [student['name'] for student in self.students]
                self.select_student_message['values'] = [student['name'] for student in self.students]
                break


    def update_months(self, event=None):
        if self.calendar_type.get() == "Hijri":
            self.starting_month['values'] = self.hijri_months
        else:
            self.starting_month['values'] = self.gregorian_months

    def set_focus_traversal(self):  
        self.root.bind('<Return>', self.select_button)  

    def select_button(self, event):  
        widget = self.root.focus_get()  
        if isinstance(widget, tk.Button):  
            widget.invoke()  

    def load_data(self):  
        if os.path.exists(self.data_file):  
            with open(self.data_file, 'r') as file:  
                return json.load(file)  
        return []  

    def save_data(self):  
        with open(self.data_file, 'w') as file:  
            json.dump(self.students, file, indent=4)  

    def add_student(self):  
        student_name = self.student_name_entry.get()  
        fees = self.fees_entry.get()  
        calendar_type = self.calendar_type.get()  
        starting_month = self.starting_month.get()  
        mobile_number = self.mobile_number_entry.get()

        if not student_name or not fees or not calendar_type or not starting_month or not mobile_number:  
            messagebox.showwarning("Input Error", "All fields are required!")  
            return  

        if any(student['name'] == student_name for student in self.students):  
            messagebox.showerror("Input Error", "Student name already exists!")  
            return  

        try:  
            fees = float(fees)  
        except ValueError:  
            messagebox.showerror("Input Error", "Fees must be a number!")  
            return  

        student_data = {  
            "name": student_name,  
            "fees": fees,  
            "calendar_type": calendar_type,  
            "starting_month": starting_month,  
            "mobile_number": mobile_number,  # Save mobile number
            "paid_months": []  # List to track months when fees are paid  
        }  
        self.students.append(student_data)  
        self.save_data()  # Save data to file  
        
        # Clear input fields
        self.student_name_entry.delete(0, tk.END)
        self.fees_entry.delete(0, tk.END)
        self.calendar_type.set('')
        self.starting_month.set('')
        self.mobile_number_entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"Student {student_name} added successfully!")  

        # Update the select student comboboxes for updating and deleting fees  
        self.select_student_update['values'] = [student['name'] for student in self.students]  
        self.select_student_delete['values'] = [student['name'] for student in self.students]  
        self.select_student_message['values'] = [student['name'] for student in self.students]  

    def show_pending_fees_for_update(self, event):  
        selected_student_name = self.select_student_update.get()  
        if not selected_student_name:  
            return  

        for student in self.students:  
            if student['name'] == selected_student_name:  
                total_months = self.gregorian_months if student['calendar_type'] == 'Gregorian' else self.hijri_months
                starting_index = total_months.index(student['starting_month'])
                current_month_index = total_months.index(total_months[self.current_month - 1]) if student['calendar_type'] == 'Gregorian' else self.hijri_months.index(self.hijri_months[self.current_month - 1])
                
                paid_months = student['paid_months']  
                pending_months = [month for month in total_months[starting_index:current_month_index + 1] if month not in paid_months]  

                self.months_to_update['values'] = pending_months  # Show pending months for update
                if pending_months:
                    self.months_to_update.set(pending_months[0])  # Auto-select first pending month
                else:
                    self.months_to_update.set('')
                break  

    def show_paid_fees_for_deletion(self, event):  
        selected_student_name = self.select_student_delete.get()  
        if not selected_student_name:  
            return  

        for student in self.students:  
            if student['name'] == selected_student_name:  
                total_months = self.gregorian_months if student['calendar_type'] == 'Gregorian' else self.hijri_months
                starting_index = total_months.index(student['starting_month'])
                
                paid_months = student['paid_months']  

                self.months_to_delete['values'] = paid_months  # Show paid months for deletion
                if paid_months:
                    self.months_to_delete.set(paid_months[0])  # Auto-select first paid month
                else:
                    self.months_to_delete.set('')
                break  

    def update_fees(self):  
        selected_student_name = self.select_student_update.get()  
        selected_month = self.months_to_update.get()  

        if not selected_student_name or not selected_month:  
            messagebox.showwarning("Input Error", "Please select a student and month!")  
            return  

        for student in self.students:  
            if student['name'] == selected_student_name:  
                if selected_month not in student['paid_months']:  
                    student['paid_months'].append(selected_month)  
                    self.save_data()  # Save data to file  
                    messagebox.showinfo("Update Success", f"Fees for {selected_student_name} updated for {selected_month}.")  
                else:  
                    messagebox.showinfo("Already Paid", f"Fees for {selected_student_name} for {selected_month} have already been marked as paid.")  
                break  

    def delete_fees(self):  
        selected_student_name = self.select_student_delete.get()  
        selected_month = self.months_to_delete.get()  

        if not selected_student_name or not selected_month:  
            messagebox.showwarning("Input Error", "Please select a student and month!")  
            return  

        for student in self.students:  
            if student['name'] == selected_student_name:  
                if selected_month in student['paid_months']:  
                    student['paid_months'].remove(selected_month)  
                    self.save_data()  # Save data to file  
                    messagebox.showinfo("Delete Success", f"Fees for {selected_student_name} for {selected_month} deleted.")  
                else:  
                    messagebox.showinfo("Not Paid", f"Fees for {selected_student_name} for {selected_month} have not been marked as paid.")  
                break  

    def send_reminder(self):  
        selected_student_name = self.select_student_message.get()  
        if not selected_student_name:  
            messagebox.showwarning("Input Error", "Please select a student!")  
            return  

        for student in self.students:  
            if student['name'] == selected_student_name:  
                mobile_number = student['mobile_number']  
                # Here you would integrate with an SMS API to send the reminder
                # For example: send_message(mobile_number, "Your fees are due. Please make the payment.")
                messagebox.showinfo("Message Sent", f"Reminder sent to {selected_student_name} at {mobile_number}")  
                break  

    def send_acknowledgment(self):  
        selected_student_name = self.select_student_message.get()  
        if not selected_student_name:  
            messagebox.showwarning("Input Error", "Please select a student!")  
            return  

        for student in self.students:  
            if student['name'] == selected_student_name:  
                mobile_number = student['mobile_number']  
                # Here you would integrate with an SMS API to send the acknowledgment
                # For example: send_message(mobile_number, "Your fees have been received. Thank you.")
                messagebox.showinfo("Message Sent", f"Acknowledgment sent to {selected_student_name} at {mobile_number}")  
                break  

    def get_current_month_index(self, calendar_type):
        if calendar_type == 'Gregorian':
            return self.current_month - 1  # 0-based index for Gregorian months
        elif calendar_type == 'Hijri':
            # Convert the current Gregorian date to Hijri
            current_gregorian_date = datetime.now().date()
            hijri_year, hijri_month, hijri_day = islamic.from_gregorian(
                current_gregorian_date.year,
                current_gregorian_date.month,
                current_gregorian_date.day
            )
            # Return the 0-based index for the Hijri month
            return self.hijri_months.index(self.hijri_months[hijri_month - 1])
        else:
            raise ValueError("Invalid calendar type")

    def view_records(self):  
        if not self.students:  
            messagebox.showinfo("No Records", "No student records found!")  
            return  

        records_window = tk.Toplevel(self.root)  
        records_window.title("Student Records")  

        tk.Label(records_window, text="Student Records", font=("Arial", 14)).pack(pady=5)  

        for student in self.students:  
            total_months = self.gregorian_months if student['calendar_type'] == 'Gregorian' else self.hijri_months
            starting_index = total_months.index(student['starting_month'])
            
            current_month_index = self.get_current_month_index(student['calendar_type']) + 1  # Include current month
            
            paid_months = student['paid_months']  
            pending_months = [month for month in total_months[starting_index:current_month_index] if month not in paid_months]  

            record = (  
                f"Name: {student['name']}, "  
                f"Monthly Fees: ${student['fees']}, "  
                f"Calendar Type: {student['calendar_type']}, "  
                f"Joined From: {student['starting_month']}, "  
                f"Paid Months: {', '.join(paid_months) if paid_months else 'None'}, "  
                f"Pending Months: {', '.join(pending_months) if pending_months else 'None'}"  
            )  
            tk.Label(records_window, text=record).pack()  
  

    def update_dashboard(self):  
    	total_received = 0  
    	total_pending = 0  
    	received_fees_detail = {}  
    	pending_fees_detail = {}  
      
    	for student in self.students:  
        	total_months = self.gregorian_months if student['calendar_type'] == 'Gregorian' else self.hijri_months
        	starting_index = total_months.index(student['starting_month'])
        
        	current_month_index = self.get_current_month_index(student['calendar_type']) + 1  # Include current month
        
        	paid_months = student['paid_months']  
        	pending_months = [month for month in total_months[starting_index:current_month_index] if month not in paid_months]  
        
        	if pending_months:  
            		pending_fees_detail[student['name']] = pending_months  
            		total_pending += len(pending_months) * student['fees']  
        
        	if paid_months:  
            		received_fees_detail[student['name']] = paid_months  
            		total_received += len(paid_months) * student['fees']  

    	summary_window = tk.Toplevel(self.root)  
    	summary_window.title("Dashboard")  

    	tk.Label(summary_window, text=f"Total Received Fees: ₹{total_received}", font=("Arial", 12)).pack(pady=5)  
    	for name, months in received_fees_detail.items():  
        	received_fees_amount = len(months) * self.students[[student['name'] for student in self.students].index(name)]['fees']
        	tk.Label(summary_window, text=f"{name}: {', '.join(months)} (Amount: ₹{received_fees_amount})").pack()

    	tk.Label(summary_window, text=f"Total Pending Fees: ₹{total_pending}", font=("Arial", 12)).pack(pady=5)  
    	for name, months in pending_fees_detail.items():  
        	pending_fees_amount = len(months) * self.students[[student['name'] for student in self.students].index(name)]['fees']
        	tk.Label(summary_window, text=f"{name}: {', '.join(months)} (Amount: ₹{pending_fees_amount})").pack()




    def export_data_to_csv(self):  
        if not self.students:  
            messagebox.showinfo("No Records", "No student records to export!")  
            return  

        filename = "students_data.csv"  
        with open(filename, mode='w', newline='') as file:  
            writer = csv.writer(file)  

            # Header  
            writer.writerow(["Name", "Fees", "Calendar Type", "Starting Month", "Mobile Number", "Paid Months", "Pending Months"])  

            # Write student data  
            for student in self.students:  
                # Ensure 'mobile_number' key exists, default to empty string if not  
                mobile_number = student.get('mobile_number', '')  
                
                total_months = self.gregorian_months if student['calendar_type'] == 'Gregorian' else self.hijri_months
                starting_index = total_months.index(student['starting_month'])
                current_month_index = self.get_current_month_index(student['calendar_type']) + 1  # Include current month
                
                paid_months = student['paid_months']  
                pending_months = [month for month in total_months[starting_index:current_month_index] if month not in paid_months]  
                
                writer.writerow([  
                    student['name'],  
                    student['fees'],  
                    student['calendar_type'],  
                    student['starting_month'],  
                    mobile_number,  # Include mobile number in CSV
                    ', '.join(paid_months),  # Joining paid months with commas  
                    ', '.join(pending_months)  # Joining pending months with commas  
                ])  

        messagebox.showinfo("Export Success", f"Data has been exported to {filename}")   

# Main execution  
if __name__ == "__main__":  
    root = tk.Tk()  
    app = FeesTrackerApp(root)  
    root.mainloop()
