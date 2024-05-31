"use client";

import React, { useContext, useState } from 'react';
import { usePathname } from "next/navigation";
import { Box, Typography } from '@mui/material'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import dayjs, { Dayjs } from 'dayjs';
import MealPlanContext from './store/MealPlanContext';
import ActivitiesContext from './store/ActivitiesContext';
import MainPageContext from './store/MainPageContext';


function Sidebar() {
    const pathname = usePathname();
    const inactiveColor = "bg-blue-600";
    const activeColor = "bg-blue-800";
    const today: Dayjs = dayjs();
    const mealPlanCtx = useContext(MealPlanContext);
    const activitiesCtx = useContext(ActivitiesContext);
    const mainPageCtx = useContext(MainPageContext);
    const [selectedDate, setSelectedDate] = useState<Dayjs>(today);

    const handleDateChangeMealPlan = (newDate: Dayjs | null) => {
        if (newDate !== null) {
            setSelectedDate(newDate);
            mealPlanCtx.setactualDate(newDate.format("DD-MM-YYYY"));
              
          }
    };

    const handleDateChangeActivities = (newDate: Dayjs | null) => {
        if (newDate !== null) {
            setSelectedDate(newDate);
            activitiesCtx.setActualDate(newDate.format("DD-MM-YYYY"));
          }
    };

    const handleDateChangeMainPage = (newDate: Dayjs | null) => {
        if (newDate !== null) {
            setSelectedDate(newDate);
            mainPageCtx.setActualDate(newDate.format("DD-MM-YYYY"));
          }
    };

    return (
        <nav className="relative w-60 bg-[#222f3d] border-2 border-[#BFA181] rounded-lg">
            <div className="container flex items-center justify-center my-5">
                APP
            </div>

            <ul className="container flex flex-col font-bold items-center">
                <a href="/" target="_self" rel="noreferrer" className="w-5/6 text-center">
                    <button className={`${pathname == "/" ? activeColor : inactiveColor}` + " hover:bg-blue-900 w-full relative my-2 text-white font-bold py-2 px-5 rounded-lg"} >User</button>
                </a>
                <a href="/meal_plan" target="_self" rel="noreferrer" className="w-5/6 text-center">
                    <button className={`${pathname == "/meal_plan" ? activeColor : inactiveColor}` + " hover:bg-blue-900 w-full relative my-2 text-white font-bold py-2 px-5 rounded-lg"}>Meal plan</button>
                </a>
                <a href="/activities" target="_self" rel="noreferrer" className="w-5/6 text-center">
                    <button className={`${pathname == "/activities" ? activeColor : inactiveColor}` + " hover:bg-blue-900 w-full relative my-2 text-white font-bold py-2 px-5 rounded-lg"}>Activities</button>
                </a>
                

                <div className={`${pathname == "/" ? 'block' : 'hidden'}`}>

                    <Box style={{ backgroundColor: 'white', marginTop: '20px' }}>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DatePicker format="DD-MM-YYYY" views={["year", "month", "day"]} value={selectedDate} onChange={handleDateChangeMainPage} label={<span style={{ color: 'blue', fontWeight: 'bold', fontSize: '20px' }}></span>} />
                        </LocalizationProvider>
                    </Box>

                </div>

                <div className={`${pathname == "/meal_plan" ? 'block' : 'hidden'}`}>

                    <Box style={{ backgroundColor: 'white', marginTop: '20px' }}>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DatePicker format="DD-MM-YYYY" views={["year", "month", "day"]} value={selectedDate} onChange={handleDateChangeMealPlan} label={<span style={{ color: 'blue', fontWeight: 'bold', fontSize: '20px' }}></span>} />
                        </LocalizationProvider>
                    </Box>

                </div>

                <div className={`${pathname == "/activities" ? 'block' : 'hidden'}`}>

                    <Box style={{ backgroundColor: 'white', marginTop: '20px' }}>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DatePicker format="DD-MM-YYYY" views={["year", "month", "day"]} value={selectedDate} onChange={handleDateChangeActivities} label={<span style={{ color: 'blue', fontWeight: 'bold', fontSize: '20px' }}></span>} />
                        </LocalizationProvider>
                    </Box>

                </div>
            </ul>
        </nav>
    );
}

export default Sidebar;
