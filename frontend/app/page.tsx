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

  function changeWeight(value: string) {
    console.log("New weight:", value);
  }
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
              onChange={(event) => {
                let value = event.target.value;
                value = value.replace(/[^0-9,]/g, '');
                if (value.length > 1 && value.charAt(0) === '0') {
                  value = value.substring(1);
                }
                if (value.charAt(0) === ',' || value.charAt(0) === '0') {
                  value = value.substring(1);
                }
                const parts = value.split(',');
                if (parts[0].length > 3) {
                  parts[0] = parts[0].substring(0, 3);
                  value = parts.join(',');
                }
                if ((value.match(/,/g) || []).length > 1) {
                  value = value.replace(/,/g, (match, offset) => offset ? "" : match);
                }
                if (parts.length > 1 && parts[1].length > 2) {
                  parts[1] = parts[1].substring(0, 2);
                  value = parts.join(',');
                }
                event.target.value = value;
                if (value.trim() !== '') {
                  changeWeight(value);
                }
              }}
            />

            <div>kg</div>
          </div>
          <div className="items-center pt-8">Goal weight: </div>
          <div className="flex items-center ">
            <input
              type="text"
              className="pt-2 w-[20%] mr-2"
              onChange={(event) => {
                let value = event.target.value;
                value = value.replace(/[^0-9,]/g, '');
                if (value.length > 1 && value.charAt(0) === '0') {
                  value = value.substring(1);
                }
                if (value.charAt(0) === ',' || value.charAt(0) === '0') {
                  value = value.substring(1);
                }
                const parts = value.split(',');
                if (parts[0].length > 3) {
                  parts[0] = parts[0].substring(0, 3);
                  value = parts.join(',');
                }
                if ((value.match(/,/g) || []).length > 1) {
                  value = value.replace(/,/g, (match, offset) => offset ? "" : match);
                }
                if (parts.length > 1 && parts[1].length > 2) {
                  parts[1] = parts[1].substring(0, 2);
                  value = parts.join(',');
                }
                event.target.value = value;
                if (value.trim() !== '') {
                  changeWeight(value);
                }
              }}
            />

            <div>kg</div>
          </div>
        </div> 

      </div>
    </div>




  );
}




