"use client"

import { food_popup_in } from "@/types";
import { fetchFoods } from "@/utils";
import { ChangeEvent, useEffect, useState } from "react";

function Foods() {
    const [values, setValues] = useState<{ [key: number]: number }>({});
    const [searchText, setSearchText] = useState("");
    const [foodList, setFoodList] = useState<food_popup_in[] | []>([]);

    const getData = async () => {
        const newFoodList = await fetchFoods();
        setFoodList(newFoodList)
      };
    
      useEffect(() => {
        getData()
      }, []);

    const handleChange = (foodId: number) => (e: ChangeEvent<HTMLInputElement>) => {
        let newValue = parseInt(e.target.value);
        if (isNaN(newValue)) {
            newValue = 1;
        }
        setValues(prevState => ({
            ...prevState,
            [foodId]: newValue
        }));
    };

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
                    <div key={food.food_id} className={`pb-4 ${index !== filteredFoodList.length - 1 ? 'mb-8 border-b border-gray-300' : ''}`} >
                        <div className="flex justify-between">
                            <div className="text-black overflow-wrap break-word max-w-[25rem]">{food.name} - {food.calories_per_100 * food.serving / 100} kalorii</div>
                            <button className="text-green-400">+</button>
                        </div>
                        <div className="flex items-center">
                            <input
                                type="number"
                                className="w-16 mr-2 text-center bg-gray-200"
                                value={values[food.food_id] || 1}
                                min="1"
                                step="1"
                                onChange={handleChange(food.food_id)}
                            />
                            <span className="text-gray-500">x</span>
                            <select className="ml-2">
                                <option>porcja ({food.serving}g)</option>
                                <option>g</option>
                            </select>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Foods;
