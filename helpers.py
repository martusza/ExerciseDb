import os
import json
import csv

import requests

AVAILABLE_BODY_PARTS = [
    "back",
    "cardio",
    "chest",
    "lower arms",
    "lower legs",
    "neck",
    "shoulders",
    "upper arms",
    "upper legs",
    "waist"
]

AVAILABLE_EQUIPMENT = [
    'ez barbell',
    'dumbbell',
    'weighted',
    'smith machine',
    'medicine ball',
    'barbell',
]

AVAILABLE_TARGET_MUSCLES = [
    'abductors',
    'abs',
    'adductors',
    'biceps',
    'calves',
    'cardiovascular system',
    'delts',
    'forearms',
    'glutes',
    'hamstrings',
    'lats',
    'levator scapulae',
    'pectorals',
    'quads',
    'serratus anterior',
    'spine',
    'traps',
    'triceps',
    'upper back'
]


class ExerciseDb:
    """
    Class to pull data from exercise db API and save to json file
    or read data from json files if exists
    """
    def __init__(self, key_path=None, data_folder="data"):
        """
        :param key_path: path to json file with API key
        """
        self.api_key = self.get_api_key(key_path)
        self.data = []
        self.file_path = data_folder
        self.validate_data_dir()

    @staticmethod
    def get_api_key(key_path):
        """
        Static method to get key value from json file
        :param key_path:
        :return:
        """
        path = "api_key.json" if not key_path else key_path
        if os.path.exists(path) and os.path.isfile(path):
            with open(path) as f:
                api_key = json.load(f).get("key")
            return api_key

    def validate_data_dir(self):
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)

    def read_api(self, query_text):
        """
        Method to get data from api using body part, target muscle or exercise name
        :param query_text:
        :return:
        """
        query_text_url = query_text.strip().replace(" ", "%20")
        if query_text in AVAILABLE_BODY_PARTS:
            url = f'https://exercisedb.p.rapidapi.com/exercises/bodyPart/{query_text_url}'
        elif query_text in AVAILABLE_TARGET_MUSCLES:
            url = f"https://exercisedb.p.rapidapi.com//exercises/target/{query_text_url}"
        else:
            url = f"https://exercisedb.p.rapidapi.com/exercises/name/{query_text_url}"

        headers = {
            'x-rapidapi-host': "exercisedb.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }
        print("Connecting with API")
        response = requests.request("GET", url, headers=headers)
        out = response.json()
        self.data = out
        query_text_file_name = query_text.replace(" ", "_")
        with open(os.path.join(self.file_path, f"exercises_{query_text_file_name}.json"), "w") as f:
            json.dump(out, f)

    def read_data(self, query_text):
        query_text_file_name = query_text.replace(" ", "_")
        with open(os.path.join(self.file_path, f"exercises_{query_text_file_name}.json")) as f:
            out = json.load(f)
        self.data = out

    def get_data(self, query_text):
        query_text_file_name = query_text.replace(" ", "_")
        path = os.path.join(self.file_path, f"exercises_{query_text_file_name}.json")
        if os.path.isfile(path):
            self.read_data(query_text_file_name)
        else:
            self.read_api(query_text)

    def search_exercise(self, **kwargs):
        matches = []
        for row in self.data:
            check = []
            # selecting filtered values by key vaule pairs
            for k, v in kwargs.items():
                if v in row.get(k):
                    check.append(v)
            if len(check) == len(kwargs):
                matches.append(row)
        print(matches)
        return matches

    def export_to_csv(self, filename, data=None):
        data = data if data else self.data
        path = os.path.join(self.file_path, filename)
        with open(path, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(data[0].keys())
            for line in data:
                writer.writerow(line.values())

    def export_all(self, batch_size=50):
        data_all = []
        id_all = []
        # data_all = ["id", "name_en", "name_pl", "description_en", "description_pl", "gifUrl", "bodyPart", "target"]
        for body_part in AVAILABLE_BODY_PARTS:
            self.get_data(body_part)
            for row in self.data:
                if row['id'] not in id_all:
                    row_export = {"id": "",
                                  "name_en": row["name"].capitalize(),
                                  "name_pl": row["name"].capitalize(),
                                  "description_en": "",
                                  "description_pl": "",
                                  "gifUrl": row["gifUrl"],
                                  "bodyPart": row["bodyPart"].capitalize(),
                                  "target": row["target"].capitalize(),
                                  }
                    data_all.append(row_export)
                    id_all.append(row['id'])

        # Saving all data if batch size == all
        if batch_size == "all" or not batch_size:
            filename = "exercises_all.csv"
            self.export_to_csv(filename, data_all)
            return
        # Saving data in batches
        for i, idx in enumerate(range(0, len(data_all), batch_size)):
            try:
                data_export = data_all[i: i+batch_size]
            except IndexError:
                data_export = data_all[i: ]
            if not os.path.exists(os.path.join(self.file_path, "batches")):
                os.mkdir(os.path.join(self.file_path, "batches"))
            filename = os.path.join("batches", f"exercises_batch{i}.csv")
            self.export_to_csv(filename, data_export)
