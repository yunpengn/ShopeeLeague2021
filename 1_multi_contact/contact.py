import pandas as pd

# Reads input.
contacts = pd.read_json("/Users/yunpeng/Downloads/contacts.json")
contacts.head()

# Creates a map from email to a list of ticket IDs.
email_dict = dict()
for index, row in contacts.iterrows():
	if row['Email']:
		if row['Email'] not in email_dict:
			email_dict[row['Email']]= set()
		email_dict[row['Email']].add(row['Id'])
print("Has finished email_dict")

# Creates a map from phone number to a list of ticket IDs.
phone_dict = dict()
for index, row in contacts.iterrows():
	if row['Phone']:
		if row['Phone'] not in phone_dict:
			phone_dict[row['Phone']]= set()
		phone_dict[row['Phone']].add(row['Id'])
print("Has finished phone_dict")

# Creates a map from order ID to a list of ticket IDs.
order_dict = dict()
for index, row in contacts.iterrows():
	if row['OrderId']:
		if row['OrderId'] not in phone_dict:
			order_dict[row['OrderId']]= set()
		order_dict[row['OrderId']].add(row['Id'])
print("Has finished order_dict")

# Creates a map from ticket ID to its original object.
contact_dict = dict()
for index, row in contacts.iterrows():
	contact_dict[row['Id']] = row
print("Has finished contact_dict")

# Builds a list from ticket_id to a list of relevant ticket IDs.
trace_dict = []

# Builds a list from ticket_id to total # of contacts.
count_dict = []

# Iterate over the input file.
for index, row in contacts.iterrows():
  if index % 10000 == 0:
    print('Current going in #{} row.'.format(index))

  # Finds all tickets with the same email.
  relevant_by_email = set()
  relevant_by_email.add(row["Id"])
  email = row['Email']
  if email:
    relevant_by_email = relevant_by_email.union(email_dict[email])

  # Finds all tickets with the same phone number.
  relevant_by_phone = set()
  relevant_by_phone.add(row["Id"])
  for relevant_ticket in relevant_by_email:
    phone_number = contact_dict[relevant_ticket]['Phone']
    if not phone_number:
      continue
    relevant_by_phone = relevant_by_phone.union(phone_dict[phone_number])
    relevant_by_phone.add(relevant_ticket)

  # Finds all tickets with the same order ID.
  relevant_by_order = set()
  relevant_by_order.add(row["Id"])
  for relevant_ticket in relevant_by_phone:
    order_id = contact_dict[relevant_ticket]['OrderId']
    if not order_id:
      continue
    relevant_by_order = relevant_by_order.union(order_dict[order_id])
    relevant_by_order.add(relevant_ticket)

  # Converts set to list and sorts.
  relevant_list = sorted(list(relevant_by_order), key=int)
  relevant_str  = [str(tk) for tk in relevant_list]

  # Saves result for all relevant ticket IDs.
  trace_dict.append("-".join(relevant_str))

  # Computes the total number of contacts.
  total_contacts = 0
  for ticket_id in relevant_list:
    num_contact = contact_dict[ticket_id]['Contacts']
    total_contacts = total_contacts + num_contact
  count_dict.append(total_contacts)

# Creates output data frame.
output_data = []

for index, trace in enumerate(trace_dict):
  count = count_dict[index]
  output_line = trace + ", " + str(count)
  output_data.append(output_data)
print("Finished output_data")

# Converts to CSV.
df = pd.DataFrame(data={"ticket_trace/contact": output_data})
df.to_csv("output.csv", sep=',', index=True, index_label="ticket_id")
print("Finished converting to CSV file")
