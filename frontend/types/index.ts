export type date_time = `${number}${number}-${number}${number}-${number}${number}${number}${number}`;

export type food_popup_in = {
    food_id: number,
    name: string,
    serving: number,
}

export type food_popup_out = {
    date_time: date_time,
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
    date_time: date_time,
    meal: meal[],
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