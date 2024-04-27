"use client"

import ChoosingFood from "@/components/ChoosingFood";
import ActivitiesContext from "@/components/store/ActivitiesContext";
import { useContext, useState } from "react";

export default function Activities() {
  const activitiesCtx = useContext(ActivitiesContext);
  //const [choosingFood, setChoosingFood] = useState<boolean>(false);
  //const [mealType, setMealType] = useState<string>("");

  // const choosingFoodHandler = (mealType: string) => {
  //   setMealType(mealType)
  //   setChoosingFood(true)
  // };

  return <div className=" w- full h-full">

    <div className="flex w-full h-[95%]  justify-center pt-6">
      <div className="flex-1 border-r text-center">
        <span className="">{activitiesCtx.actualDate}</span>
        <button
          onClick={() => {
            //choosingFoodHandler("Today");
          }}
          className="ml-2 text-green-400">+</button>
      </div>
    </div>

  </div>
}
