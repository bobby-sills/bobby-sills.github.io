<script lang="ts">
  import koreaderStats from "../../data/koreader-stats.json";

  interface DayData {
    date: string;
    pages: number;
    duration_hours: number;
  }

  let hoveredDay: { date: string; pages: number; minutes: number } | null =
    null;
  let tooltipX = 0;
  let tooltipY = 0;

  const maxColor = "orange";

  function handleMouseEnter(
    event: MouseEvent,
    day: { date: string; pages: number; hours: number },
  ) {
    const rect = (event.target as HTMLElement).getBoundingClientRect();
    tooltipX = rect.left + rect.width / 2;
    tooltipY = rect.top - 10;
    hoveredDay = {
      date: day.date,
      pages: day.pages,
      minutes: Math.round(day.hours * 60),
    };
  }

  function handleMouseLeave() {
    hoveredDay = null;
  }

  function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  }

  // Create a map of dates to pages read
  const statsMap = new Map<string, DayData>();
  koreaderStats.yearly_stats.forEach((stat) => {
    statsMap.set(stat.date, stat);
  });

  // Generate array of all days in the past 6 months
  const generateYearData = () => {
    const today = new Date();
    const sixMonthsAgo = new Date(today);
    sixMonthsAgo.setMonth(today.getMonth() - 6);

    // Align to the start of the week (Sunday)
    const startDate = new Date(sixMonthsAgo);
    const dayOfWeek = startDate.getDay();
    startDate.setDate(startDate.getDate() - dayOfWeek);

    const days: Array<{ date: string; pages: number; hours: number }> = [];
    const current = new Date(startDate);

    while (current <= today) {
      const dateStr = current.toISOString().split("T")[0];
      const stat = statsMap.get(dateStr);
      days.push({
        date: dateStr,
        pages: stat?.pages || 0,
        hours: stat?.duration_hours || 0,
      });
      current.setDate(current.getDate() + 1);
    }

    return days;
  };

  const yearData = generateYearData();

  // Calculate max hours for color intensity scaling
  const maxHours = Math.max(...yearData.map((d) => d.hours));

  // Get color intensity based on time read (returns percentage for color-mix)
  const getIntensity = (hours: number): number => {
    if (hours === 0) return 0;
    return hours / maxHours;
  };

  // Organize days into weeks (Sunday start)
  const organizeIntoWeeks = () => {
    const weeks: Array<Array<{ date: string; pages: number; hours: number }>> =
      [];
    let currentWeek: Array<{ date: string; pages: number; hours: number }> = [];

    yearData.forEach((day) => {
      currentWeek.push(day);
      if (currentWeek.length === 7) {
        weeks.push(currentWeek);
        currentWeek = [];
      }
    });

    // Pad end if needed
    if (currentWeek.length > 0) {
      while (currentWeek.length < 7) {
        currentWeek.push({ date: "", pages: 0, hours: 0 });
      }
      weeks.push(currentWeek);
    }

    return weeks;
  };

  const weeks = organizeIntoWeeks();

  // Month labels
  const getMonthLabels = () => {
    const labels: Array<{ label: string; weekIndex: number }> = [];
    let lastMonth = -1;

    weeks.forEach((week, weekIndex) => {
      const firstValidDay = week.find((d) => d.date !== "");
      if (firstValidDay) {
        const date = new Date(firstValidDay.date);
        const month = date.getMonth();
        if (month !== lastMonth) {
          labels.push({
            label: date.toLocaleString("default", { month: "short" }),
            weekIndex,
          });
          lastMonth = month;
        }
      }
    });

    return labels;
  };

  const monthLabels = getMonthLabels();
</script>

<div class="contribution-graph">
  <h3>reading activity (past 6 months)</h3>

  <div class="graph-container">
    <div class="month-labels">
      {#each monthLabels as { label, weekIndex }}
        <span style="grid-column: {weekIndex + 1};">{label}</span>
      {/each}
    </div>

    <div class="day-labels">
      <span style="grid-row: 2;">Mon</span>
      <span style="grid-row: 4;">Wed</span>
      <span style="grid-row: 6;">Fri</span>
    </div>

    <div class="grid">
      {#each weeks as week, weekIndex}
        {#each week as day, dayIndex}
          {#if day.date}
            <div
              class="day"
              role="button"
              tabindex="0"
              style="background-color: {getIntensity(day.hours) === 0
                ? 'var(--bg2)'
                : `color-mix(in srgb, var(--${maxColor}) ${getIntensity(day.hours) * 100}%, var(--bg2) ${(1 - getIntensity(day.hours)) * 100}%)`};"
              onmouseenter={(e) => handleMouseEnter(e, day)}
              onmouseleave={handleMouseLeave}
            ></div>
          {:else}
            <div class="day empty"></div>
          {/if}
        {/each}
      {/each}
    </div>

    <div class="legend">
      <span>Less</span>
      <div class="legend-squares">
        <div class="day legend-day" style="background-color: var(--bg2);"></div>
        <div
          class="day legend-day"
          style="background-color: color-mix(in srgb, var(--{maxColor}) 25%, var(--bg2) 75%);"
        ></div>
        <div
          class="day legend-day"
          style="background-color: color-mix(in srgb, var(--{maxColor}) 50%, var(--bg2) 50%);"
        ></div>
        <div
          class="day legend-day"
          style="background-color: color-mix(in srgb, var(--{maxColor}) 75%, var(--bg2) 25%);"
        ></div>
        <div class="day legend-day" style="background-color: var(--{maxColor});"></div>
      </div>
      <span>More</span>
    </div>
  </div>
</div>

{#if hoveredDay}
  <div class="tooltip" style="left: {tooltipX}px; top: {tooltipY}px;">
    <div class="tooltip-content">
      {#if hoveredDay.pages === 0}
        <strong>No reading on {formatDate(hoveredDay.date)}</strong>
      {:else}
        <strong
          >{hoveredDay.minutes} minutes on {formatDate(hoveredDay.date)}</strong
        >
      {/if}
    </div>
  </div>
{/if}

<style>
  .contribution-graph {
    margin: 30px 0;
    padding: 20px;
    background-color: var(--bg1);
    border-radius: 6px;
  }

  h3 {
    margin: 0 0 15px 0;
    color: var(--fg);
    font-size: 1rem;
    font-weight: normal;
  }

  .graph-container {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .month-labels {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 15px;
    margin-left: 30px;
    margin-bottom: 5px;
    font-size: 0.7rem;
    color: var(--fg4);
  }

  .day-labels {
    position: absolute;
    top: 30px;
    left: 0;
    display: grid;
    grid-template-rows: repeat(7, 12px);
    gap: 3px;
    font-size: 0.7rem;
    color: var(--fg4);
    text-align: right;
    width: 25px;
  }

  .grid {
    display: grid;
    grid-auto-flow: column;
    grid-template-rows: repeat(7, 12px);
    grid-auto-columns: 12px;
    gap: 3px;
    margin-left: 30px;
  }

  .day {
    width: 12px;
    height: 12px;
    border-radius: 2px;
    transition: all 0.2s ease;
  }

  .day:not(.empty):not(.legend-day):hover {
    cursor: pointer;
    filter: brightness(1.3);
  }

  .day.empty {
    background-color: transparent;
  }

  .legend-day {
    cursor: default;
  }

  .legend {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    justify-content: flex-end;
    font-size: 0.7rem;
    color: var(--fg4);
  }

  .legend-squares {
    display: flex;
    gap: 3px;
  }

  .tooltip {
    position: fixed;
    transform: translate(-50%, -100%);
    pointer-events: none;
    z-index: 1000;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .tooltip-content {
    background-color: var(--bg3);
    color: var(--fg);
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 0.85rem;
    white-space: nowrap;
  }

  .tooltip-content strong {
    display: block;
    font-weight: normal;
  }

  @media (max-width: 600px) {
    .contribution-graph {
      padding: 15px;
      overflow-x: auto;
    }

    .graph-container {
      min-width: 550px;
      position: relative;
      padding-bottom: 50px;
    }

    .legend {
      position: absolute;
      bottom: 0;
      left: 0;
      background-color: var(--bg1);
      padding: 8px;
      border-radius: 4px;
      width: fit-content;
      z-index: 10;
    }
  }
</style>
