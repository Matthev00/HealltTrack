"use client"

import ChoosingFood from "@/components/ChoosingFood";
import MealPlanContext from "@/components/store/MealPlanContext";
import { all_foods, delete_food, Food } from "@/types";
import { deleteFood, fetchAllFoods } from "@/utils";
import { useContext, useEffect, useState } from "react";

export default function MealPlan() {
  const mealPlanCtx = useContext(MealPlanContext);
  const [choosingFood, setChoosingFood] = useState<boolean>(false);
  const [mealType, setMealType] = useState<string>("");
  const [deletingFood, setdeletingFood] = useState(false);
  const [allFoods, setAllFoods] = useState<all_foods>({
    "Breakfast": {
      "kcal": 0,
      "proteins": 0,
      "fats": 0,
      "carbs": 0,
      "foods": []
    },
    "Supper": {
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
    "Snack": {
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

  async function deleteFoodItem(meal_type: string, food_name: string) {
    const food: delete_food = {
      date_time: mealPlanCtx.actualDate,
      meal_type: meal_type,
      food_name: food_name,
    }
    await deleteFood(food);
    setdeletingFood(true)
  };

  useEffect(() => {
    getAllMeals();
  }, [mealPlanCtx.actualDate]);

  useEffect(() => {
    getAllMeals();
    getAllMeals();
    getAllMeals();
    getAllMeals()
    getAllMeals()
  }, [choosingFood]);

  useEffect(() => {
    getAllMeals();
    getAllMeals();
    getAllMeals();
    setdeletingFood(false);
  }, [deletingFood]);

  return (
    <div className="w-full h-full">
      <div>
        {mealPlanCtx.actualDate}
      </div>
      <div className="flex w-full h-[95%] justify-center pt-6 ">

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
          <div>
            {allFoods.Breakfast.kcal < 0.2 ? 0 : allFoods.Breakfast.kcal.toFixed(1)} kcal
          </div>
          <div>proteins: {allFoods.Breakfast.proteins} g</div>
          <div>fats: {allFoods.Breakfast.fats} g</div>
          <div>carbs: {allFoods.Breakfast.carbs} g</div>

          <div className="mt-8 text-left mr-4 overflow-y-auto max-h-[600px]">
            {allFoods.Breakfast.foods.map((food: Food, index: number) => (
              <div key={index} className="mb-4 p-4 border border-gray-200 rounded shadow-sm">
                <div className="flex items-center" >
                  <h3 className="text-xl font-bold">{food.name}</h3>
                  <button className="text-red-500" onClick={() => deleteFoodItem("Breakfast", food.name)}>x</button>
                </div>
                <p>{food.quantity} g</p>
                <div className="flex">
                  <p>
                    {(food.calories_per_100g * food.quantity / 100 < 0.2 ? 0 : (food.calories_per_100g * food.quantity / 100).toFixed(1))} kcal
                  </p>

                  <p className="ml-4">p: {(food.proteins_per_100g * food.quantity / 100).toFixed(1)} </p>
                  <p className="ml-4">f: {(food.fats_per_100g * food.quantity / 100).toFixed(1)}</p>
                  <p className="ml-4">c: {(food.carbohydrates_per_100g * food.quantity / 100).toFixed(1)}</p>
                </div>
              </div>
            ))}
          </div>

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
          <div>
            {allFoods.Lunch.kcal < 0.2 ? 0 : allFoods.Lunch.kcal.toFixed(1)} kcal
          </div>
          <div>proteins: {allFoods.Lunch.proteins} g</div>
          <div>fats: {allFoods.Lunch.fats} g</div>
          <div>carbs: {allFoods.Lunch.carbs} g</div>

          <div className="mt-8 text-left mr-4 ml-4 overflow-y-auto max-h-[600px]">
            {allFoods.Lunch.foods.map((food: Food, index: number) => (
              <div key={index} className="mb-4 p-4 border border-gray-200 rounded shadow-sm">
                <div className="flex items-center" >
                  <h3 className="text-xl font-bold">{food.name}</h3>
                  <button className="text-red-500" onClick={() => deleteFoodItem("Lunch", food.name)} >x</button>
                </div>
                <p>{food.quantity} g</p>
                <div className="flex">
                  <p>
                    {(food.calories_per_100g * food.quantity / 100 < 0.2 ? 0 : (food.calories_per_100g * food.quantity / 100).toFixed(1))} kcal
                  </p>

                  <p className="ml-4">p: {(food.proteins_per_100g * food.quantity / 100).toFixed(1)} </p>
                  <p className="ml-4">f: {(food.fats_per_100g * food.quantity / 100).toFixed(1)}</p>
                  <p className="ml-4">c: {(food.carbohydrates_per_100g * food.quantity / 100).toFixed(1)}</p>
                </div>
              </div>
            ))}
          </div>

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
          <div>
            {allFoods.Dinner.kcal < 0.2 ? 0 : allFoods.Dinner.kcal.toFixed(1)} kcal
          </div>
          <div>proteins: {allFoods.Dinner.proteins} g</div>
          <div>fats: {allFoods.Dinner.fats} g</div>
          <div>carbs: {allFoods.Dinner.carbs} g</div>

          <div className="mt-8 text-left mr-4 ml-4 overflow-y-auto max-h-[600px]">
            {allFoods.Dinner.foods.map((food: Food, index: number) => (
              <div key={index} className="mb-4 p-4 border border-gray-200 rounded shadow-sm">
                <div className="flex items-center" >
                  <h3 className="text-xl font-bold">{food.name}</h3>
                  <button className="text-red-500" onClick={() => deleteFoodItem("Dinner", food.name)}>x</button>
                </div>
                <p>{food.quantity} g</p>
                <div className="flex">
                  <p>
                    {(food.calories_per_100g * food.quantity / 100 < 0.2 ? 0 : (food.calories_per_100g * food.quantity / 100).toFixed(1))} kcal
                  </p>

                  <p className="ml-4">p: {(food.proteins_per_100g * food.quantity / 100).toFixed(1)} </p>
                  <p className="ml-4">f: {(food.fats_per_100g * food.quantity / 100).toFixed(1)}</p>
                  <p className="ml-4">c: {(food.carbohydrates_per_100g * food.quantity / 100).toFixed(1)}</p>
                </div>
              </div>
            ))}
          </div>

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
          <div>
            {allFoods.Snack.kcal < 0.2 ? 0 : allFoods.Snack.kcal.toFixed(1)} kcal
          </div>
          <div>proteins: {allFoods.Snack.proteins} g</div>
          <div>fats: {allFoods.Snack.fats} g</div>
          <div>carbs: {allFoods.Snack.carbs} g</div>

          <div className="mt-8 text-left mr-4 ml-4 overflow-y-auto max-h-[600px]">
            {allFoods.Snack.foods.map((food: Food, index: number) => (
              <div key={index} className="mb-4 p-4 border border-gray-200 rounded shadow-sm">
                <div className="flex items-center" >
                  <h3 className="text-xl font-bold">{food.name}</h3>
                  <button className="text-red-500" onClick={() => deleteFoodItem("Snack", food.name)}>x</button>
                </div>
                <p>{food.quantity} g</p>
                <div className="flex">
                  <p>
                    {(food.calories_per_100g * food.quantity / 100 < 0.2 ? 0 : (food.calories_per_100g * food.quantity / 100).toFixed(1))} kcal
                  </p>

                  <p className="ml-4">p: {(food.proteins_per_100g * food.quantity / 100).toFixed(1)} </p>
                  <p className="ml-4">f: {(food.fats_per_100g * food.quantity / 100).toFixed(1)}</p>
                  <p className="ml-4">c: {(food.carbohydrates_per_100g * food.quantity / 100).toFixed(1)}</p>
                </div>
              </div>
            ))}
          </div>

        </div>

        <div className="flex-1 border-r text-center ">
          <span>Supper</span>
          <button
            onClick={() => {
              choosingFoodHandler("Supper");
            }}
            className="ml-2 text-green-400"
          >
            +
          </button>
          <div>
            {allFoods.Supper.kcal < 0.2 ? 0 : allFoods.Supper.kcal.toFixed(1)} kcal
          </div>
          <div>proteins: {allFoods.Supper.proteins} g</div>
          <div>fats: {allFoods.Supper.fats} g</div>
          <div>carbs: {allFoods.Supper.carbs} g</div>

          <div className="mt-8 text-left mr-4 ml-4 overflow-y-auto max-h-[600px]">
            {allFoods.Supper.foods.map((food: Food, index: number) => (
              <div key={index} className="mb-4 p-4 border border-gray-200 rounded shadow-sm">
                <div className="flex items-center" >
                  <h3 className="text-xl font-bold">{food.name}</h3>
                  <button className="text-red-500" onClick={() => deleteFoodItem("Supper", food.name)}>x</button>
                </div>
                <p>{food.quantity} g</p>
                <div className="flex">
                  <p>
                    {(food.calories_per_100g * food.quantity / 100 < 0.5 ? 0 : (food.calories_per_100g * food.quantity / 100).toFixed(1))} kcal
                  </p>

                  <p className="ml-4">p: {(food.proteins_per_100g * food.quantity / 100).toFixed(1)} </p>
                  <p className="ml-4">f: {(food.fats_per_100g * food.quantity / 100).toFixed(1)}</p>
                  <p className="ml-4">c: {(food.carbohydrates_per_100g * food.quantity / 100).toFixed(1)}</p>
                </div>
              </div>
            ))}
          </div>

        </div>


      </div>

      {choosingFood && <ChoosingFood onClose={() => setChoosingFood(false)} mealType={mealType} />}
    </div >
  );
}
