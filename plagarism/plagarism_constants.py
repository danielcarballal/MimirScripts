# User Session ID for Mimir from Chromium
USER_SESSION_ID_VALUE = ""

# User Session Token from Chromium
USER_SESSION_TOKEN_VALUE = ""

# Staff that will not be included in web scrape (first and last name).
INSTRUCTION_STAFF = []

# Files to ignore in web scrape.
FILES_TO_IGNORE = []

# Do not report all student pairs with less than MINIMUM_PLAGARISM_SCORE
# accumulated score. (Default per possible occurence is 1, but can be greater
# with multipliers).
MINIMUM_PLAGARISM_SCORE = 3

# Minimum score at which to mark a score as possible plagarism. (So if your
# assignments are out of 50 and you don't want to have signal from 30% or
# below as, set this to 15.

STUDENT_MINIMUM_SCORE = 20

# Maximum difference in score between two students on an assignment that above
# which plagarism check silently ignores the occurence.
STUDENT_MAX_DIFFERENCE = 100

# Multiplier for records that have the exact same score. I found that these
# were 2-3 times more likely to be blatantly plagarism.
SCORE_MULTIPLIER_SAME_SCORE = 2

# Multiplier if a file was manually marked plagarism.
SCORE_MULTIPLIER_MARKED_PLAGARIZED = 5

SILENCE_ERRORS = False