import pandas as pd
import re
import json

pd.set_option('display.max_columns', None)
df = pd.read_csv('credit_score.csv')

credit_scores_list = df['CREDIT_SCORE'].tolist()

list_of_important_features = ['INCOME', 'SAVINGS', 'DEBT']
list_of_important_features_ratio = ['R_SAVINGS_INCOME', 'R_DEBT_INCOME', 'R_DEBT_SAVINGS']

# def datapoint_to_text(row):
#     line_number = 1
#     string_beginning = "This is a new individual. This individual has the following attributes:\n"
#     for column, value in row.items():
#         if column in list_of_important_features and column != 'DEBT':
#             string_beginning += f"{line_number}: a total {column.lower()} in the last 12 months of ${value}\n"
#         elif column == 'DEBT':
#             string_beginning += f"{line_number}: a total existing debt of ${value}\n"
#         elif column in list_of_important_features_ratio:
#             split_attribute = column.split("_")
#             string_beginning += f"{line_number}: a ratio of {split_attribute[1].lower()} to {split_attribute[2].lower()} of {value}\n"
#         elif re.match(r'T_[^_]+_[^_]+$', column):
#             split_attribute = column.split("_")
#             string_beginning += f"{line_number}: an expenditure on {split_attribute[1].lower()} in the past {split_attribute[2]} months of ${value}\n"
#         elif re.match(r'CAT_[^_]+$', column):
#             split_attribute = column.split("_")
#             if split_attribute[1] == "GAMBLING":
#                 if value == "No":
#                     string_beginning += f"{line_number}: no gambling habit\n"
#                 else:
#                     string_beginning += f"{line_number}: a gambling habit classified as {value.lower()}\n"
#             else:
#                 if value == 0:
#                     string_beginning += f"{line_number}: does not possess the following: {split_attribute[1].lower()}\n"
#                 else:
#                     string_beginning += f"{line_number}: possesses the following: {split_attribute[1].lower()}\n"
#         else:
#             line_number -= 1
#         line_number += 1
#     final_string = string_beginning + f"This individual's credit score is: {row['CREDIT_SCORE']}"
#     return final_string

def datapoint_to_text(row):
    line_number = 1
    string_beginning = "This is a new individual's attributes:\n"
    for column, value in row.items():
        if column in list_of_important_features or column in list_of_important_features_ratio or re.match(r'T_[^_]+_[^_]+$', column) or re.match(r'CAT_[^_]+$', column):
            if line_number in range(1, 4) or line_number in range(7, 31):
                string_beginning += f"{line_number}: ${value}\n"
            else:
                string_beginning += f"{line_number}: {value}\n"
            line_number += 1
    final_string = string_beginning + f"This individual's credit score is: {row['CREDIT_SCORE']}"
    return final_string

set_of_data_points = dict()
for i in range(1000):
    set_of_data_points[i] = datapoint_to_text(df.iloc[i])
with open("credit_scores.json", "w") as file:
    json.dump(set_of_data_points, file)


