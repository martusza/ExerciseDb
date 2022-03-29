import requests
import json
from helpers import ExerciseDb

# Query text can be body part, target muscle or exercise name - used in get_data method
query_text = "hamstrings"

# Optional parameters to narrow down number of results - used in search_exercise method
search_params = {
    "name": "barbell good morning",
    "equipment": 'barbell'
}

# Creating object exercise_search
exercise_search = ExerciseDb()

# # This part of code allows pulling data for given body part / target muscle or equipment
# exercise_search.get_data(query_text)
# filtered_data = exercise_search.search_exercise(**search_params)
# exercise_search.export_to_csv("exercises.csv", filtered_data)

# To export all data and save it in batches in csv format
exercise_search.export_all(batch_size=None)