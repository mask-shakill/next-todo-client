"use client";
import { useRouter } from "next/navigation";
const PrimaryButton = ({ customStyle, url }) => {
  const router = useRouter();
  const handleRedirect = () => {
    console.log(url);
    router.push(url);
  };
  return (
    <button
      onClick={handleRedirect}
      className={`bg-[#50c2c9] ${customStyle} font-bold text-white rounded`}
    >
      Get Started
    </button>
  );
};

export default PrimaryButton;
