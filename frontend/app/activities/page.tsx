"use client"

import ChoosingActivity from "@/components/ChoosingActivity";
import ActivitiesContext from "@/components/store/ActivitiesContext";
import { useContext, useState } from "react";

export default function Activities() {
  const activitiesCtx = useContext(ActivitiesContext);
  const [choosingActivity, setChoosingActivity] = useState<boolean>(false);
  const [activityType, setActivityType] = useState<string>("");

  const choosingActivityHandler = () => {
    setChoosingActivity(true)
  }

  return <div className=" w- full h-full">

    <div className="flex w-full h-[95%]  justify-center pt-6">
      <div className="flex-1 border-r text-center">
        <span className="">{activitiesCtx.actualDate}</span>
        <button
          onClick={() => {
            choosingActivityHandler();
          }}
          className="ml-2 text-green-400">+</button>
      </div>
    </div>
    

    {choosingActivity && <ChoosingActivity onClose={() => setChoosingActivity(false)} activityType={activityType} />}
  </div>
}
