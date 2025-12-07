<script lang="ts">
  const {
    title,
    author,
    percent,
    totalPages,
    dateCompleted,
  }: {
    title: string;
    author: string;
    percent: number;
    totalPages: number;
    dateCompleted?: string;
  } = $props();

  const isCompleted = () => percent >= 100 || dateCompleted;
</script>

<div class="book-container">
  <div id="book-information">
    <div style="display: flex; flex-direction: column; gap: 5px;">
      <span style="color: var(--fg); font-size: larger;">{title}</span>
      <span style="color: var(--fg4);">by {author}</span>
    </div>
    {#if isCompleted()}
      <span style="color: var(--fg4);">completed {dateCompleted}</span>
    {:else}
      <span style="color: var(--fg); font-size: larger;"
        >{Math.ceil((percent / 100) * totalPages)}/{totalPages} pages</span
      >
    {/if}
  </div>
  {#if !isCompleted()}
    <div id="progress-bar">
      <div style:width="{percent}%" id="progress-fill"></div>
    </div>
  {/if}
</div>

<style>
  .book-container {
    margin-bottom: 20px;
  }

  #book-information {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 10px;
  }

  #progress-bar {
    height: 10px;
    width: 100%;
    margin: 10px 0px;
    background-color: var(--bg3);
    overflow: hidden;
    border-radius: 999px;
  }

  #progress-fill {
    height: 100%;
    background-color: var(--green);
    border-radius: 999px;
  }
</style>
