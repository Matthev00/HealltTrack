"use client"

import MainPageContext from "@/components/store/MainPageContext";
import { macros } from "@/types";
import { fetchMacrosFromDay } from "@/utils";
import { useContext, useEffect, useState } from "react";
import { PieChart } from 'react-minimal-pie-chart';
// ... other imports

export default function MainPage() {
  const mainPageCtx = useContext(MainPageContext);
  const [dayMacros, setDayMacros] = useState<macros>({
    kcal: 0,
    proteins: 0,
    fats: 0,
    carbs: 0,
    water: 0,
  });

  useEffect(() => {
    fetchMacrosFromDay(1, mainPageCtx.actualDate).then(setDayMacros);
  }, [mainPageCtx.actualDate]);

  // Prepare data for the chart
  const chartData = (['proteins', 'fats', 'carbs'] as (keyof macros)[]).map((key, i) => ({
    title: key,
    value: dayMacros[key],
    color: `hsl(${i * (360 / 3)}, 70%, 50%)`,
  }));  


  return (
    <div className="w-full h-full">
      <div className="flex w-full h-[15%] justify-center pt-6">
        <div className="flex-1 border-r text-center">
          <span className="">{mainPageCtx.actualDate}</span>
          <div>Kcal: {dayMacros.kcal}</div>
          <div>Water: {dayMacros.water} ml</div>
        </div>
      </div>
      <div className="flex w-full h-[85%] justify-center pt-6">
        <div style={{ width: '70%', height: '70%', marginLeft: '-50%' }}>
        <PieChart 
          data={chartData} 
          label={({ dataEntry }) => `${dataEntry.title}: ${dataEntry.value}`}
          labelStyle={{ fontSize: '7px' }} // Increase this value to make the font bigger
        />
        </div>
      </div>
    </div>
  );
}




