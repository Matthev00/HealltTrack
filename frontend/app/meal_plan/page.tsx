"use client"

import ChoosingFood from "@/components/ChoosingFood";
import MealPlanContext from "@/components/store/MealPlanContext";
import { all_foods } from "@/types";
import { fetchAllFoods } from "@/utils";
import { useContext, useEffect, useState } from "react";

export default function MealPlan() {
  const mealPlanCtx = useContext(MealPlanContext);
  const [choosingFood, setChoosingFood] = useState<boolean>(false);
  const [mealType, setMealType] = useState<string>("");
  const [allFoods, setAllFoods] = useState<all_foods>({
    "Breakfast": {
        "kcal": 0,
        "proteins": 0,
        "fats": 0,
        "carbs": 0,
        "foods": []
    },
    "Second breakfast": {
        "kcal": 0,
        "proteins": 0,
        "fats": 0,
        "carbs": 0,
        "foods": []
    },
    "Lunch": {
        "kcal": 0,
        "proteins": 0,
        "fats": 0,
        "carbs": 0,
        "foods": []
    },
    "Afternoon snack": {
        "kcal": 0,
        "proteins": 0,
        "fats": 0,
        "carbs": 0,
        "foods": []
    },
    "Dinner": {
        "kcal": 0,
        "proteins": 0,
        "fats": 0,
        "carbs": 0,
        "foods": []
    }
  });

  const choosingFoodHandler = (mealType: string) => {
    setMealType(mealType)
    setChoosingFood(true)
  };

  async function getAllMeals() {
    try {
      const allMeals = await fetchAllFoods(mealPlanCtx.actualDate);
      setAllFoods(allMeals)
    } catch (error) {
      console.error('Error fetching all meals:', error);
      throw error;
    }
  }

  useEffect(() => {
    getAllMeals();
  }, [mealPlanCtx.actualDate]);

  useEffect(() => {
      getAllMeals();
      getAllMeals();
      getAllMeals();
  }, [choosingFood]);

  return (
    <div className="w-full h-full">
      <div>
        {mealPlanCtx.actualDate}
      </div>
      <div className="flex w-full h-[95%] justify-center pt-6">
        <div className="flex-1 border-r text-center">
          <span>Breakfast</span>
          <button
            onClick={() => {
              choosingFoodHandler("Breakfast");
            }}
            className="ml-2 text-green-400"
          >
            +
          </button>
          <div>{allFoods.Breakfast.kcal} kcal</div>
          <div>proteins: {allFoods.Breakfast.proteins} g</div>
          <div>fats: {allFoods.Breakfast.fats} g</div>
          <div>carbs: {allFoods.Breakfast.carbs} g</div>
        </div>
        <div className="flex-1 border-r text-center">
          <span>Lunch</span>
          <button
            onClick={() => {
              choosingFoodHandler("Lunch");
            }}
            className="ml-2 text-green-400"
          >
            +
          </button>
          <div>{allFoods.Lunch.kcal} kcal</div>
          <div>proteins: {allFoods.Lunch.proteins} g</div>
          <div>fats: {allFoods.Lunch.fats} g</div>
          <div>carbs: {allFoods.Lunch.carbs} g</div>
        </div>
        <div className="flex-1 border-r text-center">
          <span>Dinner</span>
          <button
            onClick={() => {
              choosingFoodHandler("Dinner");
            }}
            className="ml-2 text-green-400"
          >
            +
          </button>
          <div>{allFoods.Dinner.kcal} kcal</div>
          <div>proteins: {allFoods.Dinner.proteins} g</div>
          <div>fats: {allFoods.Dinner.fats} g</div>
          <div>carbs: {allFoods.Dinner.carbs} g</div>
        </div>
        <div className="flex-1 border-r text-center">
          <span>Snack</span>
          <button
            onClick={() => {
              choosingFoodHandler("Snack");
            }}
            className="ml-2 text-green-400"
          >
            +
          </button>
          <div>{allFoods["Afternoon snack"].kcal} kcal</div>
          <div>proteins: {allFoods["Afternoon snack"].proteins} g</div>
          <div>fats: {allFoods["Afternoon snack"].fats} g</div>
          <div>carbs: {allFoods["Second breakfast"].carbs} g</div>
        </div>
        <div className="flex-1 text-center">
          <span>Supper</span>
          <button
            onClick={() => {
              choosingFoodHandler("Supper");
            }}
            className="ml-2 text-green-400"
          >
            +
          </button>
        </div>
      </div>

      {choosingFood && <ChoosingFood onClose={() => setChoosingFood(false)} mealType={mealType} />}
    </div>
  );
}
