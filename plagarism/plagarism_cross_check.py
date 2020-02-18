"""
Module for finding repeated occurences across plagarism reports.

Usage:

python plagarism_cross_check.py output1.csv,output2.csv
"""

from sys import flags

import plagarism_constants

# Util function to pretty print list of tuple occurences.
def print_occurences(student_tuple, plagarism_occurences):
	print("""***************************

Student 1: {student_1}
Student 2: {student_2}
Plagarism score: {plagarism_score}
Similar files:
{files}
""".format(
		student_1=student_tuple[0],
		student_2=student_tuple[1],
		plagarism_score=str(plagarism_occurences[0]),
		files="\n".join([str(f) for f in plagarism_occurences[1:]])))


class PlagarismCrossCheck(object):

	"""
	Inner class encapsulating single record information.
	"""
	class PlagarismCrossCheckRecord(object):
		def __init__(self, record_string):
			record_array = record_string.split(",")
			if len(record_array) < 6:
				raise TypeError(
					"Misformatted argument record_string: ", record_string)
			self.student1 = record_array[0]
			self.student2 = record_array[1]
			self.filename1 = record_array[2]
			self.filename2 = record_array[3]
			self.percent_similar = record_array[4]
			self.instructor_note = record_array[5]

			# Scores can be added to filter out less suspicious entries.
			if len(record_array) >= 8:
				self.student1_score = float(record_array[6])
				self.student2_score = float(record_array[7])
			else:
				self.student1_score, self.student2_score = -1, -1

		def student_tuple(self):
			return (self.student1, self.student2)

		def student_tuple_rev(self):
			return (self.student2, self.student1)

		def student_score_diff(self):
			return abs(self.student1_score - self.student2_score)

		def has_score(self):
			return not (self.student1_score == -1 or self.student2_score == -1)

		# Returns a score from for a record.
		def score_plagarism_record(self):
			score = 1
			if self.has_score() and self.student1_score == self.student1_score:
				score *= SCORE_MULTIPLIER_SAME_SCORE
			if self.instructor_note == "Plagarized":
				score *= SCORE_MULTIPLIER_MARKED_PLAGARIZED
			return score

		def should_ignore(self):
			if self.has_score():
				print(self)
				return (self.student_score_diff() > STUDENT_MAX_DIFFERENCE or
					self.student1_score < STUDENT_MINIMUM_SCORE or
						self.student2_score < STUDENT_MINIMUM_SCORE)
			return False

		def __str__(self):
			return """
In {assignment} these students matched {percentage} according to Mimir.
{scores}{instructor_note}""".format(
			assignment=self.filename1,
			percentage=self.percent_similar,
			scores="\nTheir graded scores were {score1} and {score2}".format(
				score1=self.student1_score,
				score2=self.student2_score) if self.has_score() else "",
			instructor_note="An instructor marked this as plagarized"
			if self.instructor_note == "\nMarked As Plagiarized" else "")


	"""
	self.files is a list of csv student_record files where each line is one plagarism occurence.

	student1,student2,filename1,fiename,percent_plagarized,instructor_note
	"""
	def __init__(self):
		self.files = []
		self.plagarism_check = {}

	def add_record_to_plagarism_check(self, record):
		score = record.score_plagarism_record()

		if (record.should_ignore()):
			return

		if record.student_tuple() in self.plagarism_check:
			self.plagarism_check[record.student_tuple()].append(record)
			self.plagarism_check[record.student_tuple()][0] += score
		elif record.student_tuple_rev() in self.plagarism_check:
			self.plagarism_check[record.student_tuple_rev()].append(record)
			self.plagarism_check[record.student_tuple_rev()][0] += score
		else:
			self.plagarism_check[record.student_tuple()] = [score, record]

	def add_file(self, fname):
		fname = "testdata/" + fname
		p_file = open(fname, "r")
		p_record = p_file.readline()
		while p_record:
			p_record = p_record.replace("\n", "")
			try:
				record_object = self.PlagarismCrossCheckRecord(p_record)
				self.add_record_to_plagarism_check(record_object)
			except TypeError as e:
				if not SILENCE_ERRORS:
					raise e
			p_record = p_file.readline()


	def print_to_std_out(self):
		for student_tuple in self.plagarism_check:
			plagarism_occurences = self.plagarism_check[student_tuple]
			score = plagarism_occurences[0]
			if score <= MINIMUM_PLAGARISM_SCORE:
				continue
			print_occurences(student_tuple, plagarism_occurences)

	def print_repeated_infractures(self):
		repeated_infractions = set([])
		for student_tuple in self.plagarism_check:
			plagarism_occurences = self.plagarism_check[student_tuple]
			score = plagarism_occurences[0]
			if score <= MINIMUM_PLAGARISM_SCORE:
				continue
			repeated_infractions.add(student_tuple[0])
			repeated_infractions.add(student_tuple[1])
		print("A total of " + str(len(repeated_infractions)) +
			" were found to have repeated infractures")
		print("Set of students who have repeated infractures: ")
		print(repeated_infractions)


if __name__ == "__main__":
	files = flags[0].split(",")
	pcc = PlagarismCrossCheck()
	for f in files: # List of record files
		pcc.add_file(f)
	pcc.print_to_std_out()
	pcc.print_repeated_infractures()