"use client";
import { useEffect, useState } from "react";
import TaskCard from "../card/TaskCard";

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/todos/")
      .then((res) => res.json())
      .then((data) => setTasks(data));
  }, []);
  return (
    <div className="mx-10 md:mx-28 mt-5 md:mt-10">
      <h1>Task list</h1>
      <div className=" shadow rounded-lg shadow-lime-500 p-5 md:p-10 mt-4 md:mt-10">
        <div className="flex justify-between">
          <h1>Daily Task</h1>
          <button>+</button>
        </div>
        {/* all tasks  */}
        <div className="">
          {tasks.map((task) => (
            <TaskCard task={task} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default TaskList;
