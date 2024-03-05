import Image from "next/image";
import circleImage from "@/assets/images/circle.png";
import TaskList from "@/components/all-tasks/TaskList";

const Todo = () => {
  return (
    <>
      {/* first section for profile  */}
      <section>
        <div className="bg-[#50c2c9] w-full h-[350px] flex flex-col items-center justify-center relative">
          <Image className="absolute top-0 left-0" src={circleImage}></Image>
          <div className="flex flex-col items-center justify-center gap-y-2">
            <img
              className=" rounded-full h-28 w-28"
              src="https://img.freepik.com/premium-photo/nothing-can-be-done-without-hope-confidence-shot-young-man-standing-modern-office_590464-53623.jpg?w=360"
              alt=""
            />
            <h1>Welcome to Mr. Shakil</h1>
          </div>
        </div>
      </section>

      {/* section two for all task list  */}
      <section>
        <TaskList />
      </section>
    </>
  );
};

export default Todo;
