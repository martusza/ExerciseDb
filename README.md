# ExerciseDb
Class allows connecting with exercisedb API
to use that code you should have you api key in api_key.json file in the same folder

>exercise_db = ExerciseDb() #create object
exercise_db.export_all(batch_size=None) #save all data from API to csv

To get data for particular muscle / body part / equipment use
get_data method
>exercise_db.get_data(query_string)

If you add additional filtering to get the exercise more precisely use search_exercise method

>exercise_db.search_exercise(**kwargs)
