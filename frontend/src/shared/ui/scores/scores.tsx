import React, { useEffect } from "react";

interface WheelProps {
  segments: string[];
  spinning: boolean;
  spinWheel: () => void;
  winnerIndex: number | null;
  wheelRef: React.RefObject<HTMLCanvasElement>;
}

const Wheel: React.FC<WheelProps> = ({
  segments,
  spinning,
  spinWheel,
  winnerIndex,
  wheelRef,
}) => {
  const drawWheel = () => {
    const wheel = wheelRef.current;
    if (!wheel) return;

    const context = wheel.getContext("2d");
    if (!context) return;

    const radius = wheel.width / 2;
    const fontSize = 14;
    const angleStep = (2 * Math.PI) / segments.length;

    context.clearRect(0, 0, wheel.width, wheel.height);
    context.translate(radius, radius);
    context.rotate(-Math.PI / 2);

    segments.forEach((segment, index) => {
      const startAngle = angleStep * index;
      const endAngle = angleStep * (index + 1);

      context.beginPath();
      context.arc(0, 0, radius, startAngle, endAngle);
      context.lineTo(0, 0);

      const colors = ["#FFD700", "#FF6347", "#00BFFF", "#98FB98"];
      const finalColors = segments.map((segment, index) => {
        return colors[index % colors.length];
      });

      context.fillStyle =
        index === winnerIndex
          ? "#c084fc" // Подсвечиваем выигравшую ячейку
          : finalColors[index]; // Применяем равномерно распределенные цвета

      context.fill();

      context.save();
      context.rotate(startAngle + angleStep / 2);
      context.fillStyle = "#fff";
      context.font = `${fontSize}px Arial`;
      context.fillText(segment, radius / 2, 0);
      context.restore();
    });

    context.resetTransform();
  };

  useEffect(() => {
    drawWheel();
  }, []);

  useEffect(() => {
    drawWheel();
  }, [winnerIndex]);

  return (
    <div className="flex flex-col">
      <div
        className="absolute top-[32.5%] left-1/2 z-10 transform -translate-x-1/2"
        style={{
          animation: spinning ? "shake 0.3s ease-in-out infinite" : "none",
        }}
      >
        <div className="w-0 h-0 border-l-[15px] border-l-transparent border-r-transparent border-r-[15px] border-t-[25px] border-t-[#FF3CAC] bg-transparent transform rotate-0 -mt-[10px]"></div>
      </div>

      <canvas
        ref={wheelRef}
        width="400"
        height="400"
        className="mb-6 border-2 border-gray-300 rounded-full shadow-lg"
      ></canvas>

      <button
        onClick={spinWheel}
        disabled={spinning}
        className="px-8 py-3 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 disabled:opacity-50"
      >
        Spin the Wheel
      </button>
    </div>
  );
};

export default Wheel;
