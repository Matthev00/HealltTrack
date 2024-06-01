import { activity_entry, activity_in, activity_out, all_foods, delete_food, food_popup_in, food_popup_out, macros } from "@/types";
import { act } from "react";

type ActualWeight = {
    date_time: string;
    weight: number;
};

export async function fetchFoods() {
    const response = await fetch("http://localhost:5000/popup_food");
    if (!response.ok) {
        throw new Error('Failed to fetch food list');
    }
    const foodList = await response.json();
    const foodListArray: food_popup_in[] = JSON.parse(foodList);
    return foodListArray
}

export async function deleteFood(food: delete_food) {
    await fetch("http://localhost:5000/delete_food", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(food),
    });
}

export async function addActualWeight(weight: string, date: string) {
    console.log(weight, date)
    await fetch("http://localhost:5000/body_measurement/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ weight: weight, date: date }),
    });
}

export async function addGoal(goal: string) {
    await fetch("http://localhost:5000/body_measurement/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ }),
    });
}

export async function fetchActualWeight(date: string) {
    try {
        const response = await fetch("http://localhost:5000/body_measurement/get/" + date);
        if (!response.ok) {
            return "";
        }
        const actualWeight = await response.json();
        return String(actualWeight.weight);
    } catch (error) {
        // Zwracamy pusty string bez logowania błędu
        return "";
    }
}

export async function fetchAllFoods(date: string) {
    const response = await fetch("http://localhost:5000/popup_food/" + date);
    if (!response.ok) {
        throw new Error('Failed to fetch food list');
    }
    const foodList = await response.json();
    // Ensure foodList is always an array
    const foodListArray: all_foods = JSON.parse(foodList);
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

export async function fetchMacrosFromDay(user_id: number, date: string) {
    const response = await fetch("http://localhost:5000/macros/" + user_id + "/" + date);
    if (!response.ok) {
        throw new Error('Failed to fetch day activities list');
    }
    const macrosFromDay = await response.json();
    const macrosFromDayParsed: macros = JSON.parse(macrosFromDay);
    return macrosFromDayParsed
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