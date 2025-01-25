import clsx from "clsx";
import React, { useEffect } from "react";

interface WheelProps {
  segments: Array<{ title: string; reward_id: number }>;
  spinning: boolean;
  winnerIndex: number | null;
  wheelRef: React.RefObject<HTMLCanvasElement>;
}

const Wheel: React.FC<WheelProps> = ({
  segments,
  winnerIndex,
  wheelRef,
  spinning,
}) => {
  const drawWheel = () => {
    const wheel = wheelRef.current;
    if (!wheel) return;

    const context = wheel.getContext("2d");
    if (!context) return;

    const radius = wheel.width / 2;
    const fontSize = 14;

    context.clearRect(0, 0, wheel.width, wheel.height);
    context.translate(radius, radius);
    context.rotate(-Math.PI / 2);

    const gap = 0.077;
    const totalAngle = Math.PI * 2;
    const segmentAngle = (totalAngle - gap * segments.length) / segments.length;
    const heightFactor = 2.3;

    segments.forEach((segment, index) => {
      const startAngle = index * (segmentAngle + gap);
      const endAngle = startAngle + segmentAngle;

      const outerRadius = radius * heightFactor;

      const innerRadius = radius * 0.55;

      const colors = ["#41AE6D", "#FFB719"];
      const finalColors = segments.map((_, i) => colors[i % colors.length]);

      context.beginPath();

      context.arc(0, 0, outerRadius, startAngle, endAngle, false);

      context.lineTo(
        Math.cos(endAngle) * innerRadius,
        Math.sin(endAngle) * innerRadius
      );

      context.arc(0, 0, innerRadius, endAngle, startAngle, true);

      context.closePath();

      context.fillStyle =
        index === winnerIndex ? "#c084fc" : finalColors[index];
      context.fill();

      context.save();
      context.rotate(startAngle + segmentAngle / 2);
      context.translate((outerRadius + innerRadius) / 2, 0);
      context.rotate(Math.PI / 2);
      context.fillStyle = "#fff";
      context.font = `${fontSize}px Arial`;
      context.textAlign = "center";
      context.fillText(segment.title, (innerRadius + outerRadius) / 2, 0);
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
    <div className="flex flex-col relative">
      <img
        className={clsx(
          "absolute top-[110px] left-[165px]",
          spinning && "animate-pulse"
        )}
        src="/images/score/Polygon 1.png"
      />
      <img
        className={clsx(
          "absolute top-32 left-32 ",
          spinning && "animate-pulse"
        )}
        src="/images/score/Ellipse 11.png"
      />
      <span className="absolute top-[168px] left-[156px] text-gray-600">
        Крутить
      </span>
      <span className="absolute top-[185px] left-[159px] text-gray-600">
        колесо
      </span>
      <canvas
        ref={wheelRef}
        width="370"
        height="370"
        className="mb-6 rounded-full shadow-lg"
      ></canvas>
    </div>
  );
};

export default Wheel;
