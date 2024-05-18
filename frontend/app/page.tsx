"use client"

import MainPageContext from "@/components/store/MainPageContext";
import { useContext } from "react";

export default function MainPage() {
  const mainPageCtx = useContext(MainPageContext);

  return (
    <div className="w-full h-full">
      <div className="flex w-full h-[15%] justify-center pt-6">
        <div className="flex-1 border-r text-center">
          <span className="">{mainPageCtx.actualDate}</span>
        </div>
      </div>
    </div>
  );
}
