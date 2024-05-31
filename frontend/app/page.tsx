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
          <div className=" items-center ">Actual weight: </div>
          <div className=" items-center pt-20 ">You only need to : </div>
        </div>
      </div>
    </div>




  );
}




