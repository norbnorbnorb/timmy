import csv
from pathlib import Path


file_name = '2v2_Tournament_100_03_29_2020_Responses_-_Form_Responses_1.csv'
file = Path.cwd() / file_name

team_names = []
with open(file, 'r', encoding='utf-8') as csv_file:
    csv_data = csv.DictReader(csv_file, delimiter=',', quotechar='"')
    # print('team names:')
    for num, row in enumerate(csv_data):
        # print(row['Team Name (There is a 15 character limit to your name and please keep it appropriate, or we will name you)'])
        row['team_name'] = row['Team Name (There is a 15 character limit to your name and please keep it appropriate, or we will name you)']
        # print(f'Enum: {num},  {row["team_name"]}')
        team_names.append(row['team_name'])

# print(team_names)
