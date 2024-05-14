"use client"

import { ChangeEvent, useContext, useEffect, useState } from "react";
import ActivitiesContext from "./store/ActivitiesContext";
import { activity_popup_in } from "@/types";
import { fetchActivities } from "@/utils";

function Activities({ onClose, activityType }: { onClose: () => void, activityType: string }) {
    const activitiesCtx = useContext(ActivitiesContext);
    const [time, setTime] = useState<{ [key: number]: number }>({});
    const [searchText, setSearchText] = useState("");
    const [activitiesList, setActivitiesList] = useState<activity_popup_in[] | []>([]);

    const getData = async () => {
        const newActivitiesList = await fetchActivities();
        const initialTime: { [key: number]: number } = {};
        for (const activity of newActivitiesList) {
            initialTime[activity.activity_id] = 60;
        }
        setTime(initialTime)
        setActivitiesList(newActivitiesList)
    };

    useEffect(() => {
        getData()
    }, []);

    const handleSaveActivities = () => {
    }

    const handleTimeChange = (activityId: number) => (e: ChangeEvent<HTMLInputElement>) => {
        let newValue = parseInt(e.target.value);
        if (isNaN(newValue)) {
            newValue = 1;
        }
        setTime(prevState => ({
            ...prevState,
            [activityId]: newValue
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
                    <div key={activity.activity_id} className={`pb-4 ${index !== filteredActivitiesList.length - 1 ? 'mb-8 border-b border-gray5-300' : ''}`} >
                        <div className="flex justify-between">
                            <div className="text-black overflow-wrap break-word max-w-[25rem]">
                                {activity.name} - { Math.round(activity.calories_burned_per_hour * time[activity.activity_id] / 60)} calories burnt
                            </div>

                            <button className="text-green-400" onClick={() => handleSaveActivities()}>+</button>
                        </div>
                        <div className="flex items-center">
                            <input
                                type="number"
                                className="w-16 mr-2 text-center bg-gray-200"
                                value={ time[activity.activity_id] }
                                min="1"
                                step="1"
                                onChange={handleTimeChange(activity.activity_id)}
                                onKeyDown={(e) => {
                                    if (e.key === '.' || e.key === ',') {
                                        e.preventDefault();
                                    }
                                }}
                            />
                            <span className="text-gray-500">min</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Activities;