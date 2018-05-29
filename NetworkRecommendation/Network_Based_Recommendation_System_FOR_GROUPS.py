import csv
import time
import pprint as pp
import networkx as nx

import Network_Based_Recommendation_System_FUNCTIONS as homework_2



print()
print("Current time: " + str(time.asctime(time.localtime())))
print()
print()


all_groups = [
	{1701: 1, 1703: 1, 1705: 1, 1707: 1, 1709: 1}, ### Movie night with friends.
	{1701: 1, 1702: 4}, ### First appointment scenario: the preferences of the girl are 4 times more important than those of the man.
	{1701: 1, 1702: 2, 1703: 1, 1704: 2}, ### Two couples scenario: the preferences of girls are still more important than those of the men...
	{1701: 1, 1702: 1, 1703: 1, 1704: 1, 1705: 1, 1720:10}, ### Movie night with a special guest.
	{1701: 1, 1702: 1, 1703: 1, 1704: 1, 1705: 1, 1720:10, 1721:10, 1722:10}, ### Movie night with 3 special guests.
]
print()
pp.pprint(all_groups)
print()


graph_file = "./input_data/u_data_homework_format.txt"

pp.pprint("Load Graph.")
print("Current time: " + str(time.asctime(time.localtime())))
graph_users_items = homework_2.create_graph_set_of_users_set_of_items(graph_file)
print(" #Users in Graph= " + str(len(graph_users_items['users'])))
print(" #Items in Graph= " + str(len(graph_users_items['items'])))
print(" #Nodes in Graph= " + str(len(graph_users_items['graph'])))
print(" #Edges in Graph= " + str(graph_users_items['graph'].number_of_edges()))
print("Current time: " + str(time.asctime(time.localtime())))
print()
print()


pp.pprint("Create Item-Item-Weighted Graph.")
print("Current time: " + str(time.asctime(time.localtime())))
item_item_graph = homework_2.create_item_item_graph(graph_users_items)
print(" #Nodes in Item-Item Graph= " + str(len(item_item_graph)))
print(" #Edges in Item-Item Graph= " + str(item_item_graph.number_of_edges()))
print("Current time: " + str(time.asctime(time.localtime())))
print()
print()


### Conversion of the 'Item-Item-Graph' to a scipy sparse matrix representation.
### This reduces a lot the PageRank running time ;)
print()
print(" Conversion of the 'Item-Item-Graph' to a scipy sparse matrix representation.")
N = len(item_item_graph)
nodelist = item_item_graph.nodes()
M = nx.to_scipy_sparse_matrix(item_item_graph, nodelist=nodelist, weight='weight', dtype=float)
print(" Done.")
print()
#################################################################################################


output_file = open("./Output_Recommendation_for_Group.tsv", 'w')
output_file_csv_writer = csv.writer(output_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
print()
for current_group in all_groups:
	print("Current group: ")
	pp.pprint(current_group)
	print("Current time: " + str(time.asctime(time.localtime())))
	
	################################################################################################################################################
	################################################################################################################################################

	# in this part of the homework we have to build a recommendation engine for a GROUP of users, where any user in the group is characterized by
	# a constant that we decided to consider as a measure of relative importance within his group and we assume to be always a positive integer 
	# bigger than or equal to one. 
	# So, given these assumption, we decided to modify the preferences (used to compute the PageRank on the item-item graph) 
	# weighting the ratings given by a user with the corresponding relative importance measure in this way: 
	# if the rating given by user to item is smaller of equal to 2, we multiply the rating for the inverse of the relative importance measure;
	# else if the rating given by user to item is bigger or equal to 3, we multipy the rating directly for the relative importance measure. 
	# For example, if the relative importance measure for user_i is 3 and his rating for item_j is 4, the final weighted score will be 12; 
	# instead if the rating for item_(j+1) is 2, the final weighted score will be 2/3 ( rating * 1/relative importance measure). 
	# With this method the relative importance measure works in positive and in negative direction.
	# After that, the final preference vector for the group is normalized to obtain a discrete probability distribution; 
	# the personalized PageRank is computed; and the items are sorted by decreasing personalized PageRank score. 
	# Finally we return an ordered list of recommendation for the group and all the process is repeated for every group.

	# P.S. we decided to remove (we know that it is not a constrain but the second part is open ended) the yet rated items from 
	# the final recommendation list because we think that, with a personalized PageRank built in this way, the final recommendation order 
	# could be biased if we consider the yet rated items; and in general we shoul order a longer list of final
	# scores also if we yet know the user score for these items(we could use different aggregation techniques). 
	# However it is possible to include these yet rated items in the final recommendation list simply commenting the line 141 in
	# the code (where you see ## COMMMENT .... ##): this could be the case when your girlfriend wants to see for the 30-th Titanic or 
	# your brother for the 100-th The gladiator. ':()

	################################################################################################################################################
	################################################################################################################################################

	sorted_list_of_recommended_items_for_current_group = []
	preference_for_current_group = {k : 0 for k in nodelist}
	
	rated_items_for_current_group = set()
	
	for user in current_group:
		
		# rated items by user 
		rated_by_user = set(graph_users_items["graph"][user].keys())
		
		# update rated items by this group
		rated_items_for_current_group.update(rated_by_user)

		
		# update weighted preference in the preference group for this user respect this particular item
		for item in graph_users_items["graph"][user]:

			rating = graph_users_items["graph"][user][item]["weight"]

			# if this user has given a bad rating to this item ------> decrease the positive impact on the overall preference vector
			if rating < 3:
				preference_for_current_group[item] += rating * ( 1/current_group[user] )
	
			# if this user has given a good rating to this item -----> increase the positive impact on the overall preference vector	
			else:
				preference_for_current_group[item] += rating * current_group[user]

			
	

	# normalization constant preference for the group
	normalization = sum(preference_for_current_group.values())
	
	# normalization preference for this group
	preference_for_current_group = {item : preference_for_current_group[item]/normalization for item in preference_for_current_group}
	
	# compute pageRank for group using preference for current group
	page_rank_for_current_group = homework_2.pagerank(M, N, nodelist, alpha=0.85, personalization=preference_for_current_group)
	
	# select only recommended items not yet rated by a member of this group
	recommendation_for_current_group = [ [ item, page_rank_for_current_group[item] ] for item in page_rank_for_current_group 
										if item not in rated_items_for_current_group ]  ## COMMENT this line if you want to consider yet rated items ##
	
	# sorted [item,score]
	recommendation_for_current_group = sorted(recommendation_for_current_group, key= lambda r : r[1], reverse=True)
	
	# final result [item]
	sorted_list_of_recommended_items_for_current_group = [rec[0] for rec in recommendation_for_current_group]
	
	###############################################################################################################################################
	###############################################################################################################################################
	
	print("Recommended Sorted List of Items:")
	print((str(sorted_list_of_recommended_items_for_current_group[:30])))
	print()
	output_file_csv_writer.writerow(sorted_list_of_recommended_items_for_current_group)
	
output_file.close()	
	
	




print()
print()
print("Current time: " + str(time.asctime(time.localtime())))
print("Done ;)")
print()
