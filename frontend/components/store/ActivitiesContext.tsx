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
    setActualDate: () => { },
});

function ActivitiesReducer(state: ActivitiesReducerState, action: ActivitiesReducerAction): ActivitiesReducerState {
    switch (action.type) {
      case ACTIVITIES_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE:
        if (action.newDate) {
          return {
            ...state,
            actualDate: action.newDate,
          };
        }
        break;
      default:
        return state; // return the current state if no action types match
    }
    return state; // return the current state if newDate or newActivity is undefined
}
  
  
export function ActivitiesContextProvider({ children }: { children: React.ReactNode }) {
    const [state, dispatch] = useReducer<React.Reducer<ActivitiesReducerState, ActivitiesReducerAction>>(ActivitiesReducer, {
      actualDate: today_formatted,
    });
  
    function setActualDate(newDate: string) {
      if (newDate) {
        dispatch({ type: ACTIVITIES_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE, newDate });
      }
    }
  
  
    const context = {
      actualDate: state.actualDate,
      setActualDate,
    };
  
    return (
      <ActivitiesContext.Provider value={context}>
        {children}
      </ActivitiesContext.Provider>
    );
}
  

export default ActivitiesContext;