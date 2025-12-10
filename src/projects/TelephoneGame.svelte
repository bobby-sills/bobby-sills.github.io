<script lang="ts">
  import Nav from "../lib/Nav.svelte";

  $effect(() => {
    document.title = "telephone game | bobby sills";
  });

  let typedNumbers = $state("");
  let gameStarted = $state(false);

  function playSound(url: string) {
    const audio = new Audio(url);
    audio.play();
  }

  $effect(() => {});
</script>

<main>
  <Nav />
  <h1>telephone game</h1>

  {#if !gameStarted}
    <p>
      call <a href="tel:+14195574228">+1 (419) 557-4228</a> to get started or
      <button
        class="start-button"
        onclick={() => {
          gameStarted = true;
        }}>play the game on in your browser</button
      >
    </p>

    <p style="text-align: center; color: var(--fg2);">please enable sound</p>
  {:else}
    <span>{typedNumbers}</span>

    <div class="keypad">
      {#each ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"] as num}
        <button class="key" onclick={() => (typedNumbers += num)}>{num}</button>
      {/each}
    </div>
  {/if}
</main>

<style>
  span {
    display: block;
    font-size: 1.25rem;
    min-height: 1.5em;
    text-align: center;
    padding: 12px 20px;
  }

  .keypad {
    margin: auto;
    display: grid;
    width: 200px;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }

  .key {
    aspect-ratio: 1;
    width: 100%;
    font-size: 1.25rem;
    font-family: Georgia, "Times New Roman", Times, serif;
    cursor: pointer;
    background-color: var(--bg2);
    border: 1px solid var(--fg);
    color: var(--fg);
  }

  .key:hover {
    background-color: var(--bg2);
  }

  .key:active {
    background-color: var(--bg1);
  }
</style>
