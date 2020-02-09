# MimirScripts

Python scripts for managing a Mimir classroom.

## Motivation

When teaching an introduction class with 120 students, Mimir is a great tool for uploading code with built-in unit tests. However, I found the integration with Blackboard lacking and the plagarism tool too inaccurate, so these hacky solutions were generated.

## Plagarism tool

Mimir generates plagarism reports based off of their [Glitner algorithm](https://www.mimirhq.com/classroom/plagiarism-detection). This creates a percentage score between each pair of students and reports back all occurences above some instructor-set percentile. This becomes exponentially larger as the number of students increases, so this tool aggregates multiple plagarism reports and detects repeated student-pairs that across auto-plagarism reports.

[Insert screenshot here]

### How to create a plagarism report

First find your user session ID and user session token in Mimir. Follow [these instructions](https://support.google.com/chrome/answer/95647?co=GENIE.Platform%3DDesktop&hl=en).

After creating a submission and having student submissions, navigate to the "Plagarism" tab of the project and click "Check for Plagarism". This will generate a plagarism report with a unique URL sent to your email address. 

[Insert screenshot here]

Mimir currently does not support downloading plagarism reports. The Mimir web scraper uses Chromium web browser to scrape this data and store it in raw txt files.

Usage:
``` 
python mimir_web_scraper.py url1,url2,url3...
```

The plagarism tool takes all URLs and generates a report of <student_name, student_name> pairs with repeated copied occurences. The script ranks them based on a point value defined in plagarism_constants.xml.

Usage:
```
python mimir_cross_check.py txtfile1,txtfile2,txtfile3
``` 
