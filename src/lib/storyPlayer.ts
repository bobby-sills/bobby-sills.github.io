import type { Story, StorySection } from './stories';
import { getAudioUrl, getWelcomeAudioUrl } from './stories';

export type GameState =
  | { phase: 'loading' }
  | { phase: 'menu'; stories: Story[] }
  | { phase: 'playing'; story: Story; currentSection: StorySection; sectionId: string }
  | { phase: 'ended'; story: Story; endingSection: StorySection };

export class StoryPlayer {
  private state: GameState = { phase: 'loading' };
  private currentAudio: HTMLAudioElement | null = null;
  private onStateChange?: (state: GameState) => void;

  constructor(onStateChange?: (state: GameState) => void) {
    this.onStateChange = onStateChange;
  }

  /**
   * Initializes the player with available stories
   */
  loadStories(stories: Story[]): void {
    this.state = { phase: 'menu', stories };
    this.playWelcomeAudio();
    this.notifyStateChange();
  }

  /**
   * Plays the welcome menu audio
   */
  private playWelcomeAudio(): void {
    const welcomeUrl = getWelcomeAudioUrl();
    this.playAudio(welcomeUrl);
  }

  /**
   * Starts playing a story by index (1-based, as users press 1, 2, 3)
   */
  selectStory(storyIndex: number): void {
    if (this.state.phase !== 'menu') {
      console.warn('Cannot select story - not in menu phase');
      return;
    }

    const story = this.state.stories[storyIndex - 1];
    if (!story) {
      console.warn(`Invalid story index: ${storyIndex}`);
      return;
    }

    this.startStory(story);
  }

  /**
   * Starts playing a specific story
   */
  private startStory(story: Story): void {
    const firstSection = story.sections[story.start_section];

    this.state = {
      phase: 'playing',
      story,
      currentSection: firstSection,
      sectionId: story.start_section
    };

    this.playCurrentSection();
    this.notifyStateChange();
  }

  /**
   * Processes a user's choice (1-based index)
   */
  makeChoice(choiceIndex: number): void {
    if (this.state.phase !== 'playing') {
      console.warn('Cannot make choice - not in playing phase');
      return;
    }

    const { story, currentSection } = this.state;

    if (!currentSection.choices || currentSection.choices.length === 0) {
      console.warn('Current section has no choices');
      return;
    }

    const choice = currentSection.choices[choiceIndex - 1];
    if (!choice) {
      console.warn(`Invalid choice index: ${choiceIndex}`);
      return;
    }

    const nextSectionId = choice.next_id;
    const nextSection = story.sections[nextSectionId];

    if (!nextSection) {
      console.error(`Next section not found: ${nextSectionId}`);
      return;
    }

    // Check if it's an ending
    if (nextSection.is_ending) {
      this.state = {
        phase: 'ended',
        story,
        endingSection: nextSection
      };
    } else {
      this.state = {
        phase: 'playing',
        story,
        currentSection: nextSection,
        sectionId: nextSectionId
      };
    }

    this.playCurrentSection();
    this.notifyStateChange();
  }

  /**
   * Plays the audio for the current section
   */
  private playCurrentSection(): void {
    this.stopAudio();

    if (this.state.phase === 'playing') {
      const { story, sectionId } = this.state;
      const audioUrl = getAudioUrl(story.id, sectionId);
      this.playAudio(audioUrl);
    } else if (this.state.phase === 'ended') {
      const { story, endingSection } = this.state;
      // Find the section ID for the ending
      const endingSectionId = Object.entries(story.sections).find(
        ([_, section]) => section === endingSection
      )?.[0];

      if (endingSectionId) {
        const audioUrl = getAudioUrl(story.id, endingSectionId);
        this.playAudio(audioUrl);
      }
    }
  }

  /**
   * Plays an audio file from URL
   */
  private playAudio(url: string): void {
    this.currentAudio = new Audio(url);
    this.currentAudio.play().catch(error => {
      console.error('Failed to play audio:', error);
    });
  }

  /**
   * Stops currently playing audio
   */
  private stopAudio(): void {
    if (this.currentAudio) {
      this.currentAudio.pause();
      this.currentAudio = null;
    }
  }

  /**
   * Replays the current section's audio
   */
  replay(): void {
    this.playCurrentSection();
  }

  /**
   * Resets the game back to the menu
   */
  returnToMenu(): void {
    this.stopAudio();
    if (this.state.phase === 'playing' || this.state.phase === 'ended') {
      const stories = this.state.phase === 'playing'
        ? [this.state.story] // We'd need to store all stories to properly return
        : [this.state.story];
      this.state = { phase: 'menu', stories };
      this.notifyStateChange();
    }
  }

  /**
   * Gets the current game state
   */
  getState(): GameState {
    return this.state;
  }

  /**
   * Notifies listeners of state changes
   */
  private notifyStateChange(): void {
    if (this.onStateChange) {
      this.onStateChange(this.state);
    }
  }

  /**
   * Cleanup
   */
  destroy(): void {
    this.stopAudio();
  }
}
