import {activity_entry, activity_in, activity_out, food_popup_in, food_popup_out } from "@/types";

export async function fetchFoods() {
    const response = await fetch("http://localhost:5000/popup_food");
    if (!response.ok) {
        throw new Error('Failed to fetch food list');
    }
    const foodList = await response.json();
    // Ensure foodList is always an array
    const foodListArray: food_popup_in[] = JSON.parse(foodList);
    return foodListArray
}

export async function fetchActivities() {
    const response = await fetch("http://localhost:5000/activity_list");
    if (!response.ok) {
        throw new Error('Failed to fetch activities list');
    }
    const activitiesList = await response.json();
    const activitiesListArray: activity_in[] = JSON.parse(activitiesList);
    return activitiesListArray
}

const mockData = [
    {
      user_id: 1,
      date: "2024-05-16",
      duration: 60,
      activity_id: 1,
    },
    {
      user_id: 1,
      date: "2024-05-16",
      duration: 30,
      activity_id: 2,
    },
    // Add more mock activities as needed
  ];

export async function fetchActivitiesFromDay(user_id: number, date: string) {
    const response = await fetch("http://localhost:5000/activity/" + user_id + "/" + date);
    if (!response.ok) {
        throw new Error('Failed to fetch day activities list');
    }
    const activitiesList = await response.json();
    const activitiesListArray: activity_entry[] = JSON.parse(activitiesList);
    return activitiesListArray
}

export async function saveActivity(activityPerformed: activity_out) {
    await fetch("http://localhost:5000/activity_out", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(activityPerformed),
    });
}

export async function saveFood(newFood: food_popup_out) {
    await fetch("http://localhost:5000/popup_food_out", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(newFood),
    });
}