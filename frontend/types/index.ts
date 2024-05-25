

export type food_popup_in = {
    food_id: number,
    name: string,
    serving: number,
    calories_per_100: number,
}

interface Meal {
    kcal: number;
    proteins: number;
    fats: number;
    carbs: number;
    foods: Food[];
}

export type all_foods = {
    Breakfast: Meal;
    Snack: Meal;
    Lunch: Meal;
    Supper: Meal;
    Dinner: Meal;
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

export type activity_in = {
    id: number
    name: string,
    calories_burned_per_hour: number,
}

export type activity_out = {
    user_id: number
    date: string,
    activity_id: number,
    duration: number,
    calories_burned: number,
}

export type activity_entry = {
    time: string,
    activity_name: string,
    duration: number,
    calories_burned: number,
}


export type macros = {
    kcal: number,
    proteins: number,
    fats: number,
    carbs: number,
    water: number,
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
    setActualDate: (newDate: string) => void;
}
  
export interface ActivitiesReducerState {
    actualDate: string;
}

export const enum ACTIVITIES_REDUCER_ACTION_TYPE {
    SET_ACTUAL_DATE,
}
  
export interface ActivitiesReducerAction {
    type: ACTIVITIES_REDUCER_ACTION_TYPE;
    newDate?: string;
}

export interface MainPageContextProps {
    actualDate: string;
    setActualDate: (newDate: string) => void;
}
  
export interface MainPageReducerState {
    actualDate: string;
}

export const enum MAINPAGE_REDUCER_ACTION_TYPE {
    SET_ACTUAL_DATE,
}
  
export interface MainPageReducerAction {
    type: MAINPAGE_REDUCER_ACTION_TYPE;
    newDate?: string;
}

export interface Food {
    name: string;
    calories_per_100g: number;
    proteins_per_100g: number;
    fats_per_100g: number;
    carbohydrates_per_100g: number;
    water_per_100g: number;
    quantity: number;
  }

  export interface delete_food {
    date_time: string,
    food_name: string,
    meal_type: string,
  }
  