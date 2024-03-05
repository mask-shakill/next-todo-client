import React from "react";

const TaskCard = ({ task }) => {
  return (
    <div className="flex items-center justify-between border shadow p-2 md:p-3 mt-2 rounded">
      <h1>{task.title}</h1>
      <button>delete</button>
    </div>
  );
};

export default TaskCard;
