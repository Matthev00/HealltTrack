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

  useEffect(() => {
    fetchActivitiesFromDay().then(setPerformedActivities);
  }, []);

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
          <div key={activity.activity_id} className="activity-entry">
            <h3 className="activity-name">{/* Replace this with the actual activity name */}Activity Name</h3>
            <p className="activity-date">Date: {activity.date}</p>
            <p className="activity-duration">Duration: {activity.duration} minutes</p>
          </div>
        ))}
      </div>

      {choosingActivity && (
        <ChoosingActivity
          onClose={() => setChoosingActivity(false)}
        />
      )}
    </div>
  );
}
