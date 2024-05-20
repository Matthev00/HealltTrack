"use client"

import { food_popup_in, food_popup_out } from "@/types";
import { fetchFoods, saveFood } from "@/utils";
import { ChangeEvent, useContext, useEffect, useState } from "react";
import MealPlanContext from "./store/MealPlanContext";

function Foods({ onClose, mealType }: { onClose: () => void, mealType: string }) {
    const mealPlanCtx = useContext(MealPlanContext);
    const [amount, setAmount] = useState<{ [key: number]: number }>({});
    const [grams, setGrams] = useState<{ [key: number]: number }>({});
    const [searchText, setSearchText] = useState("");
    const [foodList, setFoodList] = useState<food_popup_in[] | []>([]);

    const getData = async () => {
        const newFoodList = await fetchFoods();
        const initialGrams: { [key: number]: number } = {};
        const initialAmount: { [key: number]: number } = {};
        for (const food of newFoodList) {
            initialAmount[food.food_id] = 1;
            initialGrams[food.food_id] = food.serving;
        }
        setAmount(initialAmount)
        setGrams(initialGrams);
        setFoodList(newFoodList)
    };

    useEffect(() => {
        getData()
    }, []);

    const handleSaveFood = (foodId: number) => {
        const quantity = parseFloat((grams[foodId] * amount[foodId]).toFixed(1));
        const foodToSave: food_popup_out = {
            date_time: mealPlanCtx.actualDate,
            food_id: foodId,
            quantity: quantity,
            meal_type: mealType,
        }
        
        saveFood(foodToSave)
        onClose();

    }

    const handleAmountChange = (foodId: number) => (e: ChangeEvent<HTMLInputElement>) => {
        let newValue = parseInt(e.target.value);
        if (isNaN(newValue)) {
            newValue = 1;
        }
        setAmount(prevState => ({
            ...prevState,
            [foodId]: newValue
        }));
    };

    const handleSelectChange = (selectedOption: string, foodId: number) => {
        if (selectedOption === 'serving') {
            for (const food of foodList) {
                if (foodId === food.food_id) {
                    setGrams(prevState => ({
                        ...prevState,
                        [foodId]: food.serving
                    }))
                }
            }

        } else if (selectedOption === 'grams') {
            for (const food of foodList) {
                if (foodId === food.food_id) {
                    setGrams(prevState => ({
                        ...prevState,
                        [foodId]: 1
                    }))
                }
            }
        }
    }


    const filteredFoodList = foodList.filter(food =>
        food.name.toLowerCase().includes(searchText.toLowerCase())
    );

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
                {filteredFoodList.length > 0 && filteredFoodList.map((food, index) => (
                    <div key={food.food_id} className={`pb-4 ${index !== filteredFoodList.length - 1 ? 'mb-8 border-b border-gray5-300' : ''}`} >
                        <div className="flex justify-between">
                            <div className="text-black overflow-wrap break-word max-w-[25rem]">
                                {food.name} - {Math.round(food.calories_per_100 * parseFloat((grams[food.food_id] * amount[food.food_id]).toFixed(1)) / 100)} kalorii
                            </div>

                            <button className="text-green-400" onClick={() => handleSaveFood(food.food_id)}>+</button>
                        </div>
                        <div className="flex items-center">
                            <input
                                type="number"
                                className="w-16 mr-2 text-center bg-gray-200"
                                value={amount[food.food_id] }
                                min="1"
                                step="1"
                                onChange={handleAmountChange(food.food_id)}
                                onKeyDown={(e) => {
                                    if (e.key === '.' || e.key === ',') {
                                        e.preventDefault();
                                    }
                                }}
                            />
                            <span className="text-gray-500">x</span>
                            <select className="ml-2" onChange={(event) => handleSelectChange(event.target.value, food.food_id)}>
                                <option value="serving">porcja ({food.serving}g)</option>
                                <option value="grams">g</option>
                            </select>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Foods;
