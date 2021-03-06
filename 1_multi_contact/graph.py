import networkx as nx
import pandas as pd

# Reads input.
contacts = pd.read_json("/Users/yunpeng/Downloads/contacts.json")

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

# Iterate over the input file.
G = nx.Graph()
for index, row in contacts.iterrows():
  if index % 10000 == 0:
    print('Current going in #{} row.'.format(index))

  # Finds all tickets with the same email.
  current_ticket_id = row["Id"]
  for ticket_id in email_dict[current_ticket_id]:
    G.add_edge(current_ticket_id, ticket_id)

  # Finds all tickets with the same phone number.
  for ticket_id in phone_dict[current_ticket_id]:
    G.add_edge(current_ticket_id, ticket_id)

  # Finds all tickets with the same order ID.
  for ticket_id in order_dict[current_ticket_id]:
    G.add_edge(current_ticket_id, ticket_id)

# Converts to CSV.
df = pd.DataFrame(data={"ticket_trace/contact": output_data})
df.to_csv("output.csv", sep=',', index=True, index_label="ticket_id")
print("Finished converting to CSV file")
