"use client";

import { ChangeEvent, useState } from "react";

const ChoosingFood = ({ onClose, mealType }: { onClose: () => void, mealType: string; }) => {
    const [value, setValue] = useState(1);

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        let newValue = parseInt(e.target.value);
        
        // Sprawdzenie, czy wprowadzona wartość jest liczbą
        if (isNaN(newValue)) {
            // Jeśli nie jest liczbą, ustaw wartość na 1
            newValue = 1;
        }
        setValue(newValue);
    };

    return <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 z-50 flex justify-center items-center"
        onClick={(e) => {
            e.preventDefault();
            if (e.target === e.currentTarget) {
                onClose();
            }
        }}>
        <div className="w-[30rem] h-[40rem] max-w-[30rem] bg-white rounded-lg px-6 py-6 relative">
            <div className="flex justify-center pb-4 relative">
                <div>{mealType}</div>
                <button onClick={() => onClose()} className="absolute top-0 right-0 text-red-500">x</button>
            </div>
            <div className="flex justify-between items-center p-4 pb-10">
                <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-blue-200"
                    id="search"
                    type="text"
                    placeholder="Search"
                />
            </div>

            <div>
                <div className="flex justify-between">
                    <div className="text-black overflow-wrap break-word max-w-[25rem]">Banan</div>
                    <button className="text-green-400">+</button>
                </div>
                <div className="flex items-center">
                    <input
                        type="number"
                        className="w-16 mr-2 text-center bg-gray-200"
                        value={value}
                        min="1"
                        step="1"
                        onChange={handleChange} 
                    />
                    <span className="text-gray-500">x</span>
                    <select className="ml-2">
                        <option>porcja (580g)</option>
                        <option>g</option>
                    </select>
                </div>
            </div>
        </div>
    </div>


}

export default ChoosingFood;