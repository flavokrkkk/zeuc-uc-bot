import clsx from "clsx";
import React, { useEffect } from "react";

interface WheelProps {
  segments: Array<{ title: string; reward_id: number; type: string }>;
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
      context.fillStyle = "black";

      const lines = segment.title.split("\n");
      const lineHeight = 12;

      lines.forEach((line, i) => {
        context.font = `${
          segment.type === "discount"
            ? "bold 10px Arial"
            : "bold " + fontSize + "px Arial"
        }`;
        context.textAlign = "center";

        context.shadowColor = "rgba(0, 0, 0, 0.5)";
        context.shadowOffsetX = 1;
        context.shadowOffsetY = 1;
        context.shadowBlur = 2;

        context.fillText(line, 0, i * lineHeight + 110);

        context.shadowColor = "transparent";

        context.strokeStyle = "#19614a";
        context.lineWidth = 1;
        context.strokeText(line, 0, i * lineHeight + 110);
      });

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
      <div className="relative flex items-center justify-center">
        <img
          className={clsx(
            "absolute top-32 left-[122px]",
            spinning && "animate-pulse"
          )}
          src="/images/score/Ellipse 11.png"
          alt="Circle"
        />
        <img
          className={clsx(
            "absolute top-[110px] left-[156px]",
            spinning && "animate-pulse"
          )}
          src="/images/score/Polygon 1.png"
          alt="Arrow"
        />
        <span className="absolute top-[167px] left-[155px] text-2xl font-bold text-white">
          Spin
        </span>
      </div>
      <canvas
        ref={wheelRef}
        width="360"
        height="360"
        className="mb-6 rounded-full shadow-lg"
      ></canvas>
    </div>
  );
};

export default Wheel;
