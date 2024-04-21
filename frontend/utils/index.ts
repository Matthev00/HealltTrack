import { food_popup_in } from "@/types";

const foodList: food_popup_in[] = [
    {
        food_id: 1,
        name: "Pizza",
        serving: 1,
        calories_per_100: 100,
    },
    {
        food_id: 2,
        name: "Salad",
        serving: 2,
        calories_per_100: 100,
    },
    {
        food_id: 3,
        name: "Pasta",
        serving: 1.5,
        calories_per_100: 100,
    },
    {
        food_id: 4,
        name: "Pasta",
        serving: 1.5,
        calories_per_100: 100,
    },
    {
        food_id: 5,
        name: "Pasta",
        serving: 1.5,
        calories_per_100: 100,
    },
];

export async function fetchFoods() {
    //const responce = await fetch("");
    //const foodList: food_popup_in[] = await responce.json();
    return foodList;
  }