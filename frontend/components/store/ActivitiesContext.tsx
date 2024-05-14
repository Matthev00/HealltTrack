"use client";

import {
    ACTIVITIES_REDUCER_ACTION_TYPE,
    ActivitiesContextProps,
    ActivitiesReducerAction,
    ActivitiesReducerState,
} from "@/types";
import dayjs, { Dayjs } from "dayjs";
import { createContext, useReducer } from "react";

const today: Dayjs = dayjs();

const today_formatted = today.format("DD-MM-YYYY");

const ActivitiesContext = createContext<ActivitiesContextProps>({
    actualDate: today_formatted,
    setactualDate: () => { },
});

function ActivitiesReducer(state: ActivitiesReducerState, action: ActivitiesReducerAction) {
    if (action.type === ACTIVITIES_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE) {
        return {
            ...state,
            actualDate: action.newDate,
        }
    }

    return state;
}

export function ActivitiesContextProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const [activities, dispatchActivitiesAction] = useReducer(ActivitiesReducer, {
        actualDate: today_formatted,
    });

    function setactualDate(newDate: string) {
        dispatchActivitiesAction({ type: ACTIVITIES_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE, newDate: newDate });
    }


    const activitiesContext = {
        actualDate: activities.actualDate,
        setactualDate,
    };

    return (
        <ActivitiesContext.Provider value={activitiesContext}>
            {children}
        </ActivitiesContext.Provider>
    );
}

export default ActivitiesContext;