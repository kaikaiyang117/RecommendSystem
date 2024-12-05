import csv
from datetime import datetime
import math
import numpy as np
import pandas as pd
from User import User

def createItemsProfiles(data_array, labels_names, items_names):
    items_profiles = {}
    for i in range(len(items_names)):
        items_profiles[items_names[i]] = {}
        for j in range(len(labels_names)):
            items_profiles[items_names[i]][labels_names[j]] = data_array[i][j]
    return items_profiles

def createUsersProfiles(data_array, users_names, items_names, labels_names, items_profiles):
    users_profiles = {}
    users_average_scores_list = []
    items_users_saw = {}
    items_users_saw_scores = {}
    for i in range(len(users_names)):
        items_users_saw_scores[users_names[i]] = []
        items_users_saw[users_names[i]] = []
        count = 0
        sum = 0.0
        for j in range(len(items_names)):
            if data_array[i][j] > 0:
                items_users_saw[users_names[i]].append(items_names[j])
                items_users_saw_scores[users_names[i]].append([items_names[j], data_array[i][j]])
                count += 1
                sum += data_array[i][j]
        if count == 0:
            users_average_scores_list.append(0)
        else:
            users_average_scores_list.append(sum / count)
    for i in range(len(users_names)):
        users_profiles[users_names[i]] = {}
        for j in range(len(labels_names)):
            count = 0
            score = 0.0
            for item in items_users_saw_scores[users_names[i]]:
                if items_profiles[item[0]][labels_names[j]] > 0:
                    score += (item[1] - users_average_scores_list[i])
                    count += 1
            if abs(score) < 1e-6:
                score = 0.0
            if count == 0:
                result = 0.0
            else:
                result = score / count
            users_profiles[users_names[i]][labels_names[j]] = result
    return (users_profiles, items_users_saw)

def calCosDistance(user, item, labels_names):
    sigma_ui = 0.0
    sigma_u = 0.0
    sigma_i = 0.0
    for label in labels_names:
        sigma_ui += user[label] * item[label]
        sigma_u += (user[label] * user[label])
        sigma_i += (item[label] * item[label])
    if sigma_u == 0.0 or sigma_i == 0.0:  # 若分母为0，相似度为0
        return 0
    return sigma_ui/math.sqrt(sigma_u * sigma_i)

# 基于内容的推荐算法：
def contentBased(user_profile, items_profiles, items_names, labels_names, items_user_saw):
    recommend_items = []
    for i in range(len(items_names)):
        if items_names[i] not in items_user_saw:
            recommend_items.append([items_names[i], calCosDistance(user_profile, items_profiles[items_names[i]], labels_names)])
    recommend_items.sort(key=lambda item: item[1], reverse=True)
    return recommend_items

# 输出推荐给该用户的节目列表
def printRecommendedItems(recommend_items_sorted, max_num):
    count = 0
    for item, degree in recommend_items_sorted:
        print("节目名：%s, 推荐指数：%f" % (item, degree))
        count += 1
        if count == max_num:
            break

def recommend_activities(user: User):
    all_users_names = [user.user_id]
    all_labels = ['AI', 'Robotics', 'Technology', 'Innovation', 'Coding', 'ompetition']
    labels_num = len(all_labels)
    df1 = pd.read_csv("./Recommend_info/activity_rating.csv")
    data_array1 = df1.iloc[:, 1:].values
    items_users_saw_names1 = df1.columns[1:].tolist()

    df2 = pd.read_csv("./Recommend_info/activity_rating_info.csv")
    data_array2 = df2.iloc[:, 1:].values
    items_users_saw_names2 = df2.iloc[:, 0].tolist()

    # 为用户看过的节目建立节目画像
    items_users_attend_profiles = createItemsProfiles(data_array2, all_labels, items_users_saw_names2)

    # 建立用户画像users_profiles和用户参加的活动集items_users_attend
    (users_profiles, items_users_attend) = createUsersProfiles(data_array1, all_users_names, items_users_saw_names1, all_labels, items_users_attend_profiles)

    df3 = pd.read_csv("./Recommend_info/activity_to_recommend_info.csv")
    data_array3 = df3.iloc[:, 1:].values
    items_to_be_recommended_names = df3.iloc[:, 0].tolist()

    # 为备选推荐节目集建立节目画像
    items_to_be_recommended_profiles = createItemsProfiles(data_array3, all_labels, items_to_be_recommended_names)

    for current_user in all_users_names:
        print("对于用户 %s 的推荐节目如下：" % current_user)
        recommend_items = contentBased(users_profiles[current_user], items_to_be_recommended_profiles, items_to_be_recommended_names, all_labels, items_users_attend[current_user])
        printRecommendedItems(recommend_items, 3)
        print()

# 用户实例
user = User(
    user_id="12345",
    name="Alice",
    email="alice@example.com",
    major="Computer Science",
    college="Engineering",
    tags=[],
    participation_count=3,
    joined_activities=[],
    created_at="2024-12-02",
    updated_at="2024-12-02"
)
recommend_activities(user)