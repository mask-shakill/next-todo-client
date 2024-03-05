import Image from "next/image";
import circleImage from "@/assets/images/circle.png";
import imageHome from "@/assets/images/home.png";
import PrimaryButton from "@/components/button/PrimaryButton";

const HomePage = () => {
  return (
    <>
      {/* First section */}
      <section>
        <div>
          <Image
            className="w-[200px] h-[200px] md:w-[300px] md:h-[300px]"
            src={circleImage}
          />
        </div>
      </section>

      {/* Second section */}
      <section className="flex flex-col items-center justify-center">
        <div>
          <Image src={imageHome} />
        </div>
        <div className="mx-16 md:mx-64">
          <h1 className="text-center font-bold mt-10 md:text-2xl text-xl">
            Gets Things with TODOs
          </h1>
          <p className="text-center mt-5">
            I am making a to-do list app using Next.js for how it looks
            (frontend) and Django for how it works (backend). This way, we get
            the coolness of Next.js making things look good and the strong
            backend abilities of Django.
          </p>
          <div className="text-center mt-8">
            <PrimaryButton url="/todo" customStyle="py-3 px-10" />
          </div>
        </div>
      </section>
    </>
  );
};

export default HomePage;
