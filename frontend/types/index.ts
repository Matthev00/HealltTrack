

export type food_popup_in = {
    food_id: number,
    name: string,
    serving: number,
    calories_per_100: number,
}

export type food_popup_out = {
    date_time: string,
    food_id: number,
    quantity: number,
    meal_type: string,
}

export type food = {
    food_id: number,
    name: string,
    serving: number,
    quantity: number,
    amount: number,
    calories: number,
    proteins: number,
    fats: number,
    carbohydrates: number,
}

export type meal = {
    meal_id: number
    meal_type: string,
    warter_consumption: number,
    calories: number,
    proteins: number,
    fats: number,
    carbohydrates: number,
    food: food[]
}

export type meal_entry = {
    date_time: string,
    meal: meal[],
}

export type activity_popup_in = {
    activity_id: number
    name: string,
    calories_burned_per_hour: number,
}

export interface MealPlanContextProps {
    actualDate: string;
    setactualDate: (newDate: string) => void;
}

export interface MealPlanReducerState {
    actualDate: string;
}

export const enum MEALPLAN_REDUCER_ACTION_TYPE {
    SET_ACTUAL_DATE,
}
export interface MealPlanReducerAction {
    type: MEALPLAN_REDUCER_ACTION_TYPE;
    newDate: string,
}

export interface ActivitiesContextProps {
    actualDate: string;
    setactualDate: (newDate: string) => void;
}

export interface ActivitiesReducerState {
    actualDate: string;
}

export const enum ACTIVITIES_REDUCER_ACTION_TYPE {
    SET_ACTUAL_DATE,
}

export interface ActivitiesReducerAction {
    type: ACTIVITIES_REDUCER_ACTION_TYPE;
    newDate: string,
}