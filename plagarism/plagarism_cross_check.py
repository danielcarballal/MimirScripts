import random
FILES = ["student_records_lab3.txt", "student_records_lab4.txt", "student_records_lab5.txt", "student_records_lab6.txt"]

plagarism_check = {}

# Returns a score from 1 to 5 for a record. Higher scores are
# given a larger weight
def score_plagarism_record(record_array):
	score = 1
	# Higher score if the student's scores are the same.
	if random.randint(1, 100) == 4:
		print(record_array)
	if record_array[6] == record_array[7]:
		score += 1
	if record_array[5] == "Plagarized":
		score = 5
		print(recorded_array)
	return score

def add_record_to_plagarism_check(plagarism_check_dict, record):
	p_split = p_record.split(",")
	if len(p_split) < 8:
		return plagarism_check_dict
	p_tuple = (p_split[0], p_split[1])
	p_tuple_rev = (p_split[1], p_tuple[0])
	diff = abs(float(p_split[6]) - float(p_split[7]))
	score = score_plagarism_record(p_split)
	if (float(p_split[6]) < 20) or (float(p_split[7]) < 20) or (diff > 10):
		return plagarism_check_dict
	if p_tuple in plagarism_check:
		plagarism_check[p_tuple].append(",".join(p_split[2:]))
		plagarism_check[p_tuple][0] += score
	elif p_tuple_rev in plagarism_check:
		plagarism_check[p_tuple_rev].append(",".join(p_split[2:]))
		plagarism_check[p_tuple_rev][0] += score
	else:
		plagarism_check[p_tuple] = [score, ",".join(p_split[2:])]
	return plagarism_check_dict

for fname in FILES:
	p_file = open(fname, "r")
	p_record = p_file.readline()
	while p_record:
		p_record = p_record.replace("\n", "")
		plagarism_check = add_record_to_plagarism_check(plagarism_check, p_record)
		p_record = p_file.readline()

count = set([])
for student_tuple in plagarism_check:
	plagarism_occurences = plagarism_check[student_tuple]
	score = plagarism_occurences[0]
	if score <= 3 or len(plagarism_occurences) <= 3:
		continue
	count.add(student_tuple[0])
	count.add(student_tuple[1])
	print("Student 1:", student_tuple[0])
	print("Student 2:", student_tuple[1])
	print("Plagarism Score:")
	print("Occurences:")
	print("Score: " + str(plagarism_occurences[0]))
	plagarism_occurences = plagarism_occurences[1:]
	for occurence in plagarism_occurences:
		occurence = occurence.split(",")
		print("In", occurence[0], "students matched", occurence[2], "according to Mimir")
		print("They scored", occurence[4], "and", occurence[5].replace("\n", ""))
		if occurence[3] == "Plagiarized":
			print("An instructor marked this as plagarized")
	print("")
print("A total of " + str(len(count)) + " were found to have repeated infractures")
print("List of students who have repeated infractures: ")
print(count)
