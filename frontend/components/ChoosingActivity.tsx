"use client";

import ActivitiesForm from "./ActivitiesForm";

const ChoosingActivity = ({ onClose, onActivityAdded }: { onClose: () => void, onActivityAdded: () => void }) => {

    return (
        <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 z-50 flex justify-center items-center"
            onClick={(e) => {
                e.preventDefault();
                if (e.target === e.currentTarget) {
                    onClose();
                }
            }}>
            <div className="w-[30rem] h-[40rem] max-w-[30rem] bg-white rounded-lg px-6 py-6 relative">
                <div className="flex justify-center pb-4 relative">
                    <button onClick={() => onClose()} className="absolute top-0 right-0 text-red-500">x</button>
                </div>
                <ActivitiesForm onClose={onClose} onActivityAdded={onActivityAdded}/>
            </div>
        </div>

    )
}

export default ChoosingActivity;
