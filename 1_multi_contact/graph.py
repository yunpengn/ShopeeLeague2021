import csv
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

  # Adds node first.
  current_ticket_id = row["Id"]
  G.add_node(current_ticket_id)

  # Finds all tickets with the same email.
  if current_ticket_id in email_dict:
    for ticket_id in email_dict[current_ticket_id]:
      G.add_edge(current_ticket_id, ticket_id)

  # Finds all tickets with the same phone number.
  if current_ticket_id in phone_dict:
    for ticket_id in phone_dict[current_ticket_id]:
      G.add_edge(current_ticket_id, ticket_id)

  # Finds all tickets with the same order ID.
  if current_ticket_id in order_dict:
    for ticket_id in order_dict[current_ticket_id]:
      G.add_edge(current_ticket_id, ticket_id)
print("Finished building graph.")

# Gets all connected components.
components = list(nx.connected_components(G))
print("Finished calculating components.")

# Processes each component.
trace_dict = dict()
for component in components:
  # Performs string concat.
  trace = "-".join([str(tk) for tk in component])

  # Gets the total number of contacts.
  total = 0
  for node in component:
    count = contact_dict[node]['Contacts']
    total = total + count

  # Gets output format
  output_line = trace + ", " + str(total)

  # Iterates over each node.
  for node in component:
    trace_dict[node] = output_line
print("Finished processing each component")

# Converts to CSV.
output_file = open('output.csv', 'w')

# Outputs header.
output_file.write('ticket_id, ticket_trace/contact\n')
print("Finished writing header")

# Outputs per line.
for i in range(500000):
  if index % 50000 == 0:
    print('Current writing in #{} row.'.format(index))

  output_file.write(str(i) + ', ' + trace_dict[i] + '\n')
print("Finished writing body")

# Closes file.
output_file.close()
print("Finished")
