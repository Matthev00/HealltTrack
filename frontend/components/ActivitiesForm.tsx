"use client"

import { ChangeEvent, useContext, useEffect, useState } from "react";
import ActivitiesContext from "./store/ActivitiesContext";
import { activity_out, activity_in } from "@/types";
import { fetchActivities, saveActivity } from "@/utils";

function ActivitiesForm({ onClose }: { onClose: () => void }) {
    const activitiesCtx = useContext(ActivitiesContext);
    const [duration, setDuration] = useState<{ [key: number]: number }>({});
    const [startHour, setStartHour] = useState<{ [key: number]: string }>({});
    const [searchText, setSearchText] = useState("");
    const [activitiesList, setActivitiesList] = useState<activity_in[] | []>([]);

    const getData = async () => {
        const newActivitiesList = await fetchActivities();
        const initialDuration: { [key: number]: number } = {};
        for (const activity of newActivitiesList) {
            initialDuration[activity.id] = 60;
        }
        setDuration(initialDuration)
        setActivitiesList(newActivitiesList)
    };

    useEffect(() => {
        getData()
    }, []);

    const handleSaveActivities = (activityId: number) => {
        const Duration = duration[activityId];
        const StartHour = startHour[activityId]; // use the start hour from state or default to 17:00
        const activityPerformed: activity_out = {
            user_id: 1,
            date: activitiesCtx.actualDate + StartHour,
            activity_id: activityId,
            duration: Duration,
            calories_burned: 0,
        }
        saveActivity(activityPerformed); // Save the activity on your server
        onClose();
    }

    const handleTimeChange = (activityId: number) => (e: ChangeEvent<HTMLInputElement>) => {
        let newValue = parseInt(e.target.value);
        if (isNaN(newValue)) {
            newValue = 1;
        }
        setDuration(prevState => ({
            ...prevState,
            [activityId]: newValue
        }));
    };

    const handleStartHourChange = (activityId: number) => (e: ChangeEvent<HTMLInputElement>) => {
        setStartHour(prevState => ({
            ...prevState,
            [activityId]: e.target.value
        }));
    };

    const filteredActivitiesList = activitiesList.filter(activity =>
        activity.name.toLowerCase().includes(searchText.toLowerCase())
    );

    console.log(filteredActivitiesList);

    return (
        <div>
            <div className="flex justify-between items-center p-4 pb-10">
                <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-blue-200"
                    id="search"
                    type="text"
                    placeholder="Search"
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                />
            </div>
            <div className="overflow-y-auto max-h-[400px]">
                {filteredActivitiesList.length > 0 && filteredActivitiesList.map((activity, index) => (
                    <div key={activity.id} className={`pb-4 ${index !== filteredActivitiesList.length - 1 ? 'mb-8 border-b border-gray5-300' : ''}`} >
                        <div className="flex justify-between">
                            <div className="text-black overflow-wrap break-word max-w-[25rem]">
                                {activity.name} - { Math.round(activity.calories_burned_per_hour * duration[activity.id] / 60)} calories burnt
                            </div>

                            <button className="text-green-400" onClick={() => handleSaveActivities(activity.id)}>+</button>
                        </div>
                        <div className="flex items-center">
                            <input
                                type="number"
                                className="w-16 mr-2 text-center bg-gray-200"
                                value={ duration[activity.id] }
                                min="1"
                                step="1"
                                onChange={handleTimeChange(activity.id)}
                                onKeyDown={(e) => {
                                    if (e.key === '.' || e.key === ',') {
                                        e.preventDefault();
                                    }
                                }}
                            />
                            <span className="text-gray-500">min Started on:</span>
                            <input
                                type="time"
                                className="w-20 ml-2 text-center bg-gray-200"
                                value={ startHour[activity.id] }
                                onChange={handleStartHourChange(activity.id)}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ActivitiesForm;