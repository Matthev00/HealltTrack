"use client"

import ChoosingFood from "@/components/ChoosingFood";
import MealPlanContext from "@/components/store/MealPlanContext";
import { useContext, useState } from "react";

export default function MealPlan() {
  const mealPlanCtx = useContext(MealPlanContext);
  const [choosingFood, setChoosingFood] = useState<boolean>(false);
  const [mealType, setMealType] = useState<string>("");

  const choosingFoodHandler = (mealType: string) => {
    setMealType(mealType)
    setChoosingFood(true)
  };

  return <div className=" w- full h-full">
    <div>
      {mealPlanCtx.actualDate}
    </div>

    <div className="flex w-full h-[95%]  justify-center pt-6">
      <div className="flex-1 border-r text-center">
        <span className="">Śniadanie</span>
        <button
          onClick={() => {
            choosingFoodHandler("Śniadanie");
          }}
          className="ml-2 text-green-400">+</button>
      </div>
      <div className="flex-1 border-r text-center">
        <span className="">Lunch</span>
        <button
          onClick={() => {
            choosingFoodHandler("Lunch");
          }}
          className="ml-2 text-green-400">+</button>
      </div>
      <div className="flex-1 border-r text-center">
        <span className="">Obiad</span>
        <button
          onClick={() => {
            choosingFoodHandler("Obiad");
          }}
          className="ml-2 text-green-400">+</button>
      </div>
      <div className="flex-1 border-r text-center">
        <span className="">Przekąska</span>
        <button
          onClick={() => {
            choosingFoodHandler("Przekąska");
          }}
          className="ml-2 text-green-400">+</button>
      </div>
      <div className="flex-1 text-center">
        <span className="">Kolacja</span>
        <button
          onClick={() => {
            choosingFoodHandler("Kolacja");
          }}
          className="ml-2 text-green-400">+</button>
      </div>
    </div>

    {choosingFood && <ChoosingFood onClose={() => setChoosingFood(false)} mealType={mealType} />}
  </div>
}
