"use client";

import {
    MAINPAGE_REDUCER_ACTION_TYPE,
    MainPageContextProps,
    MainPageReducerAction,
    MainPageReducerState,
} from "@/types";
import dayjs, { Dayjs } from "dayjs";
import { createContext, useReducer } from "react";

const today: Dayjs = dayjs();

const today_formatted = today.format("DD-MM-YYYY");

const MainPageContext = createContext<MainPageContextProps>({
    actualDate: today_formatted,
    setActualDate: () => { },
});

function MainPageReducer(state: MainPageReducerState, action: MainPageReducerAction): MainPageReducerState {
    switch (action.type) {
      case MAINPAGE_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE:
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
  
  
export function MainPageContextProvider({ children }: { children: React.ReactNode }) {
    const [state, dispatch] = useReducer<React.Reducer<MainPageReducerState, MainPageReducerAction>>(MainPageReducer, {
      actualDate: today_formatted,
    });
  
    function setActualDate(newDate: string) {
      if (newDate) {
        dispatch({ type: MAINPAGE_REDUCER_ACTION_TYPE.SET_ACTUAL_DATE, newDate });
      }
    }
  
    const context = {
      actualDate: state.actualDate,
      setActualDate,
    };
  
    return (
      <MainPageContext.Provider value={context}>
        {children}
      </MainPageContext.Provider>
    );
}
  

export default MainPageContext;