"use client";

import MainPageContext from "@/components/store/MainPageContext";
import { macros } from "@/types";
import { addActualWeight, fetchActualWeight, fetchMacrosFromDay, addGoalWeight, fetchGoal } from "@/utils";
import { useContext, useEffect, useState } from "react";
import { PieChart } from 'react-minimal-pie-chart';
// ... other imports

export default function MainPage() {
  const mainPageCtx = useContext(MainPageContext);
  const [inputValue, setInputValue] = useState<string>("");
  const [goalValue, setGoalValue] = useState<string>("");
  const [debouncedValue, setDebouncedValue] = useState<string>("");
  const [debouncedGoalValue, setDebouncedGoalValue] = useState<string>("");
  const [dayMacros, setDayMacros] = useState<macros>({
    kcal: 0,
    proteins: 0,
    fats: 0,
    carbs: 0,
    water: 0,
  });
  const [weightDifference, setWeightDifference] = useState<number | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const macrosData = await fetchMacrosFromDay(1, mainPageCtx.actualDate);
        setDayMacros(macrosData);
        const weightData = await fetchActualWeight(mainPageCtx.actualDate);
        setInputValue(weightData);
        const goal = await fetchGoal();
        setGoalValue(goal); // Reset goal weight when date changes
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [mainPageCtx.actualDate]);

  useEffect(() => {
    const inputHandler = setTimeout(() => {
      setDebouncedValue(inputValue);
    }, 3000); // 3000 ms = 3 seconds

    return () => {
      clearTimeout(inputHandler);
    };
  }, [inputValue]);

  useEffect(() => {
    if (debouncedValue.trim() !== '') {
      addActualWeight(debouncedValue, mainPageCtx.actualDate);
      updateWeightDifference(debouncedValue, goalValue);
    }
  }, [debouncedValue]);

  useEffect(() => {
    const goalHandler = setTimeout(() => {
      setDebouncedGoalValue(goalValue);
    }, 3000); // 3000 ms = 3 seconds

    return () => {
      clearTimeout(goalHandler);
    };
  }, [goalValue]);

  useEffect(() => {
    if (debouncedGoalValue.trim() !== '') {
      addGoalWeight(debouncedGoalValue);
      updateWeightDifference(inputValue, debouncedGoalValue);
    }
  }, [debouncedGoalValue]);

  const updateWeightDifference = (actualWeight: string, goalWeight: string) => {
    const actual = parseFloat(actualWeight);
    const goal = parseFloat(goalWeight);
    if (!isNaN(actual) && !isNaN(goal)) {
      const difference = goal - actual;
      setWeightDifference(difference);
    } else {
      setWeightDifference(null);
    }
  };

  const chartData = (['proteins', 'fats', 'carbs'] as (keyof macros)[]).map((key, i) => ({
    title: key,
    value: dayMacros[key],
    color: `hsl(${i * (360 / 3)}, 70%, 50%)`,
  }));

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    let value = event.target.value;
    // Remove non-numeric characters and leading zeros
    value = value.replace(/[^0-9.]/g, '').replace(/^0+(?!$)/, '');

    // Remove leading dot
    if (value.charAt(0) === '.') {
      value = value.substring(1);
    }

    const parts = value.split('.');

    // Limit digits before dot to 3
    if (parts[0].length > 3) {
      parts[0] = parts[0].substring(0, 3);
      value = parts.join('.');
    }

    // Limit only one dot
    if ((value.match(/\./g) || []).length > 1) {
      value = value.replace(/\./g, (match, offset) => offset ? "" : match);
    }

    // Limit digits after dot to 2
    if (parts.length > 1 && parts[1].length > 2) {
      parts[1] = parts[1].substring(0, 2);
      value = parts.join('.');
    }
    setInputValue(value);
  };

  const handleGoalChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    let value = event.target.value;
    // Remove non-numeric characters and leading zeros
    value = value.replace(/[^0-9.]/g, '').replace(/^0+(?!$)/, '');

    // Remove leading dot
    if (value.charAt(0) === '.') {
      value = value.substring(1);
    }

    const parts = value.split('.');

    // Limit digits before dot to 3
    if (parts[0].length > 3) {
      parts[0] = parts[0].substring(0, 3);
      value = parts.join('.');
    }

    // Limit only one dot
    if ((value.match(/\./g) || []).length > 1) {
      value = value.replace(/\./g, (match, offset) => offset ? "" : match);
    }

    // Limit digits after dot to 2
    if (parts.length > 1 && parts[1].length > 2) {
      parts[1] = parts[1].substring(0, 2);
      value = parts.join('.');
    }

    setGoalValue(value);
  };

  return (
    <div className="w-full h-full flex-col">
      <div className="flex w-full justify-center pt-6">
        <div className="flex-1 border-r text-center">
          <span>{mainPageCtx.actualDate}</span>
          <div>Kcal: {dayMacros.kcal}</div>
          <div>Water: {dayMacros.water} ml</div>
        </div>
      </div>

      <div className="flex items-start justify-around pt-12">
        <div className="flex w-[50%] h-[85%] pt-6 ml-12">
          <div className="flex justify-start" style={{ width: '70%', height: '70%' }}>
            <div style={{ width: '80%' }}>
              <PieChart
                data={chartData}
                label={({ dataEntry }) => `${dataEntry.title}: ${dataEntry.value}`}
                labelStyle={{ fontSize: '7px' }}
              />
            </div>
          </div>
        </div>

        <div className="flex flex-col w-[40%] pt-20">
          <div className="items-center">Actual weight: </div>
          <div className="flex items-center ">
            <input
              type="text"
              className="pt-2 w-[20%] mr-2"
              value={inputValue}
              onChange={handleChange}
            />
            <div>kg</div>
          </div>
          <div className="items-center pt-8">Goal weight: </div>
          <div className="flex items-center ">
            <input
              type="text"
              className="pt-2 w-[20%] mr-2"
              value={goalValue}
              onChange={handleGoalChange}
            />
            <div>kg</div>
          </div>
          <div className="items-center pt-8">
            You need to{" "}
            {weightDifference !== null && (
              <span>
                {weightDifference > 0
                  ? `gain ${weightDifference.toFixed(2)} kg`
                  : `lose ${Math.abs(weightDifference).toFixed(2)} kg`}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
