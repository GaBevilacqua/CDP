from bs4 import BeautifulSoup

# Create a new XML structure
soup = BeautifulSoup(features='xml')  # Initialize XML parser
employees = soup.new_tag("employees")  # Create root element
soup.append(employees)

# --- Add first employee ---
employee1 = soup.new_tag("employee", id="101")
employees.append(employee1)

name1 = soup.new_tag("name")
name1.string = "John Doe"
employee1.append(name1)

position1 = soup.new_tag("position")
position1.string = "Software Engineer"
employee1.append(position1)

salary1 = soup.new_tag("salary")
salary1.string = "75000"
employee1.append(salary1)

# --- Add second employee ---
employee2 = soup.new_tag("employee", id="102")
employees.append(employee2)

name2 = soup.new_tag("name")
name2.string = "Jane Smith"
employee2.append(name2)

position2 = soup.new_tag("position")
position2.string = "Data Scientist"
employee2.append(position2)

salary2 = soup.new_tag("salary")
salary2.string = "85000"
employee2.append(salary2)

# --- Add third employee (corrected version) ---
employee3 = soup.new_tag("employee", id="103")
employees.append(employee3)

# Correct way to add name
name3 = soup.new_tag("name")
name3.string = "Alice Brown"
employee3.append(name3)

position3 = soup.new_tag("position")
position3.string = "Product Manager"
employee3.append(position3)

salary3 = soup.new_tag("salary")
salary3.string = "90000"
employee3.append(salary3)

# Save to file
with open("employees.xml", "w") as file:
    file.write(soup.prettify())

print("✅ XML file created successfully!")