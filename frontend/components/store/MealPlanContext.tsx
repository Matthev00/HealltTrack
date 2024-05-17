"use client";

import {
    MEALPLAN_REDUCER_ACTION_TYPE,
    MealPlanContextProps,
    MealPlanReducerAction,
    MealPlanReducerState
} from "@/types";
import dayjs, { Dayjs } from "dayjs";
import { createContext, useReducer } from "react";

const today: Dayjs = dayjs();

const today_formatted = today.format("DD-MM-YYYY");

const MealPlanContext = createContext<MealPlanContextProps>({
    actualDate: today_formatted,
    setactualDate: () => { },
});

function MealPlanReducer(state: MealPlanReducerState, action: MealPlanReducerAction) {
    if (action.type === MEALPLAN_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE) {
        return {
            ...state,
            actualDate: action.newDate,
        }
    }



    return state;
}

export function MealPlanContextProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const [mealPlan, dispatchMealPlanAction] = useReducer(MealPlanReducer, {
        actualDate: today_formatted,
    });

    function setactualDate(newDate: string) {
        dispatchMealPlanAction({ type: MEALPLAN_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE, newDate: newDate });
    }


    const mealPlanContext = {
        actualDate: mealPlan.actualDate,
        setactualDate,
    };

    return (
        <MealPlanContext.Provider value={mealPlanContext}>
            {children}
        </MealPlanContext.Provider>
    );
}

export default MealPlanContext;