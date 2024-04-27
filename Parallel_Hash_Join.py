import threading
from prettytable import PrettyTable

EMPLOYEE_LIST = [
    {"E.Id": 101, "Employee Name": "Arjun Mehta", "Department": "Engineering"},
    {"E.Id": 102, "Employee Name": "Neha Patel", "Department": "Marketing"},
    {"E.Id": 103, "Employee Name": "Rajesh Singh", "Department": "Sales"},
    {"E.Id": 104, "Employee Name": "Kavya Kapoor", "Department": "Engineering"},
    {"E.Id": 105, "Employee Name": "Suresh Kumar", "Department": "Engineering"},
    {"E.Id": 106, "Employee Name": "Priya Sharma", "Department": "HR"},
    {"E.Id": 107, "Employee Name": "Vikas Gupta", "Department": "Finance"},
    {"E.Id": 108, "Employee Name": "Anjali Chawla", "Department": "Marketing"},
    {"E.Id": 109, "Employee Name": "Rohit Verma", "Department": "Engineering"},
    {"E.Id": 110, "Employee Name": "Pooja Joshi", "Department": "HR"},
    {"E.Id": 111, "Employee Name": "Manoj Rao", "Department": "Sales"},
    {"E.Id": 112, "Employee Name": "Sneha Desai", "Department": "Finance"},
]

PROJECT_LIST = [
    {"E.Id": 101, "Project": "Project One"},
    {"E.Id": 102, "Project": "Project Two"},
    {"E.Id": 103, "Project": "Project Three"},
    {"E.Id": 104, "Project": "Project Four"},
    {"E.Id": 105, "Project": "Project Five"},
]


def partition_data(data, num_partitions):
    partitions = [[] for _ in range(num_partitions)]
    for item in data:
        partition_index = hash(item["E.Id"]) % num_partitions
        partitions[partition_index].append(item)
    return partitions

def local_join(employee_partition, project_partition, result):
    project_hash = {item["E.Id"]: item["Project"] for item in project_partition}
    for employee in employee_partition:
        emp_id = employee["E.Id"]
        project = project_hash.get(emp_id)
        result.append({**employee, "Project": project})


def parallel_hash_join(EMPLOYEE_LIST, PROJECT_LIST, num_partitions):
    employee_partitions = partition_data(EMPLOYEE_LIST, num_partitions)
    project_partitions = partition_data(PROJECT_LIST, num_partitions)
    
    threads = []
    result = []
    
    for emp_partition, proj_partition in zip(employee_partitions, project_partitions):
        thread = threading.Thread(target=local_join, args=(emp_partition, proj_partition, result))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
        
    return result

# Perform the parallel hash join
result = parallel_hash_join(EMPLOYEE_LIST, PROJECT_LIST, num_partitions=4)

# Create a table to display the result
table = PrettyTable(["E.Id", "Employee Name", "Department", "Project"])
for item in result:
    table.add_row([item["E.Id"], item["Employee Name"], item["Department"], item["Project"]])

print(table)
