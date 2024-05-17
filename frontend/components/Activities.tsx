"use client"

import { ChangeEvent, useContext, useEffect, useState } from "react";
import ActivitiesContext from "./store/ActivitiesContext";

function Activities({ onClose, activityType }: { onClose: () => void, activityType: string }) {
    const activitiesCtx = useContext(ActivitiesContext);
    const [searchText, setSearchText] = useState("");

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
        </div>
    );
}

export default Activities;