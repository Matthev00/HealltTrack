import { food_popup_in, food_popup_out } from "@/types";

export async function fetchFoods() {
    const response = await fetch("http://localhost:5000/popup_food");
    if (!response.ok) {
        throw new Error('Failed to fetch food list');
    }
    const foodList = await response.json();
    // Ensure foodList is always an array
    const foodListArray: food_popup_in[] = JSON.parse(foodList);
    console.log(foodListArray)
    return foodListArray
}

export async function saveFood(newFood: food_popup_out) {
    // await fetch("", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(newFood),
    // });
    console.log(newFood)
}