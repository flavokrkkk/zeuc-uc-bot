export const spinWheel = (
  segments: Array<{ title: string; reward_id: number; type: string }>,
  wheelRef: React.MutableRefObject<HTMLCanvasElement | null>,
  spinning: boolean,
  onFinished: (
    winner: { title: string; reward_id: number; type: string },
    winnerIndex: number
  ) => void,
  setSpinning: (action: boolean) => void,
  setWinnerIndex: (action: number | null) => void
) => {
  setWinnerIndex(null);
  if (spinning) return;

  setSpinning(true);

  const wheel = wheelRef.current;
  if (!wheel) return;

  const angleStep = 360 / segments.length;
  const duration = 4000;
  const startTime = Date.now();

  const randomSpin = Math.floor(Math.random() * 360) + 360 * 3;
  const rotationAngle = randomSpin;

  const spinInterval = setInterval(() => {
    const elapsedTime = Date.now() - startTime;
    const progress = Math.min(elapsedTime / duration, 1);

    const easedProgress = 1 - Math.pow(1 - progress, 3);

    const spinAngle = rotationAngle * easedProgress;
    wheel.style.transform = `rotate(${spinAngle}deg) scale(${
      1 + 0.05 * easedProgress
    })`;

    if (elapsedTime >= duration) {
      clearInterval(spinInterval);

      const finalAngle = ((spinAngle % 360) + 360) % 360;

      const finalSegmentAngles = segments.map((_segment, index) => {
        const segmentAngle = (index * angleStep + finalAngle) % 360;
        const resultFixed = segmentAngle.toFixed(0);
        return resultFixed;
      });

      const winningSegmentIndex = finalSegmentAngles.findIndex((angle) => {
        return Number(angle) >= 310;
      });
      setWinnerIndex(winningSegmentIndex);
      onFinished(segments[winningSegmentIndex], winningSegmentIndex);
      setSpinning(false);

      setWinnerIndex(winningSegmentIndex);
      onFinished(segments[winningSegmentIndex], winningSegmentIndex);
      setSpinning(false);
    }
  }, 16);
};
