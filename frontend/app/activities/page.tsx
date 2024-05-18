"use client"

import ChoosingActivity from "@/components/ChoosingActivity";
import ActivitiesContext from "@/components/store/ActivitiesContext";
import { activity_entry } from "@/types";
import { fetchActivitiesFromDay } from "@/utils";
import { useContext, useEffect, useState } from "react";

export default function Activities() {
  const activitiesCtx = useContext(ActivitiesContext);
  const [choosingActivity, setChoosingActivity] = useState<boolean>(false);
  const [performedActivities, setPerformedActivities] = useState<activity_entry[]>([]);

  const choosingActivityHandler = () => {
    setChoosingActivity(true);
  }

  const onActivityAdded = () => {
    setChoosingActivity(false);
    fetchActivitiesFromDay(1, activitiesCtx.actualDate).then(setPerformedActivities);
  }

  useEffect(() => {
    fetchActivitiesFromDay(1, activitiesCtx.actualDate).then(setPerformedActivities);
  }, [activitiesCtx.actualDate, choosingActivity]);

  return (
    <div className="w-full h-full">
      <div className="flex w-full h-[15%] justify-center pt-6">
        <div className="flex-1 border-r text-center">
          <span className="">{activitiesCtx.actualDate}</span>
          <button
            onClick={choosingActivityHandler}
            className="ml-2 text-green-400">+</button>
        </div>
      </div>

      <div>
        {performedActivities.map((activity : activity_entry) => (
          <div key={activity.activity_name} className="activity-entry">
            <h3 className="activity-name">{activity.activity_name}</h3>
            <p className="activity-date">Started on: {activity.time}</p>
            <p className="activity-duration">Duration: {activity.duration} minutes</p>
            <p className="calories-burned">Calories burned: {activity.calories_burned} kcal</p>
          </div>
        ))}
      </div>

      {choosingActivity && (
        <ChoosingActivity
          onClose={() => setChoosingActivity(false)}
          onActivityAdded={onActivityAdded}
        />
      )}
    </div>
  );
}

