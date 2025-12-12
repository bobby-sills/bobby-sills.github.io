// Story type definitions
export interface StoryChoice {
  label: string;
  next_id: string;
}

export interface StorySection {
  text: string;
  choices?: StoryChoice[];
  is_ending?: boolean;
  ending_type?: 'good' | 'bad' | 'neutral';
}

export interface Story {
  id: string;
  title: string;
  start_section: string;
  sections: Record<string, StorySection>;
}

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/bobby-sills/telephone-gamebook-backend/main';

/**
 * Fetches and parses a story file from GitHub
 */
async function fetchStoryFromGitHub(filename: string): Promise<Story> {
  const url = `${GITHUB_RAW_BASE}/stories/${filename}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch story: ${filename}`);
  }

  const code = await response.text();

  // Parse the CommonJS module
  // The file exports using: module.exports = storyObject;
  // We need to extract the story object from the code
  const story = parseStoryModule(code);

  return story;
}

/**
 * Parses a CommonJS story module and extracts the story object
 */
function parseStoryModule(code: string): Story {
  // Create a safe evaluation context
  // The story files follow the pattern: const storyName = {...}; module.exports = storyName;

  // Remove the module.exports line and extract the story object
  const storyObjectMatch = code.match(/const\s+\w+\s*=\s*(\{[\s\S]*?\});?\s*module\.exports/);

  if (!storyObjectMatch) {
    throw new Error('Could not parse story module');
  }

  // Parse the JSON-like object (it's valid JavaScript object literal)
  // We use Function constructor for safe evaluation of the object literal
  const storyObject = new Function(`return ${storyObjectMatch[1]}`)();

  return storyObject as Story;
}

/**
 * Fetches all available stories from GitHub
 */
export async function fetchAllStories(): Promise<Story[]> {
  const storyFiles = [
    'space_adventure.js',
    'fantasy_adventure.js',
    'detective_adventure.js'
  ];

  const stories = await Promise.all(
    storyFiles.map(file => fetchStoryFromGitHub(file))
  );

  return stories;
}

/**
 * Constructs the GitHub URL for a story section's audio file
 */
export function getAudioUrl(storyId: string, sectionId: string): string {
  return `${GITHUB_RAW_BASE}/public/${storyId}/${sectionId}.mp3`;
}

/**
 * Gets the welcome audio URL
 */
export function getWelcomeAudioUrl(): string {
  return `${GITHUB_RAW_BASE}/public/welcome.mp3`;
}
