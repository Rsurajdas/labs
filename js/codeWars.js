function formatDuration(seconds) {
  if (!seconds) return "now";
  if (seconds < 60) return `${seconds} second${seconds > 1 ? "s" : ""}`;
  const unitsInSeconds = {
    year: 31536000,
    day: 86400,
    hour: 3600,
    minute: 60,
  };
  let remainingSeconds = seconds;
  const durationComponents = [];
  for (const [key, value] of Object.entries(unitsInSeconds)) {
    const duration = Math.floor(remainingSeconds / value);
    remainingSeconds = Math.floor(remainingSeconds % value);
    if (duration) {
      durationComponents.push(`${duration} ${key}${duration > 1 ? "s" : ""}`);
    }
    if (!remainingSeconds) break;
  }
  if (remainingSeconds) {
    durationComponents.push(
      `${remainingSeconds} second${remainingSeconds > 1 ? "s" : ""}`,
    );
  }
  if (durationComponents.length === 1) {
    return durationComponents[0];
  }

  return `${durationComponents.slice(0, -1).join(", ")} and ${durationComponents.at(-1)}`;
}

console.log(formatDuration(43535));
