import { activity_popup_in, food_popup_in, food_popup_out } from "@/types";

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
        throw new Error('Failed to fetch food list');
    }
    const activitiesList = await response.json();
    const activitiesListArray: activity_popup_in[] = JSON.parse(activitiesList);
    return activitiesListArray
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