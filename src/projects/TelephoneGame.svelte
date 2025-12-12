<script lang="ts">
  import Nav from "../lib/Nav.svelte";
  import { playDialTone } from "../lib/dtmf";
  import { fetchAllStories } from "../lib/stories";
  import { StoryPlayer, type GameState } from "../lib/storyPlayer";

  $effect(() => {
    document.title = "telephone game | bobby sills";
  });

  let phoneInput = $state("");
  let gameStarted = $state(false);
  let gameState = $state<GameState>({ phase: "loading" });
  let player: StoryPlayer | null = null;
  let showText = $state(false);

  // Initialize the story player when game starts
  $effect(() => {
    if (gameStarted && !player) {
      player = new StoryPlayer((state) => {
        gameState = state;
      });

      // Load stories from GitHub
      fetchAllStories()
        .then((stories) => {
          player?.loadStories(stories);
        })
        .catch((error) => {
          console.error("Failed to load stories:", error);
        });
    }

    return () => {
      player?.destroy();
    };
  });

  function handleKeyPress(key: string) {
    playDialTone(key);
    phoneInput += key;

    // Handle story navigation based on game state
    if (gameState.phase === "menu") {
      const storyIndex = parseInt(key);
      if (storyIndex >= 1 && storyIndex <= 3) {
        player?.selectStory(storyIndex);
      }
    } else if (gameState.phase === "playing") {
      const choiceIndex = parseInt(key);
      const maxChoices = gameState.currentSection.choices?.length || 0;
      if (choiceIndex >= 1 && choiceIndex <= maxChoices) {
        player?.makeChoice(choiceIndex);
      }
    }
  }

  // Clear input after 5 seconds of inactivity
  $effect(() => {
    if (phoneInput.length > 0) {
      const timeout = setTimeout(() => {
        phoneInput = "";
      }, 1000);

      return () => clearTimeout(timeout);
    }
  });

  function restartGame() {
    phoneInput = "";
    gameStarted = false;
    player?.destroy();
    player = null;
    gameState = { phase: "loading" };
  }
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
        }}>play in your browser</button
      >
    </p>

    <p style="text-align: center; color: var(--fg2);">please enable sound</p>
  {:else}
    <div class="game-container">
      {#if gameState.phase === "menu"}
        <div class="story-menu">
          {#if showText}
            <p>welcome to the telephone gamebook</p>
            <ul>
              {#each gameState.stories as story, index}
                <li>
                  press <strong>{index + 1}</strong> to begin the story titled
                  {story.title.toLowerCase()}
                </li>
              {/each}
            </ul>
          {/if}
        </div>
      {:else if gameState.phase === "playing"}
        <div class="playing">
          {#if showText}
            <div class="section-text">
              <p>{gameState.currentSection.text}</p>
            </div>
            {#if gameState.currentSection.choices}
              <div class="choices">
                <ul>
                  {#each gameState.currentSection.choices as choice, index}
                    <li>
                      press <strong>{index + 1}</strong> to
                      {choice.label.toLowerCase()}
                    </li>
                  {/each}
                </ul>
              </div>
            {/if}
          {/if}
        </div>
      {:else if gameState.phase === "ended"}
        <div class="ended">
          {#if showText}
            <div class="ending-text">
              <p>{gameState.endingSection.text}</p>
            </div>
          {/if}
          <button class="restart-button" onclick={restartGame}>
            restart
          </button>
        </div>
      {/if}

      <span class="phone-display">{phoneInput}</span>

      <div class="keypad">
        {#each ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"] as num}
          <button class="key" onclick={() => handleKeyPress(num)}>{num}</button>
        {/each}
      </div>

      <button class="toggle-text-button" onclick={() => (showText = !showText)}>
        {showText ? "hide text" : "show text"}
      </button>
    </div>
  {/if}
</main>

<style>
  ul {
    list-style-type: "- ";
  }

  .game-container {
    max-width: 600px;
    margin: 0 auto;
  }

  .phone-display {
    display: block;
    font-size: 1.25rem;
    min-height: 1.5em;
    text-align: center;
  }

  .playing,
  .ended {
    margin-bottom: 0px;
  }

  .section-text,
  .ending-text {
    margin-bottom: 20px;
  }

  .section-text p,
  .ending-text > p {
    margin: 0;
  }

  .choices {
    margin-top: 20px;
  }

  .restart-button,
  .toggle-text-button {
    display: block;
    margin: 10px auto;
    text-align: center;
  }

  .keypad {
    margin: 12px auto;
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
    background-color: var(--bg1);
  }

  .key:active {
    background-color: var(--bg1);
    border-color: var(--fg);
  }
</style>
